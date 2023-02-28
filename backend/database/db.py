from sqlalchemy import create_engine, Column, String, JSON, INTEGER
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import dotenv_values

Base = declarative_base()
config = dotenv_values()


class User(Base):
    __tablename__ = "users"

    uuid = Column("uuid", String, primary_key=True)
    name = Column("name", String)
    email = Column("email", String)
    picture = Column("picture", String)
    analyzed_videos = Column("analyzed_videos", INTEGER)

    def __init__(self, uuid, name, email, picture, analyzed_videos=0):
        self.uuid = uuid
        self.name = name
        self.email = email
        self.picture = picture
        self.analyzed_videos = analyzed_videos


class Video(Base):
    __tablename__ = "videos"

    video_id = Column("video_id", String, primary_key=True)
    sentiment = Column("sentiment", JSON)
    no_of_comments = Column("no_of_comments", INTEGER)

    def __init__(self, video_id, sentiment, no_of_comments) -> None:
        self.video_id = video_id
        self.sentiment = sentiment
        self.no_of_comments = no_of_comments


# TODO change to os.environ
engine = create_engine(
    "postgresql://{}:{}@database/{}".format(
        config["DB_USER"], config["DB_PASSWORD"], config["DB"]
    ),
    echo=True,
    future=True,
)


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()
