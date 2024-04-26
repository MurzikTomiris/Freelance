from django.db.models.base import Model as Model
from django.db import transaction
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LogoutView
from django.db.models import Exists, OuterRef, Q, Prefetch

from django.urls import reverse_lazy

from freelance.forms import OrderForm
from .models import Service, Order, OrderRequest, Executor, Customer

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import Group

from django.views import View
from .forms import UserRegistrationForm, OrderRequestForm


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        user_data = form.cleaned_data
        user_type = user_data["user_type"]
        group_name = {"customer": "Customers", "executor": "Executors"}.get(user_type)

        if group_name is None:
            return render(
                request,
                self.template_name,
                {"form": form, "error": "Invalid user type"},
            )

        with transaction.atomic():
            group, _ = Group.objects.get_or_create(name=group_name)
            user = form.save()  # Сохраняем пользователя и его профиль через форму
            user.groups.add(group)
            user.save()

            # Создаем Executor или Customer, используя профиль пользователя
        if user_type == "customer":
            customer, _ = Customer.objects.get_or_create(profile=user.userprofile)
        elif user_type == "executor":
            executor, _ = Executor.objects.get_or_create(profile=user.userprofile)

        return redirect("login")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")  # Перенаправление на нужную страницу.


class MainPageView(ListView):
    model = Order  # определяем модель, с которой работаем
    template_name = "basic/index.html"
    context_object_name = "orders"  # более точное имя для 'requests'
    paginate_by = 2

    def get_queryset(self):
        open_requests = OrderRequest.objects.filter(
            order=OuterRef("pk"), status__in=["pending", "rejected"]
        )
        return (
            Order.objects.annotate(has_open_requests=Exists(open_requests))
            .filter(Q(has_open_requests=True) | Q(requests__isnull=True))
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Это главная страница проекта"
        context["title_label"] = "Активные заказы"
        return context


class ExecutorListView(ListView):
    model = Executor
    template_name = "freelance/executors/executor_list.html"
    context_object_name = "executors"


class ExecutorDetailView(DetailView):
    model = Executor
    template_name = (
        "freelance/executors/executor_detail.html"  # Укажите ваш путь к шаблону
    )
    context_object_name = "executor"


class CustomerListView(ListView):
    model = Customer
    template_name = (
        "freelance/customers/customer_list.html"  # Укажите ваш путь к шаблону
    )
    context_object_name = "customers"


class CustomerDetailView(DetailView):
    model = Customer
    template_name = (
        "freelance/customers/customer_detail.html"  # Укажите ваш путь к шаблону
    )
    context_object_name = "customer"


class CustomerAccessOrdersView(LoginRequiredMixin, ListView):
    model = OrderRequest
    template_name = (
        "freelance/customers/customer_access_orders.html"  # Укажите ваш путь к шаблону
    )
    context_object_name = "orders"

    def get_queryset(self):
        """Получаем список заказов для текущего пользователя"""
        if self.request.user.is_authenticated and self.request.user.groups.filter(
            name="Customers"
        ):
            return Order.objects.filter(customer__profile__user=self.request.user)
        return OrderRequest.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_views = []
        order_requests = OrderRequest.objects.filter(
            order__customer__profile__user=self.request.user
        )

        print(order_requests)
        for order_request in order_requests:
            order_views.append(
                {
                    "order_request": order_request,
                    "order": order_request.order,
                }
            )
        context["order_requests"] = order_requests
        context["order_views"] = order_views
        return context


class CustomerAccessOrderView(DetailView):
    model = Order
    template_name = (
        "freelance/customers/customer_access_order.html"  # Укажите ваш путь к шаблону
    )
    context_object_name = "order"

    def get_queryset(self):
        """Получаем список заказов для текущего пользователя"""
        if self.request.user.is_authenticated and self.request.user.groups.filter(
            name="Customers"
        ):
            orders = Order.objects.prefetch_related(
                Prefetch(
                    "requests",
                    queryset=OrderRequest.objects.select_related("executor").distinct(),
                )
            )

            return orders

        return OrderRequest.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_requests"] = self.object.requests.all()
        try:
            context["accepted_executor"] = self.object.requests.get(status="accepted")
        except OrderRequest.DoesNotExist:
            context["accepted_executor"] = None
        return context

    def post(self, request, *args, **kwargs):
        form = request.POST
        accepted_executor = form.get("executor")
        executors = OrderRequest.objects.filter(order__id=form.get("order"))
        for executor in executors:
            executor.status = "rejected"
            if int(accepted_executor) == executor.executor.pk:
                executor.status = "accepted"
            executor.save()

        print(form)

        return redirect("freelance:customer-access-orders")


class ServiceListView(ListView):
    model = Service
    template_name = "freelance/services/service_list.html"  # Укажите ваш путь к шаблону
    context_object_name = "services"


class ServiceDetailView(DetailView):
    model = Service
    template_name = (
        "freelance/services/service_detail.html"  # Укажите ваш путь к шаблону
    )
    context_object_name = "service"


class OrderListView(UserPassesTestMixin, ListView):
    model = Order
    template_name = "freelance/orders/order_list.html"  # Укажите ваш путь к шаблону
    context_object_name = "orders"

    def get_queryset(self):
        """
        Извлекает набор запросов на основе статуса аутентификации
        пользователя и членства в группе.

        Args:
            self (объект): Экземпляр класса.

        Returns:
            QuerySet: Отфильтрованный набор запросов на
            основе статуса аутентификации пользователя и членства в группе.
        """
        user = self.request.user

        if self.request.user.is_authenticated:
            user_groups = user.groups.all()

            if user_groups.filter(name="Customers").exists():
                customer = Customer.objects.get(profile__user=user)
                return Order.objects.filter(customer=customer)

        return Order.objects.all()

    def get_context_data(self, **kwargs):
        """
        Извлекает набор запросов на основе статуса аутентификации
        пользователя и членства в группе.

        Args:
            self (объект): Экземпляр класса.

        Returns:
            QuerySet: Отфильтрованный набор запросов на
            основе статуса аутентификации пользователя и членства в группе.
        """
        context = super().get_context_data(**kwargs)

        order_views = self.get_order_views()

        context["order_views"] = order_views
        context["title_label"] = "Список заказов"
        return context

    def get_order_views(self):
        """
        Извлекает набор запросов на основе статуса аутентификации
        пользователя и членства в группе.

        Args:
            self (объект): Экземпляр класса.

        Returns:
            QuerySet: Отфильтрованный набор запросов на
            основе статуса аутентификации пользователя и членства в группе.
        """
        if not self.request.user.is_authenticated:
            return [(order, None) for order in Order.objects.all()]

        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="Executors").exists():
            executor_requests = OrderRequest.objects.select_related("order").filter(
                executor__profile__user=self.request.user
            )
            return self.get_executor_order_views(executor_requests)

        return [(order, None) for order in Order.objects.all()]

    def get_executor_order_views(self, executor_requests):
        """
        Извлекает набор запросов на основе статуса аутентификации
        пользователя и членства в группе.

        Args:
            self (объект): Экземпляр класса.

        Returns:
            QuerySet: Отфильтрованный набор запросов на
            основе статуса аутентификации пользователя и членства в группе.
        """
        order_views = []
        for order in Order.objects.all():
            status = self.get_order_status(order, executor_requests)
            order_views.append((order, status))
        return order_views

    def get_order_status(self, order, executor_requests):
        """
        Извлекает набор запросов на основе статуса аутентификации
        пользователя и членства в группе.

        Args:
            self (объект): Экземпляр класса.

        Returns:
            QuerySet: Отфильтрованный набор запросов на
            основе статуса аутентификации пользователя и членства в группе.
        """
        for request in executor_requests:
            if request.order.pk == order.pk and request.status:
                return request.get_status_display()
        return None

    def test_func(self):
        """
        Функция требуется для использования миксина UserPassesTestMixin.
        Данная функция всегда возвращает True,
        потому-что всю работу берет на себя get_queryset.
        """
        return True


