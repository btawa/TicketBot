from discord.ext import tasks, commands
import requests
import json
import logging

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkPATickets.start()

    @tasks.loop(seconds=30.0)
    async def checkPATickets(self):
        url = "https://checkout.square.site/app/store/api/v18/editor/users/140496054/sites/788572668991732904/products/1317?include=images,options,modifiers,category,media_files,fulfillment"
        data = json.loads(requests.get(url).text)['data']

        logging.info(f"OOS Badge: {data['badges']['out_of_stock']}, Total: {data['inventory']['total']}")

        channels = []

        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name == "dev":
                    channels.append(channel)

        if data['badges']['out_of_stock'] is False:
            tickets_available = data['inventory']['total']
            for channel in channels:
                await channel.send(f"There may be {tickets_available} tickets available to PA Re-raise\nhttps://checkout.square.site/buy/SETUC3BOVOYJINH2NKV4D5HT")

