from telebot import TeleBot
from telebot.types import Message,CallbackQuery,ReplyKeyboardRemove
import os
from dotenv import load_dotenv
from buttons import currency_btn,contact_btn,main_menu
import requests
from config import CURRENCY
from base_curse import get_history,save_translate_data,get_user,save_info
from news import get_news
load_dotenv()
token=os.getenv('TOKEN')
bot=TeleBot(token)
@bot.message_handler(commands=['start','help','about','history'])
def commands(message:Message):
    chat_id=message.chat.id
    if message.text=='/start':
        user=get_user(chat_id)
        if user:
              user_name=message.from_user.username
              bot.send_message(chat_id,f'👋🏻 Здравствуйте {user_name}\nВас приветствует бот по курсам валют и новостям!')
              bot.send_message(chat_id,f'Веберите из меню что вы желаете',reply_markup=main_menu())
    elif message.text=='/help':
        bot.send_message(chat_id,f'🛠Чтобы связаться с разработчиком пишите на аккаунт @um1dov7,если возникнут проблемы')
    elif message.text=='/about':
        bot.send_message(chat_id,'''💱 Добро пожаловать в Currency & News Bot!  
Здесь вы можете:  
🔸 Узнать актуальные курсы валют  
🔸 Читать свежие новости  

Просто нажми на /start для запуска бота''')
    elif message.text=='/history':
        history = get_history(chat_id)
        text_history = ''
        if history:
            for i in history:
                text_history += f'''
Сумма который вы ввели:  {i[0]}
Валюта с которого перевели:  {i[1]}
Валюта на который перевели:  {i[2]}
Перевод курса:  {i[3]}
        '''
            bot.send_message(chat_id, text_history)
        else:
            bot.send_message(chat_id, 'У вас пока нет истории переводов')

@bot.message_handler(regexp='📈 Курсы валют')
def reaction_convercy(message:Message):
    chat_id = message.chat.id
    msg_id =message.message_id
    bot.delete_message(chat_id,msg_id)
    bot.send_message(chat_id,'Вы выбрали курсы валют 💱"',reply_markup=ReplyKeyboardRemove())
    confirm_asc_src(message)
@bot.message_handler(regexp='📰 Новости')
def reaction_news(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел новостей', reply_markup=ReplyKeyboardRemove())
    ask_count_news(message)
def ask_count_news(message:Message):
    chat_id = message.chat.id
    bot.send_message(chat_id,'📄 Напишите количество новостей, которые хотите узнать')
    bot.register_next_step_handler(message,get_count)

def get_count(message:Message):
    chat_id = message.chat.id
    if message.text.startswith('/'):
        commands(message)
    else:
        try:
            count=int(message.text.strip())
            bot.send_message(chat_id,f'📰 Отлично! Показываю {count} последних новостей.')
            confirm_news(message,count)
        except ValueError:
            bot.send_message(chat_id,'❌ Пожалуйста, введите число')
            ask_count_news(message)

def confirm_news(message:Message,count):
    chat_id = message.chat.id
    lst_news=get_news(count)
    for news in lst_news:
             bot.send_message(chat_id,f'Заголовок новости:{news["title"]}\nКраткое описание:{news["content"]}\nДата:{news["data_time"]}\nСсылка на фотографию: {news["photo"]}\nПодробнее:{news["url"]}')
    after_news(message)
def after_news(message:Message):
    chat_id=message.chat.id
    bot.send_message(chat_id,'Введите еще количество новостей которые вас интересует или выберите другую команду')
    bot.register_next_step_handler(message,get_count)


def confirm_asc_src(message:Message):
    chat_id=message.chat.id
    bot.send_message(chat_id,'Выберите с какого курса нужно перевести:',reply_markup=currency_btn('src'))
@bot.callback_query_handler(lambda call:'src' in call.data)
def confirm_src(call:CallbackQuery):
    chat_id=call.message.chat.id
    text_src = call.data.split('_')[2]
    msg_id = call.message.message_id
    bot.edit_message_text(chat_id=chat_id,message_id=msg_id,text='Выберите курс на который хотите перевести:',reply_markup=currency_btn(text_src))

@bot.callback_query_handler(lambda call: 'currency' in call.data)
def get_desc(call:CallbackQuery):
    chat_id=call.message.chat.id
    _,text_src,text_target=call.data.split('_')
    msg_id=call.message.message_id
    bot.edit_message_text(chat_id=chat_id,text='Введите сумму для перевода',message_id=msg_id)
    bot.register_next_step_handler(call.message,get_answer,text_src,text_target)
def get_answer(message: Message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text
    API_KEY = "0243b59c6a538b2dc46b7757"

    if text.startswith('/'):
        commands(message)
        return
    try:
        amount = float(text.replace(',', '').replace(' ', ''))

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{text_src}/{text_dest}/{amount}"
        response = requests.get(url).json()

        if response.get("result") == "success":
            converted = response["conversion_result"]
            rate = response["conversion_rate"]

            # форматируем числа с пробелами
            converted_fmt = f"{converted:,.2f}".replace(",", " ")
            amount_fmt = f"{amount:,.2f}".replace(",", " ")

            bot.send_message(
                chat_id,
                f"💱 {amount_fmt} {text_src} = {converted_fmt} {text_dest}\n📊 Курс: {rate} {text_dest}"
            )
            save_translate_data(chat_id, text, text_src, text_dest, converted_fmt)
        bot.send_message(chat_id, f'Введите еще сумму для перевода с {CURRENCY[text_src]} на {CURRENCY[text_dest]} или выберите другую команду')
        bot.register_next_step_handler(message, get_answer, text_src, text_dest)

    except ValueError:
        bot.send_message(chat_id, 'Введите корректную сумму!!!')
@bot.message_handler(content_types=['contact'])
def register_user(message:Message):
    chat_id=message.chat.id
    phone=message.contact.phone_number
    full_name=message.from_user.full_name
    username=message.from_user.username
    user=get_user(chat_id)
    if not user:
        save_info(username,full_name,phone,chat_id)
        bot.send_message(chat_id,'Регистрация прошла успешно🥳',reply_markup=ReplyKeyboardRemove())
        confirm_asc_src(message)
    else:
        confirm_asc_src(message)
    if message.text=='Ассаламу алейкум':
        bot.send_message(chat_id,'Ваалейкум Ассалам')

bot.infinity_polling()