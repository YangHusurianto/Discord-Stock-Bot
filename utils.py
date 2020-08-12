from nyse import NYSE
from amex import AMEX
from nasdaq import NASDAQ
from etf import ETF
from pymongo import MongoClient
from tokens import mongoToken as mT



mongoClient = MongoClient(f'mongodb://{mT["user"]}:{mT["token"]}@stockbotdatabase-shard-00-00.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-01.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-02.vvhns.mongodb.net:27017/stockChartOptions?ssl=true&replicaSet=atlas-cjdcm4-shard-0&authSource=admin&retryWrites=true&w=majority') #Logs into MongoDB
db = mongoClient['serverOption']
ownerIds = db['ownerId']

def ownerCheck(ctx):
	serverCheck = ownerIds.count_documents({ 'serverId': ctx.guild.id })
	if serverCheck == None and ctx.author.id == 147869832275034112 or ctx.author.id == 168216897450541056:
		return true
	elif serverCheck == 0:
		serverData = { 'serverId': ctx.guild.id,
					   'ownerIds': [ 147869832275034112, 
					   				 168216897450541056,
					   				 ctx.guild.owner_id
					   			   ]
					  }
		ownerIds.insert_one(serverData)
	return ctx.author.id in ownerIds.find_one({ 'serverId': ctx.guild.id })["ownerIds"]

def tickerCheck(ticker):
	if ticker == 'invalid':
		return 'invalid'

	inNYSE = False
	inAMEX = False
	inNASDAQ = False
	inETF = False

	if ticker.upper() in NYSE:
		inNYSE = True
		return NYSE[ticker.upper()]

	if ticker.upper() in AMEX:
		inAMEX = True
		return AMEX[ticker.upper()]

	if ticker.upper() in NASDAQ:
		inNASDAQ = True
		return NASDAQ[ticker.upper()]

	if ticker.upper() in ETF:
		inETF = True
		return f'https://old.nasdaq.com/symbol/{ticker.upper()}'
		
	if not (inNYSE or inAMEX or inNASDAQ or inETF):
		return 'invalid'