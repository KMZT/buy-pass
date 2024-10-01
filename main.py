import discord
import re

# Укажите ваш токен бота Discord
DISCORD_TOKEN = 'MTI5MDY4MzczMzExNjA1OTcxMQ.G9_eGH.OVlYx3H5f_erHo83ZZ6jPKa2jXRTR2n1-dbxA4'

# Инициализация бота
discord_client = discord.Client()

# Регулярное выражение для поиска ссылок
url_pattern = re.compile(r'https?://[^\s]+')

@discord_client.event
async def on_ready():
    print(f'Бот запущен как {discord_client.user}')

@discord_client.event
async def on_message(message):
    # Проверка, что сообщение не от бота
    if message.author == discord_client.user:
        return

    # Поиск ссылок в сообщении
    urls = url_pattern.findall(message.content)
    if urls:
        for url in urls:
            # Вывод ссылки в консоль
            print(f'Найдена ссылка: {url}')

# Запуск бота
discord_client.run(DISCORD_TOKEN)
