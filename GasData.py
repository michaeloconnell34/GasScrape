import requests

import time
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime,timedelta
import pandas as pd
from io import StringIO

#datetime works exactly like it looks. It's just minused one day.

yesterday = datetime.now() - timedelta(1)

#Take yesterdays date and format it, these are called f-strings. So here, the code is formatting the data so it can be read by the server coherently. It takes the yesterday variable, and truncates everything but the day, then takes the yesterday variable again, and truncates the month, then again with the year.
yesterday_date = f'{yesterday.strftime("%d")}-{yesterday.strftime("%B")[:3]}-{yesterday.strftime("%Y")}'
# https://www.tutorialspoint.com/python/time_time.htm#:~:text=%20Python%20time%20time%20%28%29%20Method%20%201,usage%20of%20time%20%28%29%20method.%20%20More%20 You can read more about it here. If there was one module for you to understand how to use, this would be it.

#Simple enough, just enclose the url of where your trying to go in string qoutation marks like so ""
original_url = "https://noms.wei-pipeline.com/reports/ci_report/launch.php?menuitem=2600315"

# This one is a bit weird, so urlparse takes the url we gave it, and splits each part of the web address up into parts. This has something to do with how a computer talks to a server. Regardless, you will need this step every time you do a scrape.

parsed = urlparse.urlparse(original_url)

#target_url is harder to find. So basically, go to the website you want to scrape. Go to inspect, and go under the tab named network. Now, run your search (you need to query the database in order to find where the link is right?). You should see some stuff pop up under that network tab. So first things first. There will be two files, and a gif. The first one is your requests url. Copy everything up until .php. That is your target_url.

# When you see the stream report, double click on it and a tab should open called headers. Take the stuff only up till it ends with .php. That's your stream_report_url. Again, all this stuff is in the headers tab.

target_url = "https://noms.wei-pipeline.com/reports/ci_report/server/request.php"
stream_report_url = "https://noms.wei-pipeline.com/reports/ci_report/server/streamReport.php"

# Now, we are going to use a python library called requests. I don't overly understand how it works but we really don't need to. It's nerd shit about how servers talk to each other. So, we start a session (meaning we will begin communicating)

s = requests.Session()
# We load the original URL so that we have website permissions. 

# load the cookies. We need to do this because if we don't the server doesn't know who we are. 
s.get(original_url)

#get id
r = s.post(target_url,
	params = {
		"request.preventCache": int(round(time.time() * 1000))
	},
	data = {
		"ReportProc": "CIPR_DAILY_BULLETIN",
		"p_ci_id": parse_qs(parsed.query)['menuitem'][0],
		"p_opun": "PL",
		"p_gas_day_from": yesterday_date,
		"p_gas_day_to": yesterday_date,
		"p_output_option": "CSV"
})
r = s.get(stream_report_url, params = r.json())




data = pd.read_csv(StringIO(r.text))
data.to_csv("example2.csv")
print("Completo Bro-dero")



