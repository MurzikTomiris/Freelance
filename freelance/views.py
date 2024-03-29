from django.views.generic import ListView, DetailView, TemplateView
from .models import Service, Order, Executor, Customer


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
