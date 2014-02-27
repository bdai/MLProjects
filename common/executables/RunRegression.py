#!/usr/bin/python
'''
executable file to run regression
'''
from Regression import StreamRegression

import argparse
import cPickle
import numpy as np
import sys
import time

class FileParser:
    '''
    The class to parse the file line by line
    '''
    def __init__ (self, file_name = None, separator = ','):
        '''
        constructor to accept the file name of the csv training
        '''
        try:
            self.csv_file = open(file_name, 'r')
        except:
            print "open file {} failed! error code {}".format(file_name, sys.exc_info()[0])
        self.sep = separator

    def ReadLine (self, convert = False):
        '''
        return a single observation

        Parameters:
        ----------------------------------------------------
        convert: whether to conver each element to double

        Returns:
        ---------------------------
        @ret_list: two elements list, with 1st being response, 2nd being design
        '''

        line = self.csv_file.readline().strip()
        if len(line) == 0:
            return None
        if convert:
            return [float(item) for item in line.split(self.sep)]
        else:
            return line.split(self.sep)

def Fit (file_name, method, res_array, ridge, total, frequency, pickle_file):
    '''
    main process of fitting the regression model

    Parameters:
    --------------------------------------------
    file_name: input file name
    method:    method of regression
    res_array: array of responses to be fitted
    ridge:     penalty to be taken in ridge regression

    Returns
    --------------------------------------------
    '''
    file_reader = FileParser(file_name)
    ## read header
    names = file_reader.ReadLine()
    if not total:
        total = int(1000)
    if len(names) - len(res_array) > total:
        print "WARNING: n < p problem!"
    regression = StreamRegression.StreamRegression(len(names) - len(res_array), len(res_array), [float(item) for item in ridge])
    for count in range(total):
        if count % frequency == 0:
            print "Training iteration: {}".format(count)
        sample = file_reader.ReadLine(True)
        response = [sample[item] for item in res_array]
        variable = [i for j, i in enumerate(sample) if j not in res_array]
        regression.Update(np.array(variable, dtype = np.float), np.array(response, dtype = np.float))

    if pickle_file:
        output_file = open(pickle_file, 'w')
        cPickle.dump(regression.GetCoef(), output_file)
        output_file.close()
    else:
        print regression.GetCoef()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help = "the csv format data file name for regression")
    parser.add_argument("type", help = "type of the regression, only stream supported",
                        default = "stream")
    parser.add_argument("--total", help = "number of samples to be used for regression, default None", default = 0, type = int)
    parser.add_argument("--lam", help = "penalty of ridge regression, default 0", default = '0', nargs = '+')
    parser.add_argument("--responses", '-r', help = "columns to be used for regression", nargs = '+', default = [1], type = int)
    parser.add_argument("--freq", help = "print for every this many iterations, default 100", type = int, default = 100)
    parser.add_argument("--pickle", help = "pickle file name to store resulting coef", default = None)
    args = parser.parse_args()
    Fit(args.data, args.type, args.responses, float(args.lam), args.total, args.freq, args.pickle)
