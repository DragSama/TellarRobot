from apscheduler.schedulers.asyncio import AsyncIOScheduler
from TellarBot import client
from TellarBot.plugins.checker import handler
from TellarBot import BOTS_LIST, BOTS_CONFIG, LOG_CHANNEL

import asyncio
import logging

log_string = """
Username: @{username}
Status: {status}
Response Time: `{time}s`
Speed: **{speed}**
"""

class Manager:

    def __init__(self):

        self.config = BOTS_CONFIG
        self.bot_details = {}
        self.scheduler = scheduler = AsyncIOScheduler()
        self.jobs = {}
        for bot in BOTS_LIST:
            config = self.config[bot]
            username = config['username']
            self.bot_details[username] = {'username': username, 'status': 'UP', 'response_time': 0, 'slow': False, 'status_message': ''}
            self.jobs[bot] = self.scheduler.add_job(
                             handler,
                            'interval',
                             seconds = 5,
                             name = username,
                             kwargs = {
                                'client': client,
                                'bot': config['username'],
                                'key_name': bot,
                                'command': config.get('command', '/start')
                                }
                             )
        self.scheduler.start()

    async def get_status(self, bot):
        config = self.bot_details.get(bot, None)
        if not config:
            return False
        return config

    async def set_status(self, key_name, username, status, response_time = False):
        config = self.config[key_name]
        if status == "DOWN":
            self.bot_details[username]['status'], status = "DOWN", "DOWN"
            self.bot_details[username]['response_time'], response_time = 0, 0
            self.bot_details[username]['slow'], slow = False, False
        else:
            if response_time > config['avg_response_time']:
                logging.warning(f'{username} is slow, Time taken to respond: {response_time}')
                self.bot_details[username]['status'], status = "UP", "UP"
                self.bot_details[username]['response_time'], response_time = response_time, response_time
                self.bot_details[username]['slow'], slow = True, True
            else:
                logging.info(f"{username} is performing normally.")
                self.bot_details[username]['status'], status = "UP", "UP"
                self.bot_details[username]['response_time'], response_time = response_time, response_time
                self.bot_details[username]['slow'], slow = True, True
        if not self.bot_details[username]['status_message']:
            self.bot_details[username]['status_message'] = await client.send_message(LOG_CHANNEL, log_string.format(username = username, status = '❌' if status == "DOWN" else '✅', time = round(response_time, 2), speed = "Normal" if not slow else "Slow"))
        else:
            text = log_string.format(username = username, status = '❌' if status == "DOWN" else '✅', time = round(response_time, 2), speed = "Normal" if not slow else "Slow")
            message = self.bot_details[username]['status_message']
            if message.text == text:
                return
            await message.edit(text)
Manager = Manager()
