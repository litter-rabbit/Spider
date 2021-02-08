from redis import StrictRedis
import pymongo


def get_redis_conn(db):
    return StrictRedis(
        host='127.0.0.1',
        port=6379,
        db=db
    )


def get_mongodb():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["app_store"]
    return mydb["appData"]


if __name__ == '__main__':
    redis_conn = get_redis_conn(0)
    mongo_conn = get_mongodb()
