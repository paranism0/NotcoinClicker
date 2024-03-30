from loadSettings import Settings
from click import Click
from getWebViewResultUrl import WebViewProcess

settings = Settings()
webview = WebViewProcess(settings.API_ID , settings.API_HASH , settings.PHONE_NUMBER , settings.ACCOUNT_PWD)
clicker = Click(webview, settings.ScorePerClick , settings.ClickNumber)
clicker.Authenticate()
clicker.startBrowser()
clicker.click()