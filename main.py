from telebot import TeleBot
from telebot.types import Message,CallbackQuery,ReplyKeyboardRemove
import os
from dotenv import load_dotenv
from buttons import currency_btn,contact_btn,main_menu,events_buttons,news_button
import requests
from base_curse import get_history,save_translate_data,get_user,save_info
from news import get_news,get_bussines_news,get_economy_news,get_university_news
from weather_info import weather_info
load_dotenv()
token=os.getenv('TOKEN')
bot=TeleBot(token)
@bot.message_handler(commands=['start', 'help', 'about', 'history'])
def commands(message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.username
    user = get_user(chat_id)

    if not user:
        bot.send_message(chat_id, f'👋🏻 Здравствуйте, {user_name}!\n🤖 Вас приветствует информативный бот по курсам валют и новостям ')
        bot.send_message(chat_id, '📲 Для использования бота пройдите регистрацию, нажав кнопку ниже 👇', reply_markup=contact_btn())
    else:
        bot.send_message(chat_id, '📍 Выберите из меню, что вы желаете 💼', reply_markup=main_menu())

@bot.message_handler(content_types=['contact'])
def register_user(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    full_name = message.from_user.full_name
    username = message.from_user.username

    user = get_user(chat_id)
    if not user:
        save_info(username, full_name, phone, chat_id)
        bot.send_message(chat_id, '✅ Регистрация прошла успешно! 🥳\n🔁 Нажмите /start для начала работы с ботом', reply_markup=ReplyKeyboardRemove())

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
#-----------------------------------Курсы Валют-------------------------------------
@bot.message_handler(regexp='📈 Курсы валют')
def reaction_convercy(message:Message):
    chat_id = message.chat.id
    msg_id =message.message_id
    bot.delete_message(chat_id,msg_id)
    bot.send_message(chat_id,'Вы выбрали курсы валют 💱"',reply_markup=ReplyKeyboardRemove())
    confirm_asc_src(message)
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
        commands(message)

    except ValueError:
        bot.send_message(chat_id, 'Введите корректную сумму!!!')
#---------------------------------------------------------------------------
#--------------------------Погода-------------------------------------------
@bot.message_handler(regexp='⛅ Погода')
def reaction_weather(message:Message):
    chat_id = message.chat.id
    msg_id =message.message_id
    bot.delete_message(chat_id,msg_id)
    bot.send_message(chat_id,'Вы выбрали ⛅ Погода"',reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id,'Укажите название города чтобы узнать погоду🤔')
    bot.register_next_step_handler(message,get_country)
def get_country(message:Message):
    chat_id = message.chat.id
    city=message.text.strip()
    try:
        weather=weather_info(city)
        bot.send_message(chat_id,weather,reply_markup=main_menu())
    except:
        bot.send_message(chat_id,'Укажите корректный город!!!')
#-----------------------------------------------------------------
#-------------------------Раздел новости-----------------------------------------
@bot.message_handler(regexp='📰 Новости')
def reaction_news(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел новостей', reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id,'🛠Выберите какой тип новостей вас интересует',reply_markup=news_button())
@bot.message_handler(regexp='📰 Экономика')
def reaction_convercy(message:Message):
    chat_id = message.chat.id
    msg_id =message.message_id
    bot.delete_message(chat_id,msg_id)
    bot.send_message(chat_id,'Вы выбрали новости 📰 Экономики"',reply_markup=ReplyKeyboardRemove())
    get_ec_news(message)
def get_ec_news(message:Message):
    chat_id = message.chat.id
    news = get_economy_news()
    for new in news:
        news_text = f'📰 Заголовок: {new["title"]}\n📌 Описание: {new["content"]}\n📅 Дата: {new["data_time"]}\n🖼 Фото: {new["photo"]}\n🔗 Подробнее: {new["url"]}'
        bot.send_message(chat_id, news_text, reply_markup=main_menu())
@bot.message_handler(regexp='📚 Новости — Обучение')
def reaction_news(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел 📚 Новости — Обучение', reply_markup=ReplyKeyboardRemove())
    confirm_news(message)
def confirm_news(message: Message):
    chat_id = message.chat.id
    lst_news = get_news()
    for new in lst_news:
        news_text = f'📰 Заголовок: {new["title"]}\n📌 Описание: {new["content"]}\n📅 Дата: {new["data_time"]}\n🖼 Фото: {new["photo"]}\n🔗 Подробнее: {new["url"]}'
        bot.send_message(chat_id, news_text, reply_markup=main_menu())
@bot.message_handler(regexp='💼 Бизнес')
def reaction_news(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел 💼 Бизнес', reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id,'💵 Вот вам последние новости в бизнесе')
    send_bs_news(message)
def send_bs_news(message:Message):
    chat_id = message.chat.id
    news=get_bussines_news()
    for new in news:
        news_text = f'📰 Заголовок: {new["title"]}\n📌 Описание: {new["content"]}\n📅 Дата: {new["data_time"]}\n🖼 Фото: {new["photo"]}\n🔗 Подробнее: {new["url"]}'
        bot.send_message(chat_id,news_text,reply_markup=main_menu())
@bot.message_handler(regexp='🎓 Новости нашего универа')
def reaction_news(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел 🎓 Новости нашего универа', reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id,'🎓 Вот вам последние новости нашего универа')
    send_univer_news(message)
def send_univer_news(message:Message):
    chat_id = message.chat.id
    news=get_university_news()
    for new in news:
        news_text = f'📰 Заголовок: {new["title"]}\n📌 Описание: {new["content"]}\n🖼 Фото: {new["photo"]}\n🔗 Подробнее: {new["url"]}'
        bot.send_message(chat_id,news_text,reply_markup=main_menu())
#-----------------------------------------------------------------------------------------------
#-------------------------------Ближайшие события-----------------------------------------------
@bot.message_handler(regexp='📅 Ближайшие события')
def get_events(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел 📅 Ближайшие события', reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id,'🛠 Вот раздел ближащих событий что вас интересует',reply_markup=events_buttons())
@bot.message_handler(regexp='🎤 Концерты / музыка')
def send_movie(message:Message):
    chat_id = message.chat.id
    msg_id = message.message_id
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, '📢 «Вы открыли раздел 🎬 Кинопремьеры / кино', reply_markup=ReplyKeyboardRemove())

#-----------------------------------------------------------------------------------------------

bot.infinity_polling()