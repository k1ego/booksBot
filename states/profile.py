from aiogram.fsm.state import State, StatesGroup

class UserDepositState(StatesGroup):
		INPUT_AMOUNT = State()
		APPLY_DEPOSIT = State()