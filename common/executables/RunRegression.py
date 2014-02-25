#!/usr/bin/python
'''
executable file to run regression
'''
import argparse
import numpy as np
import StreamRegression
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

def Fit (file_name, method, res_array, ridge, total):
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
    if not (total is None):
        total = int(1000)
    for count in range(total):
        sample = file_reader.ReadLine(True)
        print sample


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help = "the csv format data file name for regression")
    parser.add_argument("type", help = "type of the regression, only stream supported",
                        default = "stream")
    parser.add_argument("--total", help = "number of samples to be used for regression, default None", default = None)
    parser.add_argument("--lam", help = "penalty of ridge regression", default = '0.0001')
    parser.add_argument("--responses", '-r', help = "columns to be used for regression", nargs = '+', default = 1, type = int)
    args = parser.parse_args()
    try:
        Fit(args.data, args.type, args.responses, args.lam, args.total)
    except:
        print time.ctime(), "fitting error occured, code {}".format(sys.exc_info()[0])
