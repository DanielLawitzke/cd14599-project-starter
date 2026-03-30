# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.


class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """

    def __init__(self, storage):
        required_methods = ["save_order", "get_order", "get_all_orders"]
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(
                    f"Storage object must implement a callable '{method}' method."
                )
        self.storage = storage

    def add_order(
        self,
        order_id: str,
        item_name: str,
        quantity: int,
        customer_id: str,
        status: str = "pending",
    ):
        if self.storage.get_order(order_id) is not None:
            raise ValueError(f"Order with ID '{order_id}' already exists.")
        self.storage.save_order(
            order_id,
            {
                "item_name": item_name,
                "quantity": quantity,
                "customer_id": customer_id,
                "status": status,
            },
        )

    def get_order_by_id(self, order_id: str):
        return self.storage.get_order(order_id)

    VALID_STATUSES = {"pending", "processing", "shipped", "delivered", "cancelled"}

    def update_order_status(self, order_id: str, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'.")
        order = self.storage.get_order(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found.")
        order["status"] = new_status
        self.storage.save_order(order_id, order)

    def list_all_orders(self):
        return list(self.storage.get_all_orders().values())

    def list_orders_by_status(self, status: str):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'.")
        return [
            v
            for v in self.storage.get_all_orders().values()
            if v.get("status") == status
        ]