class OrderDetailView(DetailView):
    model = Order
    template_name = "freelance/orders/order_detail.html"  # Укажите ваш путь к шаблону
    context_object_name = "order"


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "freelance/orders/order_create.html"
    form_class = OrderForm
    success_url = reverse_lazy(
        "freelance:order-success"
    )  # Укажите URL для перенаправления после успешного создания

    def get_context_data(self, **kwargs):
        """
        Устанавливает профиль клиента для текущего пользователя и сохраняет форму.
        Args:
            form (Form): Экземпляр формы, который будет сохранен.
        Returns:
            HttpResponse: Ответ, возвращаемый методом form_valid родительского класса.
        """
        context = super().get_context_data(**kwargs)
        context["title_label"] = "Создание заказа"
        return context

    def form_valid(self, form):
        """
        Устанавливает профиль клиента для текущего пользователя и сохраняет форму.
        Args:
            form (Form): Экземпляр формы, который будет сохранен.
        Returns:
            HttpResponse: Ответ, возвращаемый методом form_valid родительского класса.
        """
        # Получаем объект Customer для текущего пользователя
        customer_profile, created = Customer.objects.get_or_create(
            profile__user=self.request.user
        )
        form.instance.customer = customer_profile
        return super().form_valid(form)


class OrderEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "freelance/orders/order_create.html"
    form_class = OrderForm
    model = Order
    success_url = reverse_lazy(
        "freelance:order-success"
    )  # Укажите URL для перенаправления после успешного создания

    def get_context_data(self, **kwargs):
        """
        Устанавливает профиль клиента для текущего пользователя и сохраняет форму.
        Args:
            form (Form): Экземпляр формы, который будет сохранен.
        Returns:
            HttpResponse: Ответ, возвращаемый методом form_valid родительского класса.
        """
        if (
            Order.objects.get(id=self.kwargs["pk"]).customer == None
            or self.request.user.userprofile
            != Order.objects.get(id=self.kwargs["pk"]).customer.profile
            or not self.request.user.is_authenticated
        ):
            raise PermissionDenied
        context = super().get_context_data(**kwargs)
        context["title_label"] = "Редактирование заказа"
        return context

    def form_valid(self, form):
        """
        Устанавливает профиль клиента для текущего пользователя и сохраняет форму.
        Args:
            form (Form): Экземпляр формы, который будет сохранен.
        Returns:
            HttpResponse: Ответ, возвращаемый методом form_valid родительского класса.
        """
        # Получаем объект Customer для текущего пользователя
        customer_profile, created = Customer.objects.get_or_create(
            profile__user=self.request.user
        )
        form.instance.customer = customer_profile
        return super().form_valid(form)

    def test_func(self):
        """
        Эта функция проверяет, соответствует ли пользователь клиента
        пользователю запроса.
        """
        obj = self.get_object()
        return obj.customer.profile == self.request.user.userprofile


