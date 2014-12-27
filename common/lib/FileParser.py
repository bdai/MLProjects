
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
    
