from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import os
import instructor

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

_sync_client = None
_async_client = None

def get_sync_client() -> OpenAI:
    global _sync_client
    if _sync_client is None:
        _sync_client = instructor.patch(OpenAI(api_key=api_key))
    return _sync_client

def get_async_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        _async_client = instructor.patch(AsyncOpenAI(api_key=api_key))
    return _async_client