import discord
import asyncio
import os

CHANNEL_ID = 123456789012345678  # Replace with your channel ID

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == CHANNEL_ID:
        async def delete_later(msg):
            await asyncio.sleep(300)
            try:
                await msg.delete()
            except:
                pass

        asyncio.create_task(delete_later(message))

client.run(os.environ["TOKEN"])
