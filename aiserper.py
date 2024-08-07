import http.client
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) #os.environ["SERPER_API_KEY"]
def serper_search(query):
    """Perform a Serper search"""
    print(f"Using Serper for {query}")
    conn = http.client.HTTPSConnection("scrape.serper.dev")
    payload = json.dumps({
      "url": query
    })
    headers = {
      'X-API-KEY': os.environ["SERPER_API_KEY"],
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

# conn = http.client.HTTPSConnection("scrape.serper.dev")
# payload = json.dumps({
#   "url": "https://www.chittorgarh.com/report/mainboard-ipo-list-in-india-bse-nse/83/"
# })
# headers = {
#   'X-API-KEY': os.environ["SERPER_API_KEY"],
#   'Content-Type': 'application/json'
# }
# conn.request("POST", "/", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

#print(serper_search("https://www.chittorgarh.com/report/mainboard-ipo-list-in-india-bse-nse/83/"))
print(serper_search("https://en.wikipedia.org/wiki/Gandhi_Jayanti"))