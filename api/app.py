from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from context.utils import Order, DeliveryFeeResponse, final_cost

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/calculate-delivery-fee", response_model=DeliveryFeeResponse)
def calculate_delivery_fee(order: Order):
    """
    Calculate the delivery fee based on the order details.

    This endpoint accepts an order with details such as cart value, delivery distance,
    number of items, and order time, and returns the calculated delivery fee.

    Args:
        order (Order): The order details required to calculate the delivery fee.

    Returns:
        DeliveryFeeResponse: The response containing the calculated delivery fee.
    """
    try:
        delivery_fee = final_cost(order)
        return DeliveryFeeResponse(delivery_fee=delivery_fee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    """
    Root endpoint providing basic information about the API.
    """
    api_info = {
        "name": "Delivery Fee Calculator API",
        "version": "1.0.0",
        "description": "This API calculates the delivery fee based on cart value, distance, number of items, and time."
    }
    return JSONResponse(content=api_info)
