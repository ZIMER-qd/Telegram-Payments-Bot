from aiogram.fsm.state import State, StatesGroup


class DiceGame(StatesGroup):
    user_number = State()
    dice_number = State()
    result = State()