from aiogram import F, Router, types
from aiogram.enums import ParseMode

from keyboards import profile as profile_kb
from repositories.user import UserRepo

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.profile import UserDepositState

router = Router()


@router.message(F.text == "Профиль")
async def user_profile_info(
    message: types.Message, user_repo: UserRepo, state: FSMContext
):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)

    await message.answer(
        f"<b>{message.from_user.full_name}</b>\n\n"
        f"Username - {user.username or 'Не указан'}\n"
        f"ID - <code>{user.tg_id}</code>\n"
        f"Ваш баланс - {user.view_balance} руб.",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_kb.profile_menu(),
    )


@router.callback_query(F.data == "deposit")
async def user_deposit_action(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "Введите сумму пополнения:", reply_markup=profile_kb.break_action_and_back_to_main_menu()
    )
    await state.set_state(UserDepositState.INPUT_AMOUNT)


@router.callback_query(StateFilter(UserDepositState), F.data == "cancel_deposit")
async def user_deposit_action_cancel(
    callback_query: types.CallbackQuery, state: FSMContext, user_repo: UserRepo
):
    await state.clear()
    await callback_query.answer()

    user = await user_repo.get_user_by_tg_id(callback_query.from_user.id)

    await callback_query.message.answer(
        f"<b>{callback_query.from_user.full_name}</b>\n\n"
        f"Username - {user.username or 'Не указан'}\n"
        f"ID - <code>{user.tg_id}</code>\n"
        f"Ваш баланс - {user.view_balance} руб.",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_kb.profile_menu(),
    )


@router.message(UserDepositState.INPUT_AMOUNT)
async def user_deposit_amount(
    message: types.Message, state: FSMContext, user_repo: UserRepo
):
    if not message.text.isdigit():
        await message.answer("Сумма должна быть числом. Попробуйте еще раз.")
        return

    amount = int(message.text)
    if amount <= 0:
        await message.answer(
            "Сумма должна быть положительным числом. Попробуйте еще раз."
        )
        return

    # Сохранение суммы в состоянии
    await state.update_data(deposit_amount=amount)

    await message.answer(
        f"Вы хотите пополнить баланс на {amount} руб. Подтвердите действие.",
        reply_markup=profile_kb.confirm_deposit_action(),
    )
    await state.set_state(UserDepositState.APPLY_DEPOSIT)


@router.callback_query(UserDepositState.APPLY_DEPOSIT)
async def apply_deposit_user(
    callback_query: types.CallbackQuery, state: FSMContext, user_repo: UserRepo
):
    state_data = await state.get_data()
    deposit_amount = state_data.get("deposit_amount")

    
    await user_repo.update_balance(callback_query.from_user.id, deposit_amount)
    await callback_query.message.edit_text(
        f"Баланс успешно пополнен на {deposit_amount} руб.",
        reply_markup=profile_kb.break_action_and_back_to_main_menu(
            "Профиль"
        ),
    )
    
    await callback_query.answer()

    