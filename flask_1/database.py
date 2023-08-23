from sqlalchemy import Table, Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

ModelBase = declarative_base()

post_tags = Table('post_tags', ModelBase.metadata,
    Column('post_id', Integer, ForeignKey('posts.post_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'), primary_key=True)
)

engine = create_engine("sqlite:///blog.db", echo=False)

Session = sessionmaker(bind=engine)