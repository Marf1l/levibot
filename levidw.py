import telebot
import hashlib
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os
from flask import Flask, request



# Создаем бота с твоим API токеном
bot = telebot.TeleBot("YOUR_API_TOKEN")

# Приветственное сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, "👋 Привет! Отправь мне ссылку на видео из TikTok, и я помогу тебе скачать его.\n")

# Словарь для хранения ссылок по их уникальным ключам
url_dict = {}

# Обработка сообщений с TikTok или YouTube ссылками
@bot.message_handler(func=lambda message: "tiktok.com" in message.text or "vm.tiktok.com" in message.text)
def handle_video_request(message: Message):
    url = message.text.strip()
    # Создаем уникальный хеш для ссылки
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]  # Берем первые 8 символов хеша для укороченного идентификатора
    url_dict[url_hash] = url  # Сохраняем соответствие хеш-ссылки
    
    bot.send_message(message.chat.id, "Выберите формат загрузки:", reply_markup=create_format_buttons(url_hash))

# Создание кнопок для выбора формата
def create_format_buttons(url_hash):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🎥 Видео", callback_data=f"video|{url_hash}"),
               InlineKeyboardButton("🎶 Аудио", callback_data=f"audio|{url_hash}"))
    return markup

# Обработка нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_format_selection(call):
    action, url_hash = call.data.split('|')
    url = url_dict.get(url_hash)  # Получаем оригинальную ссылку по хешу

    if not url:
        bot.answer_callback_query(call.id, "Ошибка: ссылка не найдена!")
        return

    bot.answer_callback_query(call.id)  # Подтверждаем нажатие кнопки сразу

    if action == "video":
        bot.send_message(call.message.chat.id, "⏳ Начинаю загрузку видео...")
        download_and_send_media(call.message.chat.id, url, media_type='video')
    elif action == "audio":
        bot.send_message(call.message.chat.id, "⏳ Начинаю загрузку аудио...")
        download_and_send_media(call.message.chat.id, url, media_type='audio')

# Загрузка и отправка медиа без использования ffmpeg
def download_and_send_media(chat_id, url, media_type='video'):
    # Генерируем уникальное имя файла на основе URL
    unique_filename = hashlib.md5(url.encode()).hexdigest()[:8]  # Первые 8 символов хеша
    
    if media_type == 'video':
        ydl_opts = {
            'format': 'best[ext=mp4]/best[ext=webm]',  # Выбираем одиночный видеофайл в mp4, если доступен
            'outtmpl': f'downloads/{unique_filename}.%(ext)s',
            'noplaylist': True,  # Отключаем скачивание плейлистов
            'quiet': True,  # Отключаем лишние сообщения в консоли
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Выбираем формат mp4 для видео
            }],
            'writethumbnail': False,  # Отключаем загрузку миниатюр
            'no_warnings': True,  # Отключаем предупреждения
            'merge_output_format': 'mp4',  # Объединение видео и аудио в формат mp4
            'extractor_args': {
                'tiktok': ['--no-watermark'],  # Отключение водяных знаков для TikTok
            },
        }
    else:  # media_type == 'audio'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'downloads/{unique_filename}.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        # Отправляем файл в чат
        with open(filename, 'rb') as file:
            if media_type == 'video':
                bot.send_video(chat_id, file, caption="🎥 Вот твое видео!")
            else:
                bot.send_audio(chat_id, file, caption="🎶 Вот твое аудио!")

        # Удаляем скачанный файл
        os.remove(filename)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Произошла ошибка: {str(e)}")

# Настроим Flask для приема webhook
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

if __name__ == "__main__":
    # Устанавливаем webhook
    bot.remove_webhook()  # Убираем старый webhook, если он был
    bot.set_webhook(url="https://levidw.fly.dev/webhook")  # Устанавливаем новый webhook

    # Запускаем Flask сервер
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
