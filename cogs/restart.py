import os
from discord.ext import commands
from utils import ownerCheck

class restart(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.check(ownerCheck)
	async def restart(self, ctx): #Command to restart bot for owner ids only
		await ctx.message.delete()
		os.system('start python index.py') 
		await ctx.bot.logout()

def setup(client):
	client.add_cog(restart(client))