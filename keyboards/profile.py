from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def profile_menu():
		return InlineKeyboardMarkup(
				inline_keyboard=[
						[
								InlineKeyboardButton(
										text="Пополнить баланс",
										callback_data="deposit"
								)
						]
				]
		)

def cancel_deposit_action():
		return InlineKeyboardMarkup(
				inline_keyboard=[
						[
								InlineKeyboardButton(
										text="Отмена",
										callback_data="cancel_deposit"
								)
						]
				]
		)

def confirm_deposit_action():
		return InlineKeyboardMarkup(
				inline_keyboard=[
						[
								InlineKeyboardButton(
										text="Нет",
										callback_data="cancel_deposit"
								),
								InlineKeyboardButton(
										text="Да",
										callback_data="apply_deposit"
								)
						]
				]
		)