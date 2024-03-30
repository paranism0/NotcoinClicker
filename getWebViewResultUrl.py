from pyrogram import Client
from pyrogram.raw.types import InputPeerUser
from pyrogram.raw.functions.messages import RequestWebView

class WebViewProcess:
    def __init__(self , api_id , api_hash , phoneNumber , password):
        self.client = Client(name = "session" , 
            api_id = api_id , 
            api_hash = api_hash , 
            phone_number = phoneNumber ,
            password = password
        )
        self.webUrl = "https://clicker.joincommunity.xyz/clicker"
        self.client.start()
        self.peerUser = self.client.resolve_peer(self.client.get_users("notcoin_bot").id)
    def getWebViewUrl(self):
        result = self.client.invoke(
            RequestWebView(
                bot = self.peerUser ,
                peer = self.peerUser ,
                platform = "android" ,
                url = self.webUrl ,
                from_bot_menu=True
            )
        )
        return result.url