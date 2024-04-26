class OrderRequestService:
    def __init__(self, orders, executor_requests):
        self.orders = orders
        self.executor_requests = executor_requests

    def get_orders_data(self):
        orders_data = []
        for order in self.orders:
            show_button = True
            for request in self.executor_requests:
                if request.order.pk == order.pk and request.status != "pending":
                    show_button = False
                    break
            orders_data.append((order, show_button))
        return orders_data
