from django.urls import path

from ratings.views import RatingListView, RatingUpdateView
from .views import (
    CustomLogoutView,
    MainPageView,
    ServiceListView,
    ServiceDetailView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderEditView,
    OrderRequestView,
    ExecutorListView,
    ExecutorDetailView,
    ExecutorsRequestsListView,
    CustomerListView,
    CustomerDetailView,
    CustomerAccessOrderView,
    CustomerAccessOrdersView,
)

app_name = "freelance"

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("", MainPageView.as_view(), name="main_page"),
    # Executors
    path("executors/", ExecutorListView.as_view(), name="executor-list"),
    path("executors/<int:pk>/", ExecutorDetailView.as_view(), name="executor-detail"),
    path("executors/requests/", ExecutorsRequestsListView.as_view(), name="executor-requests"),
    # Customers
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customers/access-orders/", CustomerAccessOrdersView.as_view(), name="customer-access-orders"),
    path("customers/access-order/<int:pk>/", CustomerAccessOrderView.as_view(), name="customer-access-order"),

    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    # Orders
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/edit/<int:pk>", OrderEditView.as_view(), name="order-edit"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("orders/request/<int:pk>", OrderRequestView.as_view(), name="order-request"),
    path("orders/success/", OrderListView.as_view() , name="order-success"),
]


