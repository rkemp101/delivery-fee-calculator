import pytest
from context.utils import Order, cart_value_surcharge, calculate_distance_surcharge, calculate_item_surcharge, peak_hour_surcharge, final_cost

### TEST_CART_VALUE_SURCHARGE ###

def test_cart_value_surcharge_non_integer_input():
    with pytest.raises(TypeError):
        cart_value_surcharge("1000")
        cart_value_surcharge(3000.)

def test_cart_value_surcharge_zero_or_less_input():
    with pytest.raises(ValueError):
        cart_value_surcharge(0)
        cart_value_surcharge(-1000)

def test_cart_value_surcharge():
    # Cart Value < 10 Euro.
    assert cart_value_surcharge(500) == 500
    assert cart_value_surcharge(790) == 210

    # Cart Value > 10 Euro.
    assert cart_value_surcharge(1000) == 0
    assert cart_value_surcharge(5000) == 0

    # Cart Value >= 100 Euro. Free Delivery
    assert cart_value_surcharge(10000) == 0
    assert cart_value_surcharge(30000) == 0

### TEST_CALCULATE_DISTANCE_SURCHARGE ###

def test_calculate_distance_surcharge_non_integer_input():
    with pytest.raises(TypeError):
        calculate_distance_surcharge("1000")
        calculate_distance_surcharge(3000.)

def test_calculate_distance_surcharge_zero_or_less_input():
    with pytest.raises(ValueError):
        calculate_distance_surcharge(0)
        calculate_distance_surcharge(-1000)

def test_calculate_distance_surcharge():
    # Base Delivery Fee
    assert calculate_distance_surcharge(500) == 200
    assert calculate_distance_surcharge(1000) == 200

    # Base Delivery Fee + 1 Euro per 500 meter
    assert calculate_distance_surcharge(1499) == 300
    assert calculate_distance_surcharge(1500) == 300
    assert calculate_distance_surcharge(1501) == 400

### TEST_CALCULATE_ITEM_SURCHARGE ###

def test_calculate_item_surcharge_non_integer_input():
    with pytest.raises(TypeError):
        calculate_item_surcharge("5")
        calculate_item_surcharge(5.)

def test_calculate_item_surcharge_zero_or_less_input():
    with pytest.raises(ValueError):
        calculate_item_surcharge(0)
        calculate_item_surcharge(-5)

def test_calculate_item_surcharge():
    # No surcharge for orders with less than 5 items
    assert calculate_item_surcharge(1) == 0
    assert calculate_item_surcharge(4) == 0

    # Additional 50 cent surcharge for each item above and including the 5th item
    assert calculate_item_surcharge(5) == 50
    assert calculate_item_surcharge(10) == 300

    # Additional 50 cent surcharge for each item above and including the 5th item + \
    # One-off 120 cent bulk fee for only 13th item
    assert calculate_item_surcharge(13) == 570 # ((9 * 50 cents) + 120 cents)
    assert calculate_item_surcharge(14) == 620 # ((10 * 50 cents) + 120 cents)

### TEST_PEAK_HOUR_SURCHARGE ###

def test_peak_hour_surcharge_non_string_input():
    with pytest.raises(TypeError):
        peak_hour_surcharge(12345, 1000)  # Test with a non-string input

def test_peak_hour_surcharge_invalid_format():
    with pytest.raises(ValueError):
        peak_hour_surcharge("2024-01-15 15:00:00", 1000)  # Test with incorrect format

def test_peak_hour_surcharge():
    assert peak_hour_surcharge("2024-01-15T15:00:00Z", 1000) == 1000 # Test for non-Friday order
    assert peak_hour_surcharge("2024-01-19T15:00:00Z", 1000) == 1200 # Test for Friday order during peak-hours
    assert peak_hour_surcharge("2024-01-19T19:00:00Z", 1000) == 1000 # Test for Friday order outside peak-hours
