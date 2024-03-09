import configparser
import requests
import telegram
import time
import asyncio

# Function to fetch weather forecast from OpenWeatherMap
def get_weather_forecast(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather forecast for today: {weather_description}. Temperature: {temperature}°C"
    else:
        return "Failed to fetch weather forecast"

# Function to send message to Telegram channel
async def send_message_to_telegram(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)

# Main function
async def main():
    # Load API keys from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    owm_api_key = config['API_KEYS']['owm_api_key']
    telegram_bot_token = config['API_KEYS']['telegram_bot_token']
    channel_id = config['API_KEYS']['channel_id']
    city = config['SETTINGS']['city']
    
    
    tg_bot = telegram.Bot(token=telegram_bot_token)
    
    await send_message_to_telegram(tg_bot, channel_id, "Weather forecast bot started")
    while True:
        weather_forecast = get_weather_forecast(owm_api_key, city)
        await send_message_to_telegram(tg_bot, channel_id, weather_forecast)
        await asyncio.sleep(3600)  # Fetch and send weather forecast every hour

if __name__ == "__main__":
    asyncio.run(main())