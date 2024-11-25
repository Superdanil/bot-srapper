from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    # ==========TELEGRAM==========
    BOT_TOKEN: str
    RANDOM_LINKS_COUNT: int
    MAX_DEPTH: int

    # ==========POSTGRES==========
    DB_URL: str
    ECHO: bool

    # ==========LOGGING==========
    LOGFILE: str
    ROTATION: str
    COMPRESSION: str


settings = Settings()
