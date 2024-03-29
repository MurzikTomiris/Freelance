from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
)

from .forms import OrderForm
from .models import Service, Order, Executor, Customer
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPageView(TemplateView):
    template_name = "basic/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Это главная страница проекта"
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


class OrderListView(ListView):
    model = Order
    template_name = "freelance/orders/order_list.html"  # Укажите ваш путь к шаблону
    context_object_name = "orders"


class OrderDetailView(DetailView):
    model = Order
    template_name = "freelance/orders/order_detail.html"  # Укажите ваш путь к шаблону
    context_object_name = "order"

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "freelance/orders/order_create.html"
    form_class = OrderForm
    success_url = reverse_lazy(
        "freelance:order-success"
    )  # URL для перенаправления после успешного создания

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_label"] = "Создание заказа"
        return context

    def form_valid(self, form):
        # Получаем объект Customer для текущего пользователя
        customer_profile, created = Customer.objects.get_or_create(
            user=self.request.user
        )
        form.instance.customer = customer_profile
        return super().form_valid(form)


class OrderEditView(LoginRequiredMixin, UpdateView):
    template_name = "freelance/orders/order_create.html"
    form_class = OrderForm
    model = Order
    success_url = reverse_lazy(
        "freelance:order-success"
    )  # URL для перенаправления после успешного создания

    def get_context_data(self, **kwargs):
        if (
            Order.objects.get(id=self.kwargs["pk"]).customer == None or self.request.user != Order.objects.get(id=self.kwargs["pk"]).customer.user
            or not self.request.user.is_authenticated
        ):
            raise PermissionDenied
        context = super().get_context_data(**kwargs)
        context["title_label"] = "Редактирование заказа"
        return context

    def form_valid(self, form):
        # Получаем объект Customer для текущего пользователя
        customer_profile, created = Customer.objects.get_or_create(
            user=self.request.user
        )
        form.instance.customer = customer_profile
        return super().form_valid(form)