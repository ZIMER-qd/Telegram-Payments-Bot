from datetime import datetime

from typing import Iterable

def formatting_user_status(data: Iterable):
    funcs = []
    text = f"Профиль:\n" 
    
    print(data[1])
    if data[1]:
        date = datetime.strftime(data[1], "%d.%m.%Y")
        text += f"Подписка до {date}\n"
    else:
        text += f"Подписки нет\n"

    for product in data[0]:
        if product.type == 'function':
            funcs.append(product.name)
    
    text += f"Купленные функции - {len(funcs)}\n"
    
    if funcs:
        for func in funcs:
            text += f"- {func}\n"

    return text
        



