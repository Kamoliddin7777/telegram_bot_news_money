from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from config import CURRENCY as currency
def currency_btn(src=''):
    markup=InlineKeyboardMarkup(row_width=2)
    buttons=[]
    for key,value in currency.items():
        btn=InlineKeyboardButton(text=value,callback_data=f"currency_{src}_{key}")
        buttons.append(btn)
    markup.add(*buttons)
    return markup
def contact_btn():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    btn=KeyboardButton('Отправить контакты ☎',request_contact=True)
    markup.add(btn)
    return markup
def main_menu():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📈 Курсы валют")
    btn2 = KeyboardButton("📰 Новости")
    markup.add(btn1, btn2)
    return markup
