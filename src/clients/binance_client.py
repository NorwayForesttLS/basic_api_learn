from binance.client import Client
import os

API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_API_SECRET")

binance_client = Client(API_KEY,SECRET_KEY)
