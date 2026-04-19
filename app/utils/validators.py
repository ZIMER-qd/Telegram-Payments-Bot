def check_number(num: str) -> str | None:
    print(num)
    error = "Число должно быть в диапозоне от 1 до 6.\nПопробуйте ещё раз."
    try:
        num = int(num)
        if num <= 0 or num > 6:
            return error
        return None
    except ValueError:
        return error
