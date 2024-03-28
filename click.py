from requests import session
from json import dumps , loads
from urllib.parse import unquote
from selenium import webdriver
from random import randint
from base64 import b64decode
from time import sleep
from sys import exit
from traceback import format_exc
from math import ceil

def decodeText(text : str):
    return b64decode(text.encode()).decode("utf-8" , "ignore")

class Click:
    def __init__(self , webAppData , ScorePerClick , ClickNumber , SleepTime):
        self.webAppData = webAppData
        self.webAppData2 = unquote(self.webAppData.split("=")[1].split("&")[0])
        self.ScorePerClick = ScorePerClick
        self.ClickNumber = ClickNumber
        self.SleepTime = SleepTime
        self.session = session()
        self.js_code = '''
            function requestComplete(response){
               console.log(response)
            };
            const method = "POST";
            const url = "https://clicker-api.joincommunity.xyz/clicker/core/click";
            var access_token = "%s";
            var hash = %i;
            var count = %i;
            var webAppData = "%s";
            var params = hash===-1 ? {"count": count, "webAppData": webAppData} : {"count": count, "webAppData": webAppData , "hash" : hash};
            var xhr = new XMLHttpRequest();
            xhr.open(method, url , false);
            xhr.setRequestHeader('Authorization', access_token);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.send(JSON.stringify(params));
            return xhr.response;
        '''
        self.headers = {
            "Content-Type" : "application/json",
            "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
            "X-Requested-With" : "org.telegram.messenger.web",
            "Sec-Ch-Ua" : '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "Sec-Ch-Ua-Platform" : '"Android"',
            "Origin" : "https://clicker.joincommunity.xyz" ,
            "Referer" : "https://clicker.joincommunity.xyz/"
        }
        self.session.headers.update(self.headers)
    def startBrowser(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.page_load_strategy = 'eager'
        self.browser = webdriver.Chrome(options = options)
        self.browser.get(self.webAppData)
    def Authenticate(self):
        self.session.post("https://plausible.joincommunity.xyz/api/event" , data = dumps({"n":"pageview","u":self.webAppData,"r":"null"}))
        getAuthCode = self.session.post("https://clicker-api.joincommunity.xyz/auth/webapp-session" , data = dumps({"webAppData" : self.webAppData2}))
        self.session.headers.update({"Authorization" :  "Bearer "+getAuthCode.json()["data"]["accessToken"]})
        self.getUserInfo()
    def getUserInfo(self):
        profile = self.session.get("https://clicker-api.joincommunity.xyz/clicker/profile")
        self.profile = profile.json()
        print(self.profile)
        self.multipleClicks = self.profile["data"][0]["multipleClicks"]
        self.lastAvailableCoins = self.profile["data"][0]["lastAvailableCoins"]
        self.miningPerTime = self.profile["data"][0]["miningPerTime"]
    def getFirstHash(self):
        result = self.browser.execute_script(self.js_code%(self.session.headers['Authorization'] , -1 , self.multipleClicks * randint(1,4) ,  self.webAppData2))
        result = loads(result)
        print(result)
        hash_code = result["data"][0]["hash"][0]
        self.lastAvailableCoins = result["data"][0]["lastAvailableCoins"]
        result_hash = self.browser.execute_script('''return %s'''%decodeText(hash_code))
        print(f"{decodeText(hash_code)} -> {result_hash}")
        return result_hash
    def getHashResult(self , previous_hash):
        scorePerClick = self.ScorePerClick + randint(10,50)
        scorePerClick -= scorePerClick%self.multipleClicks
        result = self.browser.execute_script(self.js_code%(self.session.headers['Authorization'] , previous_hash , scorePerClick ,  self.webAppData2))
        result = loads(result)
        print(result)
        hash_code = result["data"][0]["hash"][0]
        self.lastAvailableCoins = result["data"][0]["lastAvailableCoins"]
        result_hash = self.browser.execute_script('''return %s'''%decodeText(hash_code))
        print(f"{decodeText(hash_code)} -> {result_hash}")
        return (result , result_hash)
    def click(self):
        result_hash = self.getFirstHash()
        while 1:
            try:
                for _ in range(self.ClickNumber):
                    while True:
                        try:
                            result , result_hash = self.getHashResult(result_hash)
                            if self.lastAvailableCoins < self.ScorePerClick:
                                sleep(ceil((self.ScorePerClick - self.lastAvailableCoins)/4))
                            break
                        except:
                            self.Authenticate()
                            result_hash = self.getFirstHash()
                            sleep(1)
                    sleep(self.ScorePerClick//200)
                sleep(self.SleepTime)
            except KeyboardInterrupt:
                    print("exiting , closing browser")
                    self.browser.quit()
                    print("DONE[+]")
                    exit()
            except:
                print(format_exc())