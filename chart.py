import math
import os
import pandas as pd
from pymongo import MongoClient
from bokeh.plotting import figure, show, output_file, save
from bokeh.io import export_png
from bokeh.plotting import ColumnDataSource as cds
from bokeh.models import HoverTool, CDSView, BooleanFilter
from tokens import mongoToken as mT



mongoClient = MongoClient(f'mongodb://{mT["user"]}:{mT["token"]}@stockbotdatabase-shard-00-00.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-01.vvhns.mongodb.net:27017,stockbotdatabase-shard-00-02.vvhns.mongodb.net:27017/stockChartOptions?ssl=true&replicaSet=atlas-cjdcm4-shard-0&authSource=admin&retryWrites=true&w=majority') #Logs into MongoDB
db = mongoClient['stockChartOptions']
colorCollection = db['colors']

def createChart(ctx, chart, metaData, ticker, charts, interactive):
	df = pd.DataFrame.from_dict(chart, orient='index')  #Creates a Pandas DataFrame from the chart data retrieved from AlphaVantage
	df = df.reset_index() #Flattens all levels of the DataFrame
	df = df.rename(index={str:str}, columns={'index': 'date', '1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'}) #Renames DataFrame columns
	df['date'] = pd.to_datetime(df['date']) #Sets DataFrame date to datetime format and sorts
	df = df.sort_values(by=['date']) 
	df.open = df.open.astype(float) #Sets data to proper type
	df.close = df.close.astype(float) 
	df.high = df.high.astype(float) 
	df.low = df.low.astype(float) 
	source = cds(data = df.to_dict(orient = 'list')) #Sets the source to a copy of the DataFrame as a kaColumnDataSource 
	inc = df.close > df.open #Determins if the close was higher or lower than the open
	dec = df.open > df.close 
	view_inc = CDSView(source = source, filters = [BooleanFilter(inc)])
	view_dec = CDSView(source = source, filters = [BooleanFilter(dec)])
	w = 12 * 60 * 60 * 1000 #Sets width of bars
	colorOptions = None
	userId = 0
	if colorCollection.count_documents({ 'userId': ctx.author.id }): #Determines if a document exists for the userID, if not use default
		userId = ctx.author.id
	colorOptions = colorCollection.find({ 'userId': userId }).next()
	TOOLS = 'pan, wheel_zoom, box_zoom, hover, reset, save'
	title = metaData['exchangeCode'] + ':' + ticker.upper()

	candlestick = figure(x_axis_type = 'datetime', tools = TOOLS, plot_width = 1000, title = title, toolbar_location = None) #Creates the candlestick figure using Bokeh
	if interactive:
		candlestick.toolbar_location = 'right'
	candlestick.xaxis.major_label_orientation = math.pi / 4
	candlestick.grid.grid_line_alpha = 0.3
	candlestick.segment(x0='date', y0='high', x1='date', y1='low', color = colorOptions['segmentColor'], source=source)
	candlestick.vbar(x = 'date', width = w, top = 'open', bottom = 'close', fill_color = colorOptions['fillColorSell'], line_color = colorOptions['lineColor'], name = 'price', view = view_inc, source = source)
	candlestick.vbar(x = 'date', width = w, top = 'open', bottom = 'close', fill_color = colorOptions['fillColorBuy'], line_color = colorOptions['lineColor'], name = 'price', view = view_dec, source = source)
	candlestick.background_fill_color = colorOptions['backgroundColor']
	candlestick.border_fill_color = colorOptions['borderColor']
	candlestick.outline_line_color = colorOptions['outlineColor']
	candlestick.title.text_color = colorOptions['textColor']
	candlestick.yaxis.major_label_text_color = colorOptions['labelColor']
	candlestick.xaxis.major_label_text_color = colorOptions['labelColor']

	priceHover = candlestick.select(dict(type = HoverTool)) #Establishes hover tooltip formatting and data
	priceHover.names = ['price']
	priceHover.tooltips = [('Date', '@date{%Y-%m-%d}'),
							('Open', '@open{$0, 0.00}'),
							('Close', '@close{$0, 0.00}')]
	priceHover.formatters = {'@date' : 'datetime'}

	if charts: #If charts option selected, export chart as png for upload
		export_png(candlestick, filename = 'plot.png')

	if interactive: #If interactive, save chart as html file for upload to NeoCities
		if not os.path.isdir('./charts/'):
			os.mkdir('./charts/')
		if not os.path.isdir(f'./charts/{userId}'):
			os.mkdir(f'./charts/{userId}')
		output_file(f'./charts/{userId}\\{ticker.upper()}-Info.html', title = title)
		save(candlestick)
		
	return (userId, colorOptions['pageColor']) #Return the userId and the color choice