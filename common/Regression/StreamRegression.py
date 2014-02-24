'''
comput regression with updated vectors
'''
import numpy as np

class StreamRegression:
    '''
    class that update observations and get online estimate
    '''
    def __init__ (self, dim, y_dim = 1, lam = 0.001):
        self.mDim   = dim
        self.mYDim  = y_dim
        self.mCoef  = np.zeros([dim, y_dim])
        self.mCount = 0
        self.mXX    = np.zeros([dim, dim])
        for i in range(dim):
            self.mXX[i, i] = lam
        self.mXY = np.zeros([dim, y_dim])

    def Update (self, observation, response):
        '''
        update internal strcture by observation and response
        '''
        observation = observation.reshape(1, self.mDim)
        response = response.reshape(1, self.mYDim)
        self.mXX += np.dot(observation.T, observation)
        tmp_xy = np.dot(observation.T, response)
        tmp_xy.reshape(self.mDim, self.mYDim)
        self.mXY = self.mXY + tmp_xy
        self.mCount += 1
        self.coef = None

    def GetCoef (self):
        '''
        return the current estimated coefficients
        '''
        self.coef = np.linalg.solve(self.mXX, self.mXY)
        return self.coef
    
    def Predict (self, observation):
        '''
        prediction on future values
        '''
        if not self.coef:
            self.GetCoef()
        return np.dot(observation, self.coef)

if __name__ == "__main__":
    col = 1
    design   = np.random.randn(100, 10) * 3
    coef = np.random.uniform(-2, 2, 10 * col).reshape(10, col)
    response = np.dot(design, coef) + np.random.rand(100, col)
    regression = StreamRegression(10, col)
    for i in range(design.shape[0]):
        print "sample %d" % (i + 1,)
        regression.Update(design[i,:], response[i, :])
    print regression.GetCoef()
    print np.linalg.solve(np.dot(design.T, design), np.dot(design.T, response))
    print coef

