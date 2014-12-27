'''
comput regression with updated vectors
'''
import numpy as np

class StreamRegression:
    '''
    class that update observations and get online estimate (Note: assume all inputs are centered)
    '''
    def __init__ (self, dim, y_dim = 1, lam = [0]):
        '''
        Constructor
        
        Parameters:
        ------------------------------------------------------
        dim:   dimension of the model, number of variables to be fitted
        y_dim: dimension of the response
        lam:   list of ridge factor penalty
        '''
        self.mDim    = dim
        self.mYDim   = y_dim
        self.mCoef   = np.zeros([dim, y_dim])
        self.mCount  = 0
        self.mXX     = np.zeros([dim, dim])
        self.mLambda = lam
        self.mXY     = np.zeros([dim, y_dim])

    def GetCoef (self):
        '''
        return the current estimated coefficients
        '''
        self.coef = [self._Solve(item) for item in self.mLambda]
        return self.coef
    
    def GerRidge (self):
        '''
        return the ridge factor
        '''
        return self.mLambda
    
    def Predict (self, observation):
        '''
        prediction on future values
        '''
        if not self.coef:
            self.GetCoef()
        return np.dot(observation, self.coef)

    def SetCoef (self, coef):
        '''
        coefficients feeded from outside
        '''
        self.coef = coef

    def _Solve (self, ridge_factor):
        '''
        try to solve and given None result if failed
        '''
        try:
            res = np.linalg.solve(self.mXX + ridge_factor * np.identity(self.mDim), self.mXY) 
        except:
            print "solve failed for {}".format(ridge_factor)
            return None
        return res
               
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

if __name__ == "__main__":
    col = 1
    design   = np.random.randn(100, 10) * 3
    coef = np.random.uniform(-2, 2, 10 * col).reshape(10, col)
    response = np.dot(design, coef) + np.random.rand(100, col)
    regression = StreamRegression(10, col, [0, 0.1])
    for i in range(design.shape[0]):
        regression.Update(design[i,:], response[i, :])
    print regression.GetCoef()
    print np.linalg.solve(np.dot(design.T, design), np.dot(design.T, response))
    print coef

