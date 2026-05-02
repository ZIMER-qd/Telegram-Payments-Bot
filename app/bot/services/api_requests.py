import logging

from app.bot.core.http_client import get_client


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# products
async def create_user_product(tg_id: int, product_code: str, expire: int | None) -> dict | None:
    client = await get_client()
    
    response = await client.post(
        "/products/add", 
        json={
            "tg_id": tg_id,
            "product_code": product_code,
            "expire": expire
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None

    return response.json()


async def get_product_by_code(code: str) -> dict | None:
    client = await get_client()
    
    response = await client.get(
        "/products/by_code",
        params={
            "code": code
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None

    return response.json()


async def check_user_product(tg_id: int, product_code: int) -> dict | None:
    client = await get_client()
    
    response = await client.get(
        "/products/check",
        params={
            "tg_id": tg_id,
            "product_code": product_code
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None
    
    return response.json()


async def get_products_by_type(type_name: str) -> list[dict] | None:
    client = await get_client()
    
    response = await client.get(
        "/products/by_type",
        params={
            "type_name": type_name
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None
    
    return response.json()


async def get_user_product_codes(tg_id: int) -> list[dict] | None:
    client = await get_client()
    
    response = await client.get(
        "/products/user/by_codes",
        params={
            "tg_id": tg_id
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None
    
    return response.json()


# purchases
async def get_user_purchases(tg_id: int) -> dict | None:
    client = await get_client()
    
    response = await client.get(
        "/purchases/user",
        params={
            "tg_id": tg_id
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None
    
    return response.json()

# users
async def create_user(tg_id: int, name: str) -> dict | None:
    client = await get_client()
    
    response = await client.post(
        "/users/add",
        json={
            "tg_id": tg_id,
            "name": name
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None
    
    return response.json()

# subscriptions
async def delete_user_sub(tg_id: int) -> dict | None:
    client = await get_client()
    
    response = await client.delete(
        "/sub/del",
        params={
            "tg_id": tg_id
        }
    )

    if not response.is_success:
        logging.warning(f"API error {response.status_code}: {response.text}")
        return None
    
    return response.json()