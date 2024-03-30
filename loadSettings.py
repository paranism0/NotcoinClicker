from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_ID : int
    API_HASH : str
    PHONE_NUMBER : str
    ACCOUNT_PWD : str
    ScorePerClick : int
    ClickNumber : int

    class Config:
        env_file = '.env'