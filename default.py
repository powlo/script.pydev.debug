import sys
import os
import xbmc
import xbmcaddon

### get addon info
__addon__       = xbmcaddon.Addon(id='script.pydev.debug')
__addonid__     = __addon__.getAddonInfo('id')
__addonname__   = __addon__.getAddonInfo('name')
__author__      = __addon__.getAddonInfo('author')
__version__     = __addon__.getAddonInfo('version')
__addonpath__   = __addon__.getAddonInfo('path')
__addonprofile__= xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode('utf-8')
__PYSRC_PATH__  = 'pysrc_path'
link_name = os.path.join(__addonpath__, 'resources', 'lib', 'link')


def activate():
    source = __addon__.getSetting(__PYSRC_PATH__)
    
    #import win32file
    #win32file.CreateSymbolicLink(fileSrc, fileTarget, 1)    
    if os.path.isdir(source):
        if os.path.islink(link_name):
            os.unlink(link_name)
        os.symlink(source, link_name)
        xbmc.log('script.pydev.debug: Created symlink from %s to %s' % (link_name, source))
        
if __name__ == '__main__':
    xbmc.log("######## Activating Script PyDev Debug........................")
    xbmc.log('## Add-on ID   = %s' % str(__addonid__))
    xbmc.log('## Add-on Name = %s' % str(__addonname__))
    xbmc.log('## Author      = %s' % str(__author__))
    xbmc.log('## Version     = %s' % str(__version__))    
    activate()