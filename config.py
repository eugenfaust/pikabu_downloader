from dataclasses import dataclass
from os import getenv


@dataclass
class DB:
    host: str
    db_name: str
    user: str
    password: str
    port: int = 5432

    def get_uri(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass
class Config:
    db: DB
    token: str
    admin_id: int
    channel_id: int
    sentry_dsn: str


def load_config():
    return Config(
        db=DB(host=getenv('DB_HOST'),
              db_name=getenv('DB_NAME'),
              user=getenv('DB_USER'),
              password=getenv('DB_PASS'),
              port=getenv('DB_PORT', 5432)),
        token=getenv('BOT_TOKEN'),
        admin_id=getenv('ADMIN_ID', 0),
        channel_id=getenv('CHANNEL_ID', 0),
        sentry_dsn=getenv('SENTRY_DSN'),
    )