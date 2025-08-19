import os
import requests


def GetAllSolidesPontos():
    headerAPIKey = {
        "Authorization":f"Basic {os.getenv("APIKEY_SOLIDES")}"
    }
    url = "https://apis.tangerino.com.br/punch/summary?justClosed=true&size=200"
    resp = requests.get(url , headers=headerAPIKey)
    data = resp.json()
    return data["content"]
 
def GetAllSolidesFunc():
    headerAPIKey = {
        "Authorization":f"Basic {os.getenv("APIKEY_SOLIDES")}"
    }
    # url = "https://employer.tangerino.com.br/employee/find-all?size=180"
    url = "https://employer.tangerino.com.br/employee/find-all?size=143"
    resp = requests.get(url , headers=headerAPIKey)
    data = resp.json()
    
    
    dic = {u["id"]:u["name"] for u in data["content"]}
    return dic