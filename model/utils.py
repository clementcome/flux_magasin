import numpy as np

def norm(vect):
    '''
    Returns the norm of a vector
    :param vect: (list or array) Vector
    :return: (float) Norm of the vector
    '''
    return np.sqrt(vect[0]**2+vect[1]**2)