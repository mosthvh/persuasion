import discord
import asyncio
import os

CHANNEL_ID = 1513832206941028443  # your channel ID
STICKY_TEXT = "📌 Anything sent in this channel will auto delete in 5 minutes : )"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sticky_message_id = None


# -------------------------
# DELETE USER MESSAGES AFTER 5 MINUTES (your original system)
# -------------------------
async def delete_later(msg):
    await asyncio.sleep(300)
    try:
        await msg.delete()
    except:
        pass


# -------------------------
# SEND / REFRESH STICKY MESSAGE
# -------------------------
async def send_sticky(channel):
    global sticky_message_id

    msg = await channel.send(STICKY_TEXT)
    sticky_message_id = msg.id


async def refresh_sticky(channel):
    global sticky_message_id

    # delete old sticky
    if sticky_message_id:
        try:
            old = await channel.fetch_message(sticky_message_id)
            await old.delete()
        except:
            pass

    # send new sticky
    await send_sticky(channel)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await send_sticky(channel)


@client.event
async def on_message(message):
    global sticky_message_id

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    # -------------------------
    # your original delete system
    # -------------------------
    asyncio.create_task(delete_later(message))

    # -------------------------
    # sticky message system
    # -------------------------
    await refresh_sticky(message.channel)


client.run(os.environ["TOKEN"])
