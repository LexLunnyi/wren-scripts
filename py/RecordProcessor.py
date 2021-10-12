from pathlib import Path
from ecgdetectors import Detectors
from matplotlib import pyplot

from RajaSelvaraj import RajaSelvaraj


class RecordProcessor(object):
    def __init__(self, record_name, record_type, sample_rate, samples):
        self.__record_name = record_name
        self.__record_type = record_type
        self.__sample_rate = sample_rate
        self.__samples = samples
        Path(record_type).mkdir(parents=True, exist_ok=True)
        self.__record_dir = record_type + "/" + record_name
        Path(self.__record_dir).mkdir(parents=True, exist_ok=True)

    def __get_ritms(self, r_peaks):
        res = []
        index = 0
        prev = 0;
        for cur in r_peaks:
            if index == 0:
                prev = cur
                index += 1
                continue
            cur = r_peaks[index]
            diff = cur - prev
            res.append(diff)
            index += 1
            prev = cur
        return res

    def __save_ritmogram(self, prefix, r_peaks):
        rr = self.__get_ritms(r_peaks)
        names = list(range(len(rr)))
        pyplot.bar(names, rr)
        pyplot.savefig(self.__record_dir + "/" + prefix + ".png")
        pyplot.clf()

    def __get_peaks(self):
        peaks = []
        detectors = Detectors(self.__sample_rate)

        r_peaks = detectors.pan_tompkins_detector(self.__samples);
        self.__save_ritmogram("pan_tompkins", r_peaks)
        peaks.append([])
        peaks[0].extend(r_peaks)

        r_peaks = detectors.swt_detector(self.__samples);
        self.__save_ritmogram("swt", r_peaks)
        peaks.append([])
        peaks[1].extend(r_peaks)

        r_peaks = detectors.engzee_detector(self.__samples);
        self.__save_ritmogram("engzee", r_peaks)
        peaks.append([])
        peaks[2].extend(r_peaks)

        r_peaks = detectors.hamilton_detector(self.__samples);
        self.__save_ritmogram("hamilton", r_peaks)
        peaks.append([])
        peaks[3].extend(r_peaks)

        r_peaks = detectors.christov_detector(self.__samples);
        self.__save_ritmogram("christov", r_peaks)
        peaks.append([])
        peaks[4].extend(r_peaks)

        r_peaks = detectors.two_average_detector(self.__samples);
        self.__save_ritmogram("two_average", r_peaks)
        peaks.append([])
        peaks[5].extend(r_peaks)

        selvaraj_detector = RajaSelvaraj(self.__samples, self.__sample_rate)
        r_peaks = selvaraj_detector.get()
        self.__save_ritmogram("raja", r_peaks)
        peaks.append([])
        peaks[6].extend(r_peaks)

        return peaks


    def save(self):
        peaks = self.__get_peaks()
        text_file = open(self.__record_dir + "/samples.csv", "w")
        index = 0
        pan_tompkins_index = 0
        swt_index = 0
        engzee_index = 0
        hamilton_index = 0
        christov_index = 0
        two_average_index = 0
        selvaraj_index = 1

        text_file.write("ecg,pan_tompkins,swt,engzee,hamilton,christov,two_average,selvaraj\n")

        for sample in self.__samples:
            row = str(sample) + ","

            if pan_tompkins_index < len(peaks[0]) and (index == peaks[0][pan_tompkins_index]):
                pan_tompkins_index += 1
                row += "3000,"
            else:
                row += "0,"

            if swt_index < len(peaks[1]) and (index == peaks[1][swt_index]):
                swt_index += 1
                row += "3000,"
            else:
                row += "0,"

            if engzee_index < len(peaks[2]) and (index == peaks[2][engzee_index]):
                engzee_index += 1
                row += "3000,"
            else:
                row += "0,"

            if hamilton_index < len(peaks[3]) and (index == peaks[3][hamilton_index]):
                hamilton_index += 1
                row += "3000,"
            else:
                row += "0,"

            if christov_index < len(peaks[4]) and (index == peaks[4][christov_index]):
                christov_index += 1
                row += "3000,"
            else:
                row += "0,"

            if two_average_index < len(peaks[5]) and (index == peaks[5][two_average_index]):
                two_average_index += 1
                row += "3000,"
            else:
                row += "0,"

            if selvaraj_index < len(peaks[6]) and (index == peaks[6][selvaraj_index]):
                selvaraj_index += 1
                row += "3000\n"
            else:
                row += "0\n"

            text_file.write(row)
            index += 1

        text_file.close()


