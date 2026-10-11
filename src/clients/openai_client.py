import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()

OPENAI_CLIENT = OpenAI(timeout=30.0)
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

