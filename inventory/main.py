import os
from dotenv import load_dotenv
import pdb

from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel

app = FastAPI()

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
    return []