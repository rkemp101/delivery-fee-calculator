# Delivery Fee Calculator API

## Introduction

The Delivery Fee Calculator API is a Python-based HTTP API designed to provide a simple and efficient way to calculate delivery fees based on various factors such as the cart value, the number of items in the cart, the time of the order, and the delivery distance.

This code is needed when a customer is finalized their shopping cart and is ready to know how much the delivery will cost.

## Specification
Rules for calculating a delivery fee
* If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
* A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
  * Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  * Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  * Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
* If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
  * Example 1: If the number of items is 4, no extra surcharge
  * Example 2: If the number of items is 5, 50 cents surcharge is added
  * Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
  * Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
  * Example 5: If the number of items is 14, 6,20€ surcharge is added ((10 * 50 cents) + 1,20€)
* The delivery fee can __never__ be more than 15€, including possible surcharges.
* The delivery is free (0€) when the cart value is equal or more than 200€.
* During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€). **In order to avoid confusion regarding timezones, the backend utilises UTC**.

## Prerequisites

* Python 3.8+
* Other dependencies listed in `requirements.txt`

## Installation and Usage
* For quick installation execute the **`make`** command from the root directory or `pip install` the requirements.txt.

```
.
├── api
│   ├── __init__.py
│   ├── fast.py
├── context
│   ├── __init__.py
│   ├── params.py
│   ├── utils.py
├── tests
│   ├── __init__.py
│   ├── fast_test.py
│   ├── utils_test.py
├── Makefile
├── README.md
└── requirements.txt
```

* Option 1:
  ```make setup```

* Option 2:
  ```pip install -r requirements.txt```

### Running the tests
* Test individual functions:
  ```make test_utils```

* Test final output of response:
  ```test_api```

## Running the app

* To test the API you can execute the **`make`** command from the root directory.

  * Option 1:
    ```make run_api_local```

  * Option 2:
    ```uvicorn api.fast:app --reload```

* Once running, head over to the Open API Docs example: (http://127.0.0.1:8000/docs)

* In the Open API Docs select the POST method for the endpoint "/ calculate-delivery-fee".
* Click on Try it out and then >>> Execute.
* A JSON request will be sent to the API and the API response can be located in the response body.
* Values in the request body to test out the API, in order to reproduce tests.
