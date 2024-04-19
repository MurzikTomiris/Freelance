from django.urls import path
from .views import (
    MainPageView,
    ServiceListView,
    ServiceDetailView,
    OrderListView,
    OrderDetailView,
    ExecutorListView,
    ExecutorDetailView,
    CustomerListView,
    CustomerDetailView,
    CustomLogoutView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderEditView,
    ExecutorsRequestsListView,
    OrderRequestView, CustomerAccessOrderView, CustomerAccessOrdersView,
)

app_name = "freelance"

urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("executors/", ExecutorListView.as_view(), name="executor-list"),
    path("executors/<int:pk>/", ExecutorDetailView.as_view(), name="executor-detail"),
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/edit/<int:pk>", OrderEditView.as_view(), name="order-edit"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/success/", OrderListView.as_view(), name="order-success"),
    path("orders/request/<int:pk>", OrderRequestView.as_view(), name="order-request"),
    path("executors/requests/", ExecutorsRequestsListView.as_view(), name="executor-requests"),

    path("customer_access_order", CustomerAccessOrderView.as_view(), name="customer-access-order"),
    path("customer_access_orders", CustomerAccessOrdersView.as_view(), name="customer-access-orders"),
]
