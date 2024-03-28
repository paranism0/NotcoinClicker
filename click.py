from requests import session
from json import dumps , loads
from urllib.parse import unquote
from selenium import webdriver
from random import randint
from base64 import b64decode
from time import sleep
from sys import exit

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
        # options.add_argument("--headless=new")
        options.page_load_strategy = 'eager'
        self.browser = webdriver.Chrome(options = options)
        self.browser.get(self.webAppData)
    def getAuth(self):
        self.session.post("https://plausible.joincommunity.xyz/api/event" , data = dumps({"n":"pageview","u":self.webAppData,"r":"null"}))
        getAuthCode = self.session.post("https://clicker-api.joincommunity.xyz/auth/webapp-session" , data = dumps({"webAppData" : self.webAppData2}))
        self.session.headers.update({"Authorization" :  "Bearer "+getAuthCode.json()["data"]["accessToken"]})
    def getFirstHash(self):
        result = self.browser.execute_script(self.js_code%(self.session.headers['Authorization'] , -1 , 9 % randint(1,30) ,  self.webAppData2))
        result = loads(result)
        print(result)
        hash_code = result["data"][0]["hash"][0]
        return self.browser.execute_script('''return %s'''%decodeText(hash_code))
    def getHashResult(self , previous_hash):
        result = self.browser.execute_script(self.js_code%(self.session.headers['Authorization'] , previous_hash , self.ScorePerClick + randint(40,280) ,  self.webAppData2))
        result = loads(result)
        print(result)
        hash_code = result["data"][0]["hash"][0]
        result_hash = self.browser.execute_script('''return %s'''%decodeText(hash_code))
        return (result , result_hash)
    def click(self):
        result_hash = self.getFirstHash()
        while 1:
            for _ in range(self.ClickNumber):
                try:
                    result , result_hash = self.getHashResult(result_hash)
                    sleep(self.SleepTime)
                except KeyboardInterrupt:
                    print("exiting , closing browser")
                    self.browser.close()
                    self.browser.quit()
                    exit()
                    print("DONE[+]")
                except:
                    self.getAuth()
                    result_hash = self.getFirstHash()