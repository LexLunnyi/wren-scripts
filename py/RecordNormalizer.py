import statistics

import pymongo
from bson import ObjectId


def get_db():
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    return myclient["wren"]


def get_data(recordId):
    mydb = get_db()
    mycol = mydb["samples"]
    myquery = {"recordId": recordId}
    return mycol.find(myquery)


def map_ecg(data):
    return data['sourceEcg']


def get_statistics(data):
    median = statistics.median(data)
    sub = data[2000:]
    minVal = min(sub)
    maxVal = max(sub)
    return minVal, maxVal, median


def normalize():
    mydb = get_db()
    record_collection = mydb["records"]
    sample_collection = mydb["samples"]
    #records = list(record_collection.find({"_id": ObjectId("6153514dacc3347ef02e78f7")}))
    records = list(record_collection.find({}))
    index = 0
    for record in records:
        data = list(get_data(record['_id']));
        source_ecg_data = map(map_ecg, data)
        min, max, median = get_statistics(list(source_ecg_data))
        index += 1
        print(str(index) + ")" + str(record['_id']) + " -> " + str(median))
        for sample in data:
            old_ecg = sample["sourceEcg"]
            ecg = old_ecg - median
            if old_ecg < min or old_ecg > max:
                ecg = 0
            query = {"_id": sample["_id"]}
            update = {"$set": {"ecg": ecg}}
            sample_collection.find_one_and_update(query, update, upsert=True)

        query = {"_id": record['_id']}
        update = {"$set": {"sourceEcgMedian": median}}
        record_collection.find_one_and_update(query, update, upsert=True)
