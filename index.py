import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from tokens import discordToken

client = commands.Bot(command_prefix = '$') #Prefix for all commands to use

client.remove_command('help') #Removes default help command

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		return await ctx.send('Stonk Command Not Found') #Error message to return to the user on invalid command

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}') #Load cog extensions

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}') #Unload cog extensions

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}') #On startup load all cog extensions.

client.run(discordToken)