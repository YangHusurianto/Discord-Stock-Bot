from discord.ext import commands
from nightlyCleanup import scheduleWipe as sw

class systemCheck(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self): #On startup print online statement and establish nightly wipe scheduler
		print('Bot online')
		sw()

	@commands.command()
	async def ping(self, ctx): #Command to check bot availability and response time
		await ctx.send(f'Pong!\n{round(ctx.bot.latency * 1000)}ms')

def setup(client):
	client.add_cog(systemCheck(client))