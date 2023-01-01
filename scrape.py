import urllib.request
from bs4 import BeautifulSoup
import re
import ssl

def getapidata(word):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	prompt = word.replace(" ","_").lower()
	prompt.title()

	url = f"https://en.wikipedia.com/wiki/{prompt}"

	try:
		fhandle = urllib.request.urlopen(url, context=ctx)
		htmlParse = BeautifulSoup(fhandle, 'html.parser')
		summary = htmlParse.find_all("p")[1].get_text()
		if len(summary.strip())==0:
			summary = htmlParse.find_all("p")[2].get_text()
		summary = str(re.sub(r'[^A-Za-z .]+', '', summary))
		return summary
	except:
		return ""