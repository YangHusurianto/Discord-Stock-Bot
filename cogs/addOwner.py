import discord
from discord.ext import commands
from pymongo import MongoClient
from utils import ownerCheck
from tokens import mongoToken as mT



mongoClient = MongoClient(f'mongodb://{mT["user"]}:{mT["token"]}@stockbotdatabase-shard-00-00.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-01.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-02.vvhns.mongodb.net:27017/stockChartOptions?ssl=true&replicaSet=atlas-cjdcm4-shard-0&authSource=admin&retryWrites=true&w=majority') #Logs into MongoDB
db = mongoClient['serverOption']
ownerIds = db['ownerId']

class addOwner(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['addowner'])
	@commands.check(ownerCheck)
	async def addOwner(self, ctx, member: discord.Member): #Command to add a bot owner
		if member.id in ownerIds.find_one({ 'serverId': ctx.guild.id })["ownerIds"]:
			await ctx.send('User already a bot owner')
		else:
			ownerIds.update({ 'serverId': ctx.guild.id }, { '$push': { 'ownerIds': member.id } })
			await ctx.send(f'{member} added as bot owner')

	@addOwner.error
	async def addOwnerError(ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('Invalid user')

def setup(client):
	client.add_cog(addOwner(client))