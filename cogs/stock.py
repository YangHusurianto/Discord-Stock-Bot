import discord
import os
import requests
import pandas as pd
import typing
import neocities
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from utils import tickerCheck as tc
from chart import createChart as cc
from editChart import chartEdit as ce
from tokens import neocitiesToken as nc
from tokens import apiKey



headers = {
	'Content-Type': 'application/json'
}

stockOption = { '-c', '-v', '-r', '-d', '-i' } #Possible stock options
ALPHA_API_KEY = apiKey['alpha'] #Grabs api keys
TIINGO_API_KEY = apiKey['tiingo']
FINN_API_KEY = apiKey['finn']

nc = neocities.NeoCities('stonkman', nc)

class stock(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['stonk']) #Establishes the 'stock' command with alias 'stonk'
	async def stock(self, ctx, ticker: typing.Optional[str] = 'invalid', *args): #ticker -> stock option to search, args -> return modifiers
		url = tc(ticker) #Returns the NASDAQ URL of the ticker

		if ticker == 'help': #Establishes a help command
			embedHelp = discord.Embed(
				title = 'Stonk Man Help Become More Debt',
				color = 0xff0000,
				url = 'https://cdn.discordapp.com/attachments/736458386316460053/737478279577206865/unknown.png'
			)
			embedHelp.add_field(name = 'Basic Command Format', value = '`$stock [ticker] [-v] [-d] [-r] [-c] [-i]`', inline = False)
			embedHelp.add_field(name = 'Ticker', value = 'The stock symbol used to uniquely identify publicly traded shares', inline = False)
			embedHelp.add_field(name = '-v', value = 'Verbose details that include adjusted prices of the supplied ticker', inline = False)
			embedHelp.add_field(name = '-d', value = 'A description of the supplied ticker', inline = False)
			embedHelp.add_field(name = '-r', value = 'Realtime pricing of the supplied ticker', inline = False)
			embedHelp.add_field(name = '-c', value = 'Customizeable candlestick graph spanning four months of the supplied ticker', inline = False)
			embedHelp.add_field(name = '-i', value = 'Interactive customizeable candlestick graph spanning four months of the supplied ticker', inline = False)
			return await ctx.send(embed = embedHelp)

		if url == 'invalid': #Return message if ticker not found in NYSE, NASDAQ, or AMEX
			return await ctx.send('Invalid Ticker')
		url = url[:8] + url [12:] #Strip the url of the old status

		content = requests.get(f'https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={TIINGO_API_KEY}', headers = headers).json()[0] #Grab api data
		metaData = requests.get(f'https://api.tiingo.com/tiingo/daily/{ticker}?token={TIINGO_API_KEY}', headers = headers).json()
		realtime = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={FINN_API_KEY}').json()
		chart = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_API_KEY}').json()['Time Series (Daily)']
		prevDay = datetime.strptime(f'{content["date"][:10]}', '%Y-%m-%d').replace(tzinfo = timezone.utc).strftime('%a %b %d %Y') #Gets date of closing
		day = datetime.now().astimezone(timezone(timedelta(hours = -7), 'US/Arizona')).strftime('%a %b %d %Y %X %Z%z')
		embedVar = discord.Embed( ##Creates base stock embed for editing and upload
			title = f'{metaData["name"]} ({metaData["exchangeCode"]}:{metaData["ticker"]})',
			color = 0xcf3ab4,
			url = f'{url}'
		)

		if len(args) > 0: #Verifies if applied modifier exists
			if not args[0] in stockOption:
				return await ctx.send('Invalid modifier')

		realtimes = False #Establishes what modifiers were used
		charts = False
		interactive = False
		verboseOpt = False

		if '-r' in args:
			realtimes = True
		if '-c' in args:
			charts = True
		if '-i' in args:
			interactive = True
		if '-v' in args:
			verboseOpt = True

		if len(args) == 0 and not realtimes or verboseOpt and verboseOpt != realtimes: #Base stock details
			embedVar.add_field(name = 'Date', value = f'{prevDay}', inline = False)
			embedVar.add_field(name = 'Open', value = f'{content["open"]}', inline = False)
			embedVar.add_field(name = 'High', value = f'{content["high"]}', inline = False)
			embedVar.add_field(name = 'Low', value = f'{content["low"]}', inline = False)
			embedVar.add_field(name = 'Close', value = f'{content["close"]}', inline = False)

		elif verboseOpt and realtimes: #Return if verbose and realtime chosen; returned data is similar
			return await ctx.send('Cannot send verbose and realtime data simultaneously')

		if realtimes: #Realtime stock details
			embedVar.add_field(name = 'Date', value = f'{day}', inline = False)
			embedVar.add_field(name = 'Close', value = f'{realtime["c"]}', inline = False)
			embedVar.add_field(name = 'Low', value = f'{realtime["l"]}', inline = False)
			embedVar.add_field(name = 'High', value = f'{realtime["h"]}', inline = False)
			embedVar.add_field(name = 'Open', value = f'{realtime["o"]}', inline = False)

		if verboseOpt and not realtimes: #Verbose details of adjusted stock prices
			embedVar.add_field(name = 'Adj. Open', value = f'{content["adjOpen"]}', inline = False)
			embedVar.add_field(name = 'Adj. High', value = f'{content["adjHigh"]}', inline = False)
			embedVar.add_field(name = 'Adj. Low', value = f'{content["adjLow"]}', inline = False)
			embedVar.add_field(name = 'Adj. Close', value = f'{content["adjClose"]}', inline = False)

		if '-d' in args: #Description of ticker
			embedVar.add_field(name = 'Description', value = f'{metaData["description"]}', inline = False)

		userId = 0
		pageColor = None;
		if charts or interactive: #Establishes chart for upload
			chartReturns = cc(ctx, chart, metaData, ticker, charts, interactive)
			userId = chartReturns[0]
			pageColor = chartReturns[1]
		chartMade = interactive or charts

		if len(args) == 1 and not chartMade or len(args) > 1 and not (interactive and charts) or len(args) == 0: #Determins if embed details should be sent
			await ctx.send(embed = embedVar)

		if interactive: #Embed with link to chart
			file = discord.File(f'./charts/{userId}/{ticker.upper()}-Info.html', filename = f'{ticker.upper()}-Info.html')
			ce(f'./charts/{userId}/{ticker.upper()}-Info.html', pageColor)
			nc.upload((f'./charts/{userId}/{ticker.upper()}-Info.html', f'/{userId}/{ticker.upper()}-Info.html'))
			embedLink = discord.Embed(
				title = 'Stonk Man Show Debt',
				color = 0x336699,
				url = f'https://stonkman.neocities.org/{userId}/{ticker.upper()}-Info.html'
			)
			await ctx.send(embed = embedLink)

		if charts: #Uploads chart to Discord
			file = discord.File('./plot.png', filename = f'{ticker.upper()}-Chart.png')
			embedVar.set_image(url = 'attachment://chart.png')
			await ctx.send(file = file)

def setup(client):
	client.add_cog(stock(client))