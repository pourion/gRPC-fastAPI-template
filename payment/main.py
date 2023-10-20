import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from starlette.requests import Request

from redis_om import get_redis_connection, HashModel

import requests


app = FastAPI()


# frontend runs on port 3000 but backend on 8000, middleware fixes it
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)


# Load environment variables from the .env file
load_dotenv(dotenv_path='../.env')
# Access the environment variable
REDIS_PASSWD = os.getenv("REDIS_PASSWORD")
REDIS_CLOUD_URL = os.getenv("REDIS_CLOUD_URL")
REDIS_PORT= os.getenv("REDIS_PORT")


# this should be a separate database than inventory
# but because second redis cloud db is not free I use the same one
# this database doesnt need to be redis though; it could be MongoDB, etc.
redis = get_redis_connection(
    host=REDIS_CLOUD_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWD,
    decode_responses=True,
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded
    
    class Meta:
        database = redis
        



@app.get('/orders/{pk}')
def get(pk: str):
    order = Order.get(pk)
    # redis.xadd('refund_order', order.dict(), '*')
    return order




@app.post('/orders')
async def create(req: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await req.json()
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2*product['price'],
        total=1.2*product['price'],
        quantity=body['quantity'],
        status='pending',
    )
    order.save()
    
    background_tasks.add_task(order_completed, order)
    
    
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')  # event to send to inventory to subtract quantity after payment
