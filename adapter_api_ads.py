import requests
import json
import pandas as pd

class AdapterApiAds:
    def __init__(self, api_token, is_localhost):
        self.token = "&access_token=" + api_token
        self.url = 'https://api-thiago-alves' + self.token
        self.is_localhost = is_localhost

    def get_ads_status(self):
        if self.is_localhost:
            with open("data/data-ads.json") as file:
                return json.load(file)
        else:
            url = self.url + "/ads"
            data = requests.get(url + self.token)
            return json.loads(data._content.decode("utf-8"))
    
    def get_ad_set_status(self):
        if self.is_localhost:
            with open("data/data-ads-sets.json") as file:
                return json.load(file)
        else:
            url = self.url + "/ad-sets"
            data = requests.get(url + self.token)
            return json.loads(data._content.decode("utf-8"))

    def get_campaigns_status(self):
        if self.is_localhost:
            with open("data/data-campaigns.json") as file:
                return json.load(file)
        else:
            url = self.url + "/campaigns"
            data = requests.get(url + self.token)
            return json.loads(data._content.decode("utf-8"))

if __name__ == "__main__":
    api_token = open("environments/api_token").read()
    is_localhost = open("environments/is_localhost").read()

    api_ads = AdapterApiAds(api_token, is_localhost)

    api_ads.get_campaigns_status()
    api_ads.get_ads_status()
    api_ads.get_ad_set_status()
