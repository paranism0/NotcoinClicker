from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ScorePerClick : int
    ClickNumber : int
    webAppData : str

    class Config:
        env_file = '.env'