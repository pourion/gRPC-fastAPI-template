import os
from dotenv import load_dotenv
import pdb

from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
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

redis = get_redis_connection(
    host=REDIS_CLOUD_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWD,
    decode_responses=True,
)


# everytime we query Product it will be stored in the redis connection
class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta:
        database = redis



@app.get('/products')
def all():
    # return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]


def format(primary_key: str):
    product = Product.get(primary_key)
    return {
        'id' : product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }


@app.post('/products')
def create(product: Product):
    return product.save()

# get by product id. E.g, http://localhost:8000/products/01HD5F85AK65KRWRHWZQFHMPQN 
@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)