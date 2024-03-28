from loadSettings import Settings
from click import Click

settings = Settings()
clicker = Click(settings.webAppData , settings.ScorePerClick , settings.ClickNumber , settings.SleepTime)
clicker.getAuth()
clicker.startBrowser()
clicker.click()