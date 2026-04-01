import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---


@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock


@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)


# --- Tests for add_order ---


def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    # Verify exact payload including default status 'pending'
    mock_storage.save_order.assert_called_once_with(
        "ORD001",
        {
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending",
        },
    )


def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate storage finds existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(
        ValueError, match="Order with ID 'ORD_EXISTING' already exists."
    ):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")


# --- Tests for get_order_by_id ---


def test_get_order_by_id_existing(order_tracker, mock_storage):
    """Tests fetching an existing order by ID."""
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }
    result = order_tracker.get_order_by_id("ORD001")
    assert result["order_id"] == "ORD001"


def test_get_order_by_id_not_found(order_tracker, mock_storage):
    """Tests fetching a non-existent order returns None."""
    mock_storage.get_order.return_value = None
    result = order_tracker.get_order_by_id("NONEXISTENT")
    assert result is None


# --- Tests for update_order_status ---


def test_update_order_status_success(order_tracker, mock_storage):
    """Tests updating an order status successfully."""
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }
    order_tracker.update_order_status("ORD001", "shipped")
    mock_storage.save_order.assert_called_once()


def test_update_order_status_invalid_status(order_tracker, mock_storage):
    """Tests that an invalid status raises ValueError immediately."""
    with pytest.raises(ValueError, match="Invalid status"):
        order_tracker.update_order_status("ORD001", "flying")


def test_update_order_status_not_found(order_tracker, mock_storage):
    """Tests that updating a non-existent order raises ValueError."""
    mock_storage.get_order.return_value = None
    with pytest.raises(ValueError, match="not found"):
        order_tracker.update_order_status("NONEXISTENT", "shipped")


# --- Tests for list_all_orders ---


def test_list_all_orders_empty(order_tracker, mock_storage):
    """Tests listing orders when storage is empty."""
    mock_storage.get_all_orders.return_value = {}
    result = order_tracker.list_all_orders()
    assert result == []


def test_list_all_orders_multiple(order_tracker, mock_storage):
    """Tests listing all orders returns all entries."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
        "ORD002": {"order_id": "ORD002", "status": "shipped"},
    }
    result = order_tracker.list_all_orders()
    assert len(result) == 2


# --- Tests for list_orders_by_status ---


def test_list_orders_by_status_match(order_tracker, mock_storage):
    """Tests filtering orders by status returns only matching ones."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
        "ORD002": {"order_id": "ORD002", "status": "shipped"},
    }
    result = order_tracker.list_orders_by_status("pending")
    assert len(result) == 1
    assert result[0]["order_id"] == "ORD001"


def test_list_orders_by_status_no_match(order_tracker, mock_storage):
    """Tests filtering returns empty list when no orders match."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
    }
    result = order_tracker.list_orders_by_status("shipped")
    assert result == []


def test_list_orders_by_status_invalid(order_tracker, mock_storage):
    """Tests that an invalid status raises ValueError."""
    with pytest.raises(ValueError, match="Invalid status"):
        order_tracker.list_orders_by_status("flying")
