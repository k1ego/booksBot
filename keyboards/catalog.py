from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_catalog_kb(catalog):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category_cb, category in catalog.items():
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=category["text"], 
                    callback_data=f"category:{category_cb}"
                )
            ]
        )
    return keyboard
