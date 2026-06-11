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
# STICKY REFRESH LOOP (NEW SYSTEM)
# -------------------------
async def sticky_loop():
    await client.wait_until_ready()

    global sticky_message_id
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("Channel not found")
        return

    while not client.is_closed():
        try:
            # delete old sticky if it exists
            if sticky_message_id:
                try:
                    old = await channel.fetch_message(sticky_message_id)
                    await old.delete()
                except:
                    pass

            # send new sticky
            msg = await channel.send(STICKY_TEXT)
            sticky_message_id = msg.id

        except Exception as e:
            print("Sticky loop error:", e)

        await asyncio.sleep(60)  # refresh every minute


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(sticky_loop())


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    asyncio.create_task(delete_later(message))


client.run(os.environ["TOKEN"])
