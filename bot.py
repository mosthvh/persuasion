import discord
import asyncio
import os

CHANNEL_ID = 1513832206941028443
STICKY_TEXT = "📌 Anything sent in this channel will auto delete in 5 minutes :)"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sticky_message_id = None


# -------------------------
# DELETE MESSAGES AFTER 5 MINUTES
# -------------------------
async def delete_later(msg):
    await asyncio.sleep(300)
    try:
        await msg.delete()
    except:
        pass


# -------------------------
# CREATE OR UPDATE STICKY MESSAGE
# -------------------------
async def update_sticky(channel):
    global sticky_message_id

    # If sticky exists → edit it (NO spam)
    if sticky_message_id:
        try:
            msg = await channel.fetch_message(sticky_message_id)
            await msg.edit(content=STICKY_TEXT)
            return
        except:
            pass

    # If it doesn't exist → create it
    msg = await channel.send(STICKY_TEXT)
    sticky_message_id = msg.id


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await update_sticky(channel)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    # delete user message after 5 min
    asyncio.create_task(delete_later(message))

    # ensure sticky stays at bottom (without spam)
    await update_sticky(message.channel)


client.run(os.environ["TOKEN"])
