import csv
from pathlib import Path
import pymongo
import re


def load(file_name):
    data = []
    full_name = file_name + ".RR"
    rr_file = Path(full_name)
    if not rr_file.exists():
        return False, data

    with open(full_name) as tsv:
        for line in csv.reader(tsv, delimiter=" ", skipinitialspace=True):
            data.append(int(line[1]))

    return True, data


def back_resample(data, ratio):
    for idx, val in enumerate(data):
        data[idx] = val * ratio


def get_indices(data):
    indices = []
    prev = 0
    for rr in data:
        cur = prev + rr
        indices.append(cur)
        prev = cur
    return indices


def get_recor_id(name):
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    mydb = myclient["wren"]
    mycol = mydb["records"]
    rgx = re.compile('.*' + name + '.*', re.IGNORECASE)
    myquery = {"path": rgx}
    return mycol.find(myquery)[0]["_id"]


def update_record(id, rrs):
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    mydb = myclient["wren"]
    mycol = mydb["records"]
    mycol.update({"_id": id}, {"$set": {"leti_r_detected": True, "rrs": rrs}})


def update_samples(recordId, sampleNumbers):
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    mydb = myclient["wren"]
    mycol = mydb["samples"]
    mycol.update_many({"$and": [{"recordId": recordId}, {"sampleNumber": {"$in": sampleNumbers}}]},
                      {"$set": {"leti_r_detected": True}})
    mycol.update_many({"$and": [{"recordId": recordId}, {"sampleNumber": {"$nin": sampleNumbers}}]},
                      {"$set": {"leti_r_detected": False}})


def parse(name):
    res, data = load(name)
    if not res:
        return

    back_resample(data, 2)
    indices = get_indices(data)

    id = get_recor_id(name)
    update_record(id, data)
    update_samples(id, indices)
    print(name)
