import httpx
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

client: httpx.AsyncClient | None = None


async def create_http_client():
    global client

    client = httpx.AsyncClient(
        base_url="http://127.0.0.1:8000",
        timeout=10
    )
    logging.info("Session connection created")


async def close_http_client():
    global client

    if client:
        await client.aclose()
        logging.info("Session connection closed")


# async def get_client():
#     if client is None:
#         raise RuntimeError("HTTP client is not initialized")
    
#     return client