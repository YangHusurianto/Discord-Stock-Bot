import discord
import requests
import typing
import re
from discord.ext import commands
from tokens import apiKey

ALPHA_API_KEY = apiKey['alpha']
TIINGO_API_KEY = apiKey['tiingo']

headers = {
	'Content-Type': 'application/json'
}

class search(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def search(self, ctx, *args): #Search command with multiple keywords argumetn
		if len(args) == 0:
			return await ctx.send('Invalid Search Term')
		keywords = None

		if len(args) > 1: #Encodes spaces for the link
			keywords = "%20".join(args)
		else:
			keywords = args[0]

		if keywords == 'help': #Help command for search
			embedHelp = discord.Embed(
				title = "Stonk Man Teach To Search For Debt",
				color = 0xee55ee,
				url = 'https://cdn.discordapp.com/attachments/736458386316460053/737634420089159792/ktda12tnnjd41.png'
			)
			embedHelp.add_field(name = "Basic Command Format", value = "`$search [keywords]`", inline = False)
			embedHelp.add_field(name = "Keywords", value = "One or more keywords pertaining to the search", inline = False)
			return await ctx.send(embed = embedHelp)

		searchResult = requests.get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={ALPHA_API_KEY}").json() #Return search results
		embedSearch = discord.Embed(
			title = "Stonk Man Help Search For Debt",
			color = 0xbb33bb,
			url = "https://cdn.discordapp.com/attachments/736458386316460053/737629298864685067/4f5.png"
		)
		tickerOne = searchResult['bestMatches'][0]['1. symbol']
		tickerTwo = searchResult['bestMatches'][1]['1. symbol']
		tickerThree = searchResult['bestMatches'][2]['1. symbol']
		metaDataOne = requests.get(f"https://api.tiingo.com/tiingo/daily/{tickerOne}?token={TIINGO_API_KEY}", headers = headers).json()['description']
		metaDataTwo = requests.get(f"https://api.tiingo.com/tiingo/daily/{tickerTwo}?token={TIINGO_API_KEY}", headers = headers).json()['description']
		metaDataThree = requests.get(f"https://api.tiingo.com/tiingo/daily/{tickerThree}?token={TIINGO_API_KEY}", headers = headers).json()['description']
		lengthOne = 256 if len(metaDataOne) > 256 else len(metaDataOne)
		lengthTwo = 256 if len(metaDataTwo) > 256 else len(metaDataTwo)
		lengthThree = 256 if len(metaDataThree) > 256 else len(metaDataThree)
		embedSearch.add_field(name = f"1. {searchResult['bestMatches'][0]['2. name']} ({tickerOne})", value = f"{metaDataOne[:lengthOne]}...", inline = False) #Add top three search results to embed
		embedSearch.add_field(name = f"2. {searchResult['bestMatches'][1]['2. name']} ({tickerTwo})", value = f"{metaDataTwo[:lengthTwo]}...", inline = False)
		embedSearch.add_field(name = f"3. {searchResult['bestMatches'][2]['2. name']} ({tickerThree})", value = f"{metaDataThree[:lengthThree]}...", inline = False)
		embedSearch.add_field(name = "For more information", value = "`$stock [ticker] -d`", inline = False)
		return await ctx.send(embed = embedSearch)

def setup(client):
	client.add_cog(search(client))