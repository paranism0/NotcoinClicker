from loadSettings import Settings
from click import Click

settings = Settings()
clicker = Click(settings.webAppData , settings.ScorePerClick , settings.ClickNumber)
clicker.Authenticate()
clicker.startBrowser()
clicker.click()