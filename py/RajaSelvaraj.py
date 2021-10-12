# https://biosignalsplux.com/learn/notebooks/Categories/Detect/r_peaks_rev.html

import biosignalsnotebooks as bsnb
from numpy import linspace, diff, zeros_like, arange, array, asarray
from matplotlib import pyplot


class RajaSelvaraj(object):
    def __init__(self, signal, sample_rate):
        self.__signal = asarray(signal)
        self.__sample_rate = sample_rate
        self.__filtered = bsnb.detect._ecg_band_pass_filter(signal, sample_rate)
        self.__differentiated = diff(self.__filtered)
        self.__squared = self.__differentiated * self.__differentiated
        nbr_sampls_int_wind = int(0.080 * self.__sample_rate)
        self.__integrated = zeros_like(self.__squared)
        cumulative_sum = self.__squared.cumsum()
        self.__integrated[nbr_sampls_int_wind:] = (cumulative_sum[nbr_sampls_int_wind:] -
                                                   cumulative_sum[:-nbr_sampls_int_wind]) / nbr_sampls_int_wind
        self.__integrated[:nbr_sampls_int_wind] = cumulative_sum[:nbr_sampls_int_wind] / arange(1,
                                                                                                nbr_sampls_int_wind + 1)
        rr_buffer, signal_peak_1, noise_peak_1, threshold = bsnb.detect._buffer_ini(self.__integrated, self.__sample_rate)
        probable_peaks, possible_peaks = bsnb.detect._detects_peaks(self.__integrated, self.__sample_rate)
        definitive_peaks = bsnb.detect._checkup(probable_peaks, self.__integrated, self.__sample_rate, rr_buffer, signal_peak_1, noise_peak_1, threshold)

        # Conversion to integer type.
        definitive_peaks = array(list(map(int, definitive_peaks)))
        map_integers = definitive_peaks - 40 * (self.__sample_rate / 1000)
        self.__definitive_peaks_reph = array(list(map(int, map_integers)))
        #The same as detected_peaks = bsnb.detect_r_peaks(signal, sr, time_units=True, plot_result=True)


    def get(self):
        return self.__definitive_peaks_reph

    def show(self):
        detected_peaks = bsnb.detect_r_peaks(self.__signal, self.__sample_rate, time_units=True, plot_result=True)
        # print(detected_peaks)
        pyplot.plot(self.__signal)
        print(self.__definitive_peaks_reph)
        pyplot.plot(self.__definitive_peaks_reph)
        # pyplot.plot(self.__squared)
        pyplot.show()
