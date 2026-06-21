import discord
import requests
import asyncio
import winsound
import os

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = 1479770827061854298

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_weather = "STARTUP"


@client.event
async def on_ready():
    global last_weather

    print(f"Logged in as {client.user}")

    user = await client.fetch_user(USER_ID)

    try:
        await user.send("✅ Weather Bot is online and working!")
        print("Startup DM sent!")
    except Exception as e:
        print("DM error:", e)

    while True:
        try:
            data = requests.get(
                "https://api.growagarden2stock.com/weather"
            ).json()

            current = data["current"]

            if current is None:
                weather = None
            else:
                weather = current["weather_name"]

            if weather != last_weather:

                if weather is None:
                    print("☀️ No active weather")

                else:
                    message = (
                        f"🚨 WEATHER ALERT! 🚨\n\n"
                        f"Weather: {weather}\n"
                        f"Effect: {current['weather_effect']}"
                    )

                    print(message)

                    # Triple beep alarm
                    winsound.Beep(2000, 500)
                    winsound.Beep(2000, 500)
                    winsound.Beep(2000, 500)

                    try:
                        await user.send(message)
                        print("Weather DM sent!")
                    except Exception as e:
                        print("Weather DM error:", e)

                last_weather = weather

            await asyncio.sleep(30)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(30)


client.run(TOKEN)
