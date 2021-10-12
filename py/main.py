import glob

import pymongo
import os

import samplerate
from bson import ObjectId
from matplotlib import pyplot
from scipy.io.wavfile import write

import RecordNormalizer
import RecordsVisualizator
from RecordProcessor import RecordProcessor
from RajaSelvaraj import RajaSelvaraj
import numpy
from scipy import signal
import RR_loader


def get_data(recordId):
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    mydb = myclient["wren"]
    mycol = mydb["samples"]
    myquery = {"recordId": recordId}
    return mycol.find(myquery)


def get_ecg(data):
    return data['ecg']


def get_recors():
    myclient = pymongo.MongoClient(
        "mongodb://localhost/wren?connectTimeoutMS=30000&socketTimeoutMS=30000&waitQueueMultiple=100")
    mydb = myclient["wren"]
    mycol = mydb["records"]
    myquery = {"type": "HEA_ECG_PCG"}
    return list(mycol.find(myquery))




if __name__ == '__main__':
    #RecordsVisualizator.show_ecg("a0112")
    #RecordsVisualizator.show_ecg("a0362")
    #RecordNormalizer.normalize()



    #RecordsVisualizator.show_ecg("a0005")
    #RecordsVisualizator.show_ecg("a0034")
    #RecordsVisualizator.show_ecg("a0312")
    #RecordsVisualizator.show_ecg("a0377")

    RecordsVisualizator.show_ecg("a0074")
    #RecordsVisualizator.show_ecg("a0267")


    #RecordsVisualizator.export_ritmograms("abnormal_detected", {"$and": [{"normal": False}, {"leti_r_detected": True}]})




# DETECT R-PEAKS
# if __name__ == '__main__':
#     records = get_recors()
#     for record in records:
#         # record_proc = RecordProcessor(os.path.basename(record["path"]), rtype, record["sampleRate"], ecg)
#         # record_proc.save()



# LOAD RR FILES FROM R_DETECTOR
# if __name__ == '__main__':
#     os.chdir("RRs")
#     for file in glob.glob("*.RR"):
#         name = file.split(".")[0]
#         RR_loader.parse(name)


# #LOAD ECG, FILTER 60HZ, RESAMPLE, AND CONVERT TO WAV
# if __name__ == '__main__':
#     records = get_recors()
#     for record in records:
#         data = list(get_data(record["_id"]))
#         ecg = list(map(get_ecg, data))
#         rtype = "normal" if record["normal"] else "ubnormal"
#         #filter 60 Hz
#         b, a = signal.iirnotch(60, 30, 2000)
#         filtered_ecg = signal.lfilter(b, a, ecg)
#         #resample
#         ratio = 0.5
#         converter = 'sinc_best'  # or 'sinc_fastest', ...
#         resampled_ecg = samplerate.resample(filtered_ecg, ratio, converter)
#         #save
#         record_name = os.path.basename(record["path"]).split(".")[0]
#         write("/home/aberdnikov/study/RDetector/" + record_name + ".wav", 1000, resampled_ecg.astype(numpy.int16))
#         print(record_name + ".wav")


