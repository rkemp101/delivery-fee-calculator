from pydantic import BaseModel, Field
from datetime import datetime
from zoneinfo import ZoneInfo
from context.params import *

class Order(BaseModel):
    """
    A class to represent an order.

    Attributes:
        cart_value (int): Value of the shopping cart in cents.
        delivery_distance (int): Distance between the store and customer’s location in meters.
        number_of_items (int): Number of items in the customer's shopping cart.
        time (str): Order time in UTC in ISO format.
    """
    cart_value: int = Field(..., title="Cart Value",
                            description="Value of the shopping cart in cents.",
                            example=790)
    delivery_distance: int = Field(..., title="Delivery Distance",
                                   description="The distance between the store and customer’s location in meters.",
                                   example=2235)
    number_of_items: int = Field(..., title="Number of Items",
                                 description="The number of items in the customer's shopping cart.",
                                 example=4)
    time: str = Field(..., title="Time",
                      description="Order time in UTC in ISO format.",
                      example="2024-01-15T13:00:00Z")

class DeliveryFeeResponse(BaseModel):
    """
    A class to represent a response containing the delivery fee.

    Attributes:
        delivery_fee (int): The calculated delivery fee in cents.
    """
    delivery_fee: int = Field(..., title="Delivery Fee",
                              description="The calculated delivery fee in cents.",
                              example=710)

def cart_value_surcharge(cart_value: int) -> int:
    """
    Calculate the cart value surcharge based on the cart value.

    Args:
        cart_value (int): The value of the shopping cart.

    Returns:
        int: The surcharge amount for small orders.
    """
    if not isinstance(cart_value, int):
        raise TypeError("Input cart value must be of type 'int'")
    if cart_value <= 0:
        raise ValueError("Input cart value must be greater than zero")
    if cart_value < CART_VALUE_MINIMUM:
        return CART_VALUE_MINIMUM - cart_value
    else:
        return 0

def calculate_distance_surcharge(delivery_distance: int) -> int:
    """
    Calculate the surcharge for delivery distance.

    Args:
        delivery_distance (int): The distance between the partner and customer's location.

    Returns:
        int: The calculated distance surcharge.
    """
    if not isinstance(delivery_distance, int):
        raise TypeError("Input delivery distance must be of type 'int'")
    if delivery_distance <= 0:
        raise ValueError("Input delivery distance must be greater than zero")
    if delivery_distance <= DISTANCE_MINIMUM:
        return BASE_DISTANCE_FEE
    else:
        distance_counter = (delivery_distance - DISTANCE_MINIMUM) // DISTANCE_STEP
        if delivery_distance % DISTANCE_STEP != 0:
            distance_counter += 1

    return BASE_DISTANCE_FEE + (distance_counter * DISTANCE_SURCHARGE_RATE)

def calculate_item_surcharge(number_of_items: int) -> int:
    """
    Calculate the surcharge based on the number of items in the order.

    Args:
        number_of_items (int): The number of items in the order.

    Returns:
        int: The calculated item surcharge.
    """
    if not isinstance(number_of_items, int):
        raise TypeError("Input number of items must be of type 'int'")
    if number_of_items <= 0:
        raise ValueError("Input number of items must be greater than zero")
    if number_of_items >= LARGE_ORDER_MAXIMUM:
        number_of_items -= LARGE_ORDER_MINIMUM
        return (number_of_items * BULK_FEE) + LARGE_ORDER_SURCHARGE
    elif LARGE_ORDER_MINIMUM < number_of_items < LARGE_ORDER_MAXIMUM:
        number_of_items -= LARGE_ORDER_MINIMUM
        return (number_of_items * BULK_FEE)
    else:
        return 0

def peak_hour_surcharge(time: str, subtotal_surcharges: int) -> int:
    """
    Calculate the peak hour surcharge based on the order time and subtotal surcharges.

    Args:
        time (str): The order time in UTC in ISO format.
        subtotal_surcharges (int): The subtotal of other calculated surcharges.

    Returns:
        int: The total surcharge including any peak hour surcharge.
    """
    if not isinstance(time, str):
        raise TypeError("Input time must be a string.")

    try:
        datetime_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise ValueError("Invalid time format. Expected format: YYYY-MM-DDTHH:MM:SSZ")

    datetime_obj = datetime_obj.replace(tzinfo=ZoneInfo("UTC"))
    order_datetime_utc = datetime_obj.astimezone(ZoneInfo("UTC"))

    if order_datetime_utc.weekday() == PEAK_DAY_OF_WEEK and PEAK_HOUR_START <= order_datetime_utc.hour < PEAK_HOUR_END:
        return subtotal_surcharges * PEAK_MULTIPLIER
    else:
        return subtotal_surcharges

def final_cost(order: Order) -> int:
    """
    Calculate the final cost of the order including all surcharges.

    Args:
        order (Order): The order details.

    Returns:
        int: The final cost of the order.
    """
    # Calculating subtotal surcharges
    subtotal_surcharges = cart_value_surcharge(order.cart_value) + \
                          calculate_distance_surcharge(order.delivery_distance) + \
                          calculate_item_surcharge(order.number_of_items)

    # Calculating grand total with potential peak hour surcharge
    grand_total = peak_hour_surcharge(order.time, subtotal_surcharges)

    # Checking for free delivery eligibility
    if order.cart_value >= CART_VALUE_FREE:
        return 0
    else:
        # All orders are limited to 15 euro delivery fee
        return min(GRAND_TOTAL_LIMIT, grand_total)
