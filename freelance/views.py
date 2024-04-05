from django.db.models.base import Model as Model
from django.db import IntegrityError, transaction
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
)


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse_lazy

from freelance.forms import OrderForm
from .models import Service, Order, Executor, Customer, UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import UserRegistrationForm


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


class MainPageView(TemplateView):
    template_name = "basic/index.html"
    paginate_by = 2  # Устанавливаем количество элементов на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Это главная страница проекта"
        # Получаем заказы, которые не взяты в работу

        orders_taken = Order.objects.filter(order_taken=False)
        # Инициализируем объект Paginator
        paginator = Paginator(orders_taken, self.paginate_by)

        # Получаем номер страницы из GET-параметра
        page_number = self.request.GET.get("page")

        try:
            # Получаем объект страницы
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # Если номер страницы не целое число, показываем первую страницу
            page = paginator.page(1)
        except EmptyPage:
            # Если номер страницы больше максимального, показываем последнюю страницу
            page = paginator.page(paginator.num_pages)

        context["pending_orders"] = page
        return context


class ExecutorListView(ListView):
    model = Executor
    template_name = (
        "freelance/executors/executor_list.html"  # Укажите ваш путь к шаблону
    )
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
