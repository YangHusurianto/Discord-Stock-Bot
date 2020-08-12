from bs4 import BeautifulSoup

def chartEdit(file, rgb): #Edit chart to implemenet page background color editing
	with open(file) as f:
		soup = BeautifulSoup(f, features = 'html.parser')
		style = soup.new_tag('style')
		style.string = 'body{background:' + rgb + ';}.bk{margin:0 auto !important;}'
		soup.head.insert_before(style)
		with open(file, 'w') as out:
			out.write(str(soup))