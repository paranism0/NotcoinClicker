from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ScorePerClick : int
    ClickNumber : int
    SleepTime : int
    webAppData : str

    class Config:
        env_file = '.env'