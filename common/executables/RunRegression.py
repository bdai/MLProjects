#!/usr/bin/python
'''
executable file to run regression
'''
import argparse
import numpy as np
import StreamRegression

class FileParser:
    '''
    The class to parse the file line by line
    '''
    def __init__ (self, file_name = None):
        '''
        constructor to accept the file name of the csv training
        '''
        self.csv_file = file_name

    def ReadLine (self):
        '''
        return an observation
        ---------------------------
        @ret_list: two elements list, with 1st being response, 2nd being design
        '''
        return [np.array(5), np.array(6)]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help = "the csv format data file name for regression")
    parser.add_argument("type", help = "type of the regression, only stream supported",
                        default = "stream")
    parser.add_argument("--lambda", help = "penalty of ridge regression", default = '0.0001')
    parser.add_argument("--responses", '-r', help = "columns to be used for regression", nargs = '+', default = 1, type = int)
    args = parser.parse_args()
    print args
