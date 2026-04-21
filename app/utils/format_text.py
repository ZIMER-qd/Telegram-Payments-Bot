from datetime import datetime

from app.database.models import Product
from typing import Tuple, List, Optional

def formatting_user_status(data: Tuple[List[Product], Optional[datetime]]) -> str:
    """Format user profile information for display.

    Args:
        data: Tuple[List[Product], Optional[datetime]]: 
            - List of purchased function products
            - Subscription expiration datetime (if exists)

    Returns:
        str: Formatted profile text.
    """
    funcs, sub_expire = data

    text = f"Профиль:\n" 
    
    if sub_expire:
        date = datetime.strftime(sub_expire, "%d.%m.%Y")
        text += f"Подписка до {date}\n"
    else:
        text += f"Подписки нет\n"
    
    text += f"Купленные функции - {len(funcs)}\n"
    
    if funcs:
        for func in funcs:
            text += f"- {func.name}\n"

    return text
        



