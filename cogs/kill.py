import discord
from discord.ext import commands
from utils import ownerCheck

class kill(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['shutdown', 'stop'])
	@commands.check(ownerCheck) 
	async def kill(self, ctx): #Command to kill bot for owner ids only
		await ctx.message.delete()
		embedKill = discord.Embed(
			title = "Stonks Are Dying",
			color = 0xff3333,
			url = "https://cdn.discordapp.com/attachments/736458386316460053/737788574833049721/americas-debt-ekists-34-64-5-32-84-54-54-64-95-48-5-95-32-58608941.png"
		)
		await ctx.send(embed = embedKill) #Reports that bot has been sh
		await ctx.bot.close()

def setup(client):
	client.add_cog(kill(client))