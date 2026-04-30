def check_number(num: str) -> str | None:
    """Checking the number

    Args:
        num (str): Number entered by the user.

    Returns:
        str | None: String if was a mistake otherwise None.
    """

    print(num)
    error = "Число должно быть в диапозоне от 1 до 6.\nПопробуйте ещё раз."
    try:
        num = int(num)
        if num <= 0 or num > 6:
            return error
        return None
    except ValueError:
        return error
    

def has_access(products: set, code: str) -> bool:
    """
    Check whether a specific function is доступна пользователю.

    Args:
        products (Set[str]): Set of product codes owned by the user.
        code (str): Target function code to check.

    Returns:
        bool: True if the user has access to the function
        (either directly or via 'func_all'), otherwise False.
    """
    
    result = any(item['code'] == code or item['code'] == 'func_all' for item in products)
    return result