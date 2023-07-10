import telebot
import sqlite3
import openai

# Конфигурация Telegram бота
bot_token = '6332185362:AAG5weQqjaCUPtjGp_bbwDTIwIprQdCLLKc'
bot = telebot.TeleBot(bot_token)

# Конфигурация OpenAI API
openai.api_key = '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'

# Подключение к базе данных SQLite
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# Создание таблицы для хранения пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT
                )''')
conn.commit()

# Функция для получения количества аудитории
def get_audience_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    return count

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Добавление пользователя в базу данных
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    cursor.execute("INSERT INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                   (user_id, username, first_name, last_name))
    conn.commit()
    
    bot.reply_to(message, 'Привет! Я здесь, чтобы предоставить тебе психологическую поддержку.')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Добавьте здесь код обработки текстовых сообщений с использованием OpenAI API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message.text,
        temperature=0.7,
        max_tokens=50
    )
    reply = response.choices[0].text.strip()
    
    bot.reply_to(message, reply)

# Обработчик команды /audience
@bot.message_handler(commands=['audience'])
def audience(message):
    count = get_audience_count()
    bot.reply_to(message, f"Количество аудитории: {count}")

# Обработчик команды /add_ad
@bot.message_handler(commands=['add_ad'])
def add_ad(message):
    # Добавьте здесь логику добавления рекламы
    bot.reply_to(message, 'Реклама успешно добавлена')

# Обработчик команды /manage_content
@bot.message_handler(commands=['manage_content'])
def manage_content(message):
    # Добавьте здесь логику управления контентом
    bot.reply_to(message, 'Административная панель управления контентом')

# Запуск Telegram бота
bot.polling()
