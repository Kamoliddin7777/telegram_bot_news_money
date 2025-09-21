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
    markup=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    btn1 = KeyboardButton("📈 Курсы валют")
    btn2 = KeyboardButton("📰 Новости")
    btn3=KeyboardButton("⛅ Погода")
    btn4=KeyboardButton("📅 Ближайшие события")
    markup.add(btn1, btn2,btn3,btn4)
    return markup
def news_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    btn1 = KeyboardButton("📰 Экономика")
    btn2 = KeyboardButton("💼 Бизнес")
    btn3 = KeyboardButton("📚 Новости — Обучение")
    btn4 = KeyboardButton("🎓 Новости нашего универа")
    markup.add(btn1, btn2, btn3,btn4)
    return markup
def events_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = KeyboardButton("🎭 Театры / спектакли")
    btn3 = KeyboardButton("🎤 Концерты / музыка")
    markup.add(btn2, btn3)
    return markup
