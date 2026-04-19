def has_access(products: set, code: str) -> False | True:
    result = code in products or 'func_all' in products
    return result