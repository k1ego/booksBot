from aiogram import F, Router, types

router = Router()


@router.message(F.text == "О нас")
async def info(message: types.Message):
    await message.answer(
        (
            "Я бот для покупки книг.\n"
            "Ты можешь посмотреть весь\n"
            "мой каталог и купить понравившуюся книжку.\n\n"
            "Хорошего чтения!"
        )
    )
