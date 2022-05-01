from aiogram import types
from loader import dp
from states import Accounts
from aiogram.dispatcher import FSMContext
from utils import send_all_admin
from data.config import admin_login

@dp.message_handler(text="INFO", state='*')
async def info_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "- Аккаунт(ы) зарегистрирован на почту rambler, верифицирован номер.\nПодойдет под любой дискорд сервер.\n- После покупки, вы получаете текстовый документ с аккаунтами  в формате почта:пароль:токен и инструкцию по заходу на аккаунт через токен.")


@dp.message_handler(text="ПОМОЩЬ 🆘", state='*')
async def help_message(message: types.Message, state: FSMContext):
    await state.finish()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Связаться с  поддержкой ", url=f'https://t.me/{admin_login}'))
    await message.answer("Связаться с  поддержкой", reply_markup=markup)


@dp.message_handler(text="Заказать discord  аккаунт(ы)", state="*")
async def buy_message(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Стоимость одного аккаунта - 1$\n\nВведите кол-во аккаунтов")
    await Accounts.count.set()


@dp.callback_query_handler(text='change_order', state='*')
async def buy_message(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Стоимость одного аккаунта - 1$\n\nВведите кол-во аккаунтов")
    await Accounts.count.set()


@dp.message_handler(state=Accounts.count)
async def get_count(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        get_count = int(message.text)
        await state.finish()
        markup = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text='да', callback_data=f'confirm_order_{get_count}'),
                   types.InlineKeyboardButton(text='нет', callback_data='cancel_order')]
        markup.add(*buttons)
        markup.add(types.InlineKeyboardButton(text='изменить', callback_data='change_order'))
        await message.answer(f"Ваш заказ {get_count} аккаунт?",
                             reply_markup=markup)
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n")


@dp.callback_query_handler(text_startswith="confirm_order")
async def confirm_payment(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Спасибо за заказ, ожидайте  продавца!')
    count = call.data.split('_')[2]
    user = call.from_user.username
    await send_all_admin(f"@{user} совершил заказ {count} аккаунт")


@dp.callback_query_handler(text_startswith="cancel_order")
async def cancel_payment(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Ваш заказ отменен.')
