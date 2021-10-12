import os
from pathlib import Path
import pymongo
import re
from matplotlib import pyplot
from scipy import signal


def get_db():
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    return myclient["wren"]

def get_recor_id(name):
    mydb = get_db()
    mycol = mydb["records"]
    rgx = re.compile('.*' + name + '.*', re.IGNORECASE)
    myquery = {"path": rgx}
    rec = mycol.find(myquery)[0]
    return rec["_id"]#, rec["leti_r_detected"]


def get_data(recordId):
    mydb = get_db()
    mycol = mydb["samples"]
    myquery = {"recordId": recordId}
    return mycol.find(myquery)


def map_ecg(data):
    return data['ecg']


def map_pcg(data):
    return data['sourcePcg']*3000


def map_rrs(data):
    return data['rrs']


def map_qrs(data):
    if data['leti_r_detected']:
        return data['ecg'] * 1.3
    else:
        return 0


def get_qrs_points(data):
    x = []
    y = []
    index = 0
    for sample in data:
        if sample['leti_r_detected']:
            x.append(index)
            y.append(sample['ecg'])
        index += 1
    return x, y


def show_ecg(name):
    id = get_recor_id(name)
    data = list(get_data(id))
    ecg = list(map(map_ecg, data))
    pcg = list(map(map_pcg, data))
    #qrs = list(map(map_qrs, data))

    #if detected:
    x_qrs, y_qrs = get_qrs_points(data)

    #filter 60 Hz
    b, a = signal.iirnotch(60, 30, 2000)
    filtered_ecg = signal.lfilter(b, a, ecg)

    pyplot.plot(ecg)
    pyplot.plot(filtered_ecg)
    pyplot.plot(pcg)
    #pyplot.plot(qrs)
    #if detected:
    pyplot.plot(x_qrs, y_qrs, 'o', color='black');
    pyplot.show()


def extract_name(path):
    return os.path.basename(path).split(".")[0]


def export_ritmograms(dir, query):
    Path(dir).mkdir(parents=True, exist_ok=True)
    mydb = get_db()
    mycol = mydb["records"]
    records = list(mycol.find(query))
    for record in records:
        name = extract_name(record['path'])
        names = list(range(len(record['rrs'])))
        pyplot.bar(names, record['rrs'])
        pyplot.savefig(dir + "/" + name + ".png")
        pyplot.clf()