class OrderRequestView(UpdateView):
    model = OrderRequest
    form_class = OrderRequestForm
    template_name = "freelance/orders/order_request.html"
    success_url = reverse_lazy("freelance:order-success")

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        try:
            order_request = OrderRequest.objects.get(
                order=order,
                executor=Executor.objects.get(profile__user=self.request.user),
            )
            form = self.form_class(instance=order_request)
        except OrderRequest.DoesNotExist:
            form = self.form_class(initial={"order": order})
        return render(request, self.template_name, {"form": form, "order": order})

    def post(self, request, *args, **kwargs):
        order_pk = self.kwargs["pk"]
        try:
            order = get_object_or_404(Order, pk=order_pk)
            executor = Executor.objects.get(profile__user=request.user)
        except (Executor.DoesNotExist, Order.DoesNotExist):
            return self.render_form(order)

        form = self.form_class(request.POST)
        with transaction.atomic():
            order_request, created = self.get_or_create_order_request(order, executor)
            order_request.about_executor = request.POST["about_executor"]
            order_request.status = "pending"
            order_request.save()
        return redirect(self.success_url)

    def get_or_create_order_request(self, order, executor):
        return OrderRequest.objects.get_or_create(order=order, executor=executor)

    def render_form(self, order):
        return render(
            self.request,
            self.template_name,
            {"form": self.form_class(), "order": order},
        )


class ExecutorsRequestsListView(ListView):
    template_name = "freelance/executors/executors-requests.html"
    context_object_name = "requests"

    def get_queryset(self):
        executor = Executor.objects.get(profile__user=self.request.user)
        return OrderRequest.objects.filter(executor=executor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_label"] = "Заявки"
        return context
