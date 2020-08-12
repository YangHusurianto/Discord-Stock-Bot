import discord
import typing
import re
from discord.ext import commands
from pymongo import MongoClient
from colorDict import cssColors
from customizationNames import customName, uiName
from tokens import mongoToken as mT



mongoClient = MongoClient(f'mongodb://{mT["user"]}:{mT["token"]}@stockbotdatabase-shard-00-00.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-01.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-02.vvhns.mongodb.net:27017/stockChartOptions?ssl=true&replicaSet=atlas-cjdcm4-shard-0&authSource=admin&retryWrites=true&w=majority') #Logs into MongoDB
db = mongoClient['stockChartOptions']
colorCollection = db['colors']

class customize(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['custom']) #Establishes the 'customize' command with alias 'custom'
	async def customize(self, ctx, tag: typing.Optional[str] = 'invalid', *arg): #tag -> chart property to edit, arg -> new chart property color
		if tag == 'invalid': 
			return await ctx.send('Use `$customize help` for more information or `$customize list` to view all customization options and their ids')

		if tag == 'help': #Establishes a help command
			embedHelp = discord.Embed(
				title = 'Stonk Man Help Debt Become Pretty',
				color = 0x11ff11,
				url = 'https://cdn.discordapp.com/attachments/736458386316460053/737477940165607475/unknown.png'
			)
			embedHelp.add_field(name = 'Basic Command Frmat', value = '`$customize [id] [color]`', inline = False)
			embedHelp.add_field(name = 'Id', value = 'The id of the customization option to modify. Use `$customize list` to see all ids', inline = False)
			embedHelp.add_field(name = 'Color', value = 'The color to use. Accepted colors: CSS, Hex, or RGB(A)', inline = False)
			embedHelp.add_field(name = 'CSS Example', value = 'Colors can be found at: www.w3schools.com/colors/colors_names.asp', inline = False)
			embedHelp.add_field(name = 'Hex Example', value = '#09AF32', inline = False)
			embedHelp.add_field(name = 'RGB(A) Example', value = '0-127-255 or 0,127,255', inline = False)
			return await ctx.send(embed = embedHelp)

		if tag == 'list':
			embedList = discord.Embed(
				title = 'Stonk Man Give Beauty Options',
				color = 0x66ff66,
				url = 'https://cdn.discordapp.com/attachments/736458386316460053/737478009568755762/unknown.png'
			)
			embedList.add_field(name = 'Segment Color (sc)', value = 'The color of the upper and lower quartiles of each data set', inline = False)
			embedList.add_field(name = 'Sell Fill Color (sfc)', value = 'The color of the middle quartiles of each data set where sells exceeded buys', inline = False)
			embedList.add_field(name = 'Buy Fill Color (bfc)', value = 'The color of the middle quartiles of each data set where buys exceeded sells', inline = False)
			embedList.add_field(name = 'Sell/Buy Border Color (sbbc)', value = 'The border color of the middle quartiles of each data set', inline = False)
			embedList.add_field(name = 'Background Color (bgc)', value = 'The color of the chart background', inline = False)
			embedList.add_field(name = 'Border Color (bc)', value = 'The color of the chart border', inline = False)
			embedList.add_field(name = 'Outline Color (oc)', value = 'The color of the chart outline', inline = False)
			embedList.add_field(name = 'Text Color (tc)', value = 'The color of the chart title', inline = False)
			embedList.add_field(name = 'Label Color (lc)', value = 'The color of the axis labels', inline = False)
			embedList.add_field(name = 'Page Color (pc)', value = 'The color of the page background', inline = False)
			return await ctx.send(embed = embedList)

		arg = args[0]
		if tag in { 'sc', 'sfc', 'bfc', 'sbbc', 'bgc', 'bc', 'oc', 'tc', 'lc', 'pc' }: #Verify valid tag
			if arg[:1].isnumeric(): 
				if '-' in arg:
					arg.replace('-', ', ')
				arg = arg + ' '
			isRgb = re.search(r'(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]), (1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]), (1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]) ', arg)

			if arg in cssColors or (re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', arg) and len(arg) > 4) or isRgb: #Verify valid color
				if isRgb:
					arg = f'rgb({arg.strip()})'
				customChoice = customName[tag]

				if colorCollection.count_documents({ 'userId': ctx.author.id }) == 0: #If user collection exists, modify, else create new
					colorOptions = { 'userId': ctx.author.id,
									 'segmentColor': 'white',
									 'fillColorSell': '#32E82C',
									 'fillColorBuy': '#F2583E',
									 'lineColor': 'white',
									 'backgroundColor': 'black', 
									 'borderColor': 'slategray',
									 'outlineColor': 'black',
									 'textColor': 'white',
									 'labelColor': 'white',
									 'pageColor': 'rgb(12, 12, 12)'
								    }
					colorOptions[customChoice] = arg
					colorCollection.insert_one(colorOptions)
				else:
					userOptions = colorCollection.find({ 'userId': ctx.author.id })
					changeColor = userOptions.next()
					changeColor[customChoice] = arg
					colorCollection.update_one({ 'userId': ctx.author.id}, { '$set': {f'{customChoice}': arg}})
				return await ctx.send(f'{uiName[tag]} changed to {arg} for {ctx.author.display_name}')

			else:
				return await ctx.send('Please enter a valid color')

		else:
			return await ctx.send('Please use a valid customization id')
		
def setup(client):
	client.add_cog(customize(client))