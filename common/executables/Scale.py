#!/usr/bin/python
'''
executable file to scale the columns of a csv file
'''
import argparse
from lib.FileParser import FileParser
import math

def RunScale (input_file, output_file, stat_file, total, frequency):
    if not total:
        total = 1e16
    ## first pass to calculate mean
    file_reader = FileParser(input_file)
    names = file_reader.ReadLine()
    mean = [float(0)] * len(names)
    std  = [float(0)] * len(names)
    count = 0
    line = file_reader.ReadLine(True)
    while line:
        if frequency and count % frequency == 0:
            print "Iteration calculation {}".format(count)
        count += 1
        for k, item in enumerate(line):
            mean[k] += item
            std[k] += item * item
        if count > total:
            break
        line = file_reader.ReadLine(True)
    mean = [item / count for item in mean]
    for i, item in enumerate(mean):
        std[i] = math.sqrt(std[i] / count - item * item)
    
    ## write output file
    output = open(output_file, 'w')
    output.write(','.join(names) + '\n')
    file_reader = FileParser(input_file)
    names = file_reader.ReadLine()
    line = file_reader.ReadLine(True)
    count = 0
    while line:
        if frequency and count % frequency == 0:
            print "Iteration for writing {}".format(count)
        count += 1
        corrected = [''] * len(names)
        for k, item in enumerate(line):
            corrected[k] = "%.6f" % ((item - mean[k]) / std[k])
        output.write(','.join(corrected) + '\n')
        line = file_reader.ReadLine(True)
        if count > total:
            break

    if stat_file:
        output_stat = open(stat_file, 'w')
        for i in range(len(mean)):
            output_stat.write("%s, %.6f, %.6f\n" % (names[i], mean[i], std[i]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'scale the columns of a csv file')
    parser.add_argument("data", help = "the csv format data file name for regression")
    parser.add_argument('stat', help = 'file to store scaled file')
    parser.add_argument('--total', help = 'total number of lines use', default = None, type = int)
    parser.add_argument('--freq', help = 'printing frequency, default no print', default = 0, type = int)
    parser.add_argument('--output', '-o', help = 'output file for row mean and std, default no print', default = None)
    args = parser.parse_args()
    
    RunScale(args.data, args.stat, args.output, args.total, args.freq)
