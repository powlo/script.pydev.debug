import xbmc
import pydevd_file_utils
from functools import wraps
    
def xbmcfilenamedecorator(func):
    @wraps(func)
    def xbmcfilename(filename):
        filename = xbmc.translatePath(filename)
        return func(filename)
    return xbmcfilename

pydevd_file_utils._NormFile = xbmcfilenamedecorator(pydevd_file_utils._NormFile)
pydevd_file_utils.NormFileToServer = xbmcfilenamedecorator(pydevd_file_utils.NormFileToServer)
pydevd_file_utils.NormFileToClient = xbmcfilenamedecorator(pydevd_file_utils.NormFileToClient)

import pydevd