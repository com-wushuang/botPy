from peewee import *

db = SqliteDatabase('advertisement.db')


class Advertisement(Model):
    key = CharField()
    introduction = TextField()
    content = TextField()

    class Meta:
        database = db


def list_ads():
    query = Advertisement.select()
    ads = []
    for item in query:
        ad = dict()
        ad['id'] = item.id
        ad['key'] = item.key
        ad['introduction'] = item.introduction
        ad['content'] = item.content
        ads.append(ad)
    return ads


def create_ad(obj):
    Advertisement.create(
        key=obj['key'],
        introduction=obj['introduction'],
        content=obj['content']
    )