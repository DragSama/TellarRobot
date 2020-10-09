import time
import logging
from TellarBot import client
from telethon.sync import events

async def handler(client, bot, key_name, command):
      async with client.conversation(bot) as conv:
          from TellarBot.plugins.classes import Manager
          await conv.send_message(command)
          s_time = time.time()
          try:
              await conv.get_response()
          except:
              await Manager.set_status(key_name, bot, 'DOWN')
              logging.critical(f'{bot} is down!')
              return
          response_time = time.time() - s_time
          await Manager.set_status(key_name, bot,"UP", response_time)

@client.on(events.NewMessage(pattern='.status ', outgoing = True))
async def status(event):
    from TellarBot.plugins.classes import Manager
    bot = await Manager.get_status(event.text.split(' ', 1)[1])
    logging.critical(f"{bot}, {event.text.split(' ', 1)[1]}")
    if not bot:
        return
    msg = f"Status: **{bot['status']}**\n"
    msg += f"Is Slow: **{bot['slow']}**\n"
    msg += f"Response Time: `{bot['response_time']}`"
    await event.reply(msg)

@client.on(events.NewMessage(pattern='.runtime', outgoing = True))
async def u(event):
      await event.reply('Uptime checker robot is running !')
