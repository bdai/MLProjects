#!/usr/bin/python
'''
executable file to run regression
'''
import argparse
import cPickle
import numpy as np
import sys
import time

from lib.FileParser import FileParser

def SKFit (file_name, res_array, ridge, total, pickle_file):
    '''
    fit regression model with sklearn

    Parameters:
    --------------------------------------------
    file_name:   input file name
    res_array:   array of responses to be fitted, starting from 1
    ridge:       penalty to be taken in ridge regression
    total:       number of points to use
    frequency:   printing frequncy
    pickle_file: name of the file to store resutling coefficient
    '''
    from sklearn.linear_model import Ridge

    if not total:
        total = int(1000)
    ridge_obj = [Ridge(alpha = float(item)) for item in ridge]
    ### numpy array has size problem, using pandas may slow things down
    ## full_mat = np.genfromtxt(file_name, dtype = float, delimiter = ',', names = True)
    from pandas import read_csv
    full_mat = read_csv(file_name, delimiter = ',', nrows = total).values
    print full_mat.shape
    res_array = [item - 1 for item in res_array]
    response = full_mat[:, res_array]
    var_list = [i for i in range(full_mat.shape[1]) if i not in res_array]
    variable = full_mat[:, var_list]
    res_list = [Ridge(alpha = float(item), fit_intercept = False) for item in ridge]
    for item in res_list:
        item.fit(variable, response)
    res_list = [item.coef_.T for item in res_list]
    
    if pickle_file:
        output_file = open(pickle_file, 'w')
        cPickle.dump(res_list, output_file)
        output_file.close()
    else:
        print res_list
        print res_list[0].shape

def StreamFit (file_name, res_array, ridge, total, frequency, pickle_file):
    '''
    fit regression model with streaming

    Parameters:
    --------------------------------------------
    file_name:   input file name
    res_array:   array of responses to be fitted
    ridge:       penalty to be taken in ridge regression
    total:       number of points to use
    frequency:   printing frequncy
    pickle_file: name of the file to store resutling coefficient
    '''
    from Regression import StreamRegression

    file_reader = FileParser(file_name)
    ## read header
    names = file_reader.ReadLine()
    if not total:
        total = int(1e16)
    if len(names) - len(res_array) > total:
        print "WARNING: n({}) < p({}) problem!".format(total, len(names) - len(res_array))
    regression = StreamRegression.StreamRegression(len(names) - len(res_array), len(res_array), [float(item) for item in ridge])
    for count in range(total):
        if frequency and count % frequency == 0:
            print "Training iteration: {}".format(count)
        sample = file_reader.ReadLine(True)
        # WARN: res_array starts with 1
        response = [sample[item - 1] for item in res_array]
        variable = [i for j, i in enumerate(sample) if j + 1 not in res_array]
        regression.Update(np.array(variable, dtype = np.float), np.array(response, dtype = np.float))

    if pickle_file:
        output_file = open(pickle_file, 'w')
        cPickle.dump(regression.GetCoef(), output_file)
        output_file.close()
    else:
        print regression.GetCoef()
        print regression.GetCoef()[0].shape

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run ridge regression with different methods')
    parser.add_argument("data", help = "the csv format data file name for regression")
    parser.add_argument("type", help = "type of the regression, default 'stream'",
                        default = "stream")
    parser.add_argument("--total", help = "number of samples to be used for regression, default None", default = 0, type = int)
    parser.add_argument("--lam", help = "penalty of ridge regression, default 0", default = '0', nargs = '+')
    parser.add_argument("--responses", '-r', help = "columns to be used for regression", nargs = '+', default = [1], type = int)
    parser.add_argument("--freq", help = "print for every this many iterations, default not print", type = int, default = 0)
    parser.add_argument("--pickle", help = "pickle file name to store resulting coef", default = None)
    args = parser.parse_args()
    if args.type.startswith('stream'):
        StreamFit(args.data, args.responses, args.lam, args.total, args.freq, args.pickle)
    elif args.type.startswith('sklearn'): # use sklearn to fit
        SKFit(args.data, args.responses, args.lam, args.total, args.pickle)
    else:
        print "Unkown fitting method {}".format(args.type)
