import discord
from discord.ext import commands

class help(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['aid', 'assist'])
	async def help(self, ctx): #Overrides default help command
		embedHelp = discord.Embed(
				title = "Stonk Man Govt. Aid",
				color = 0x6666ff,
				url = "https://cdn.discordapp.com/attachments/736458386316460053/737478279577206865/unknown.png"
			);
		embedHelp.add_field(name = "Basic Command Format", value = "`$stock help`\n`$search help`\n`$customize help`", inline = False)
		await ctx.send(embed = embedHelp)


def setup(client):
	client.add_cog(help(client))