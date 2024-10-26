import telebot
import json
import requests


bot = telebot.TeleBot('', parse_mode=None)
API = ''

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'ЙОУ, {message.from_user.first_name}')

@bot.message_handler(commands=['mypfp'])
def send_profile_photo(message):
    user_id = message.from_user.id

    photos = bot.get_user_profile_photos(user_id)

    if photos.total_count > 0:
        first_photo = photos.photos[0] 
        highest_resolution_photo = first_photo[-1] 
        bot.send_photo(message.chat.id, highest_resolution_photo.file_id)
    else:
        bot.send_message(message.chat.id, 'У вас нет аватарки.')



@bot.message_handler(commands=['map'])
def send_map(message):
    try:
        floor = int(message.text.split()[1])  

        
        if floor == 1:
            photo = open('1floor.png', 'rb') 
        elif floor == 2:
            photo = open('2floor.png', 'rb')  
        elif floor == 3:
            photo = open('3floor.png', 'rb') 
        else:
            bot.send_message(message.chat.id, 'Этаж указан неверно. Введите 1, 2 или 3.')
            return

        bot.send_photo(message.chat.id, photo)
        photo.close()

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, 'Пожалуйста, укажите этаж после команды, например: /map 1')


@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        city = message.text.split()[1].strip().lower()

        req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = json.loads(req.text)


        if req.status_code == 200 and 'main' in data:
            temp = data["main"]["temp"]
            bot.reply_to(message, f'Погода в {city.title()}: {temp} градусов Цельсия')
            image = 'SUNNY.png' if temp > 5.0 else 'cold.jpg'
            file = open('./' + image, 'rb')
            bot.send_photo(message.chat.id, file)
        else:
            error_message = data.get("message", "Не удалось получить данные о погоде.")
            bot.reply_to(message, f'Ошибка: {error_message}')
    
    except IndexError:
        bot.reply_to(message, 'Пожалуйста, укажите город после команды /weather, например: /weather Москва')
    
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка при обработке запроса.')



@bot.message_handler(commands=['aboutme'])
def main(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['site', 'website', 'madi'])
def site(message):
    bot.send_message(
        message.chat.id, 
        "Вот ссылка на мой сайт: <a href='https://akiyam1.github.io/updatedportfolio'>ссылка</a>", 
        parse_mode='HTML'
    )



@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'ЙОУ, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Id: {message.from_user.id}')


bot.polling(none_stop=True)
