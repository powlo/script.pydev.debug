import os
import urllib2
import zipfile
import shutil
import xbmc
import xbmcgui
import xbmcaddon
import errno

### get addon info
__addon__       = xbmcaddon.Addon(id='script.pydev.debug')
__addonid__     = __addon__.getAddonInfo('id')
__addonname__   = __addon__.getAddonInfo('name')
__author__      = __addon__.getAddonInfo('author')
__version__     = __addon__.getAddonInfo('version')
__addonpath__   = __addon__.getAddonInfo('path')

###Constants that may need to be updated in future revisions
download_url = "http://sourceforge.net/projects/pydev/files/pydev/PyDev%202.7.3/PyDev%202.7.3.zip/download"
download_folder = os.path.join(__addonpath__, 'resources', 'download')
lib_folder = os.path.join(__addonpath__, 'resources', 'lib')
patch_folder = os.path.join(__addonpath__, 'resources', 'patch')
download_file =  os.path.join(download_folder, 'PyDev2.7.3.zip')
pysrc_folder = os.path.join(download_folder,'plugins/org.python.pydev_2.7.3.2013031601/pysrc/')

def activate():
    """
    Downloads, extracts and patches PyDev's pysrc
    """
    shutil.rmtree(download_folder)
    os.mkdir(download_folder)
    xbmc.log("%s: Downloading..." % __addonname__)
    xbmc.log("%s: From '%s' to '%s' " % (__addonname__, download_url, download_file))
    try:
        file = urllib2.urlopen(download_url)
    except urllib2.URLError as e:
        dialog = xbmcgui.Dialog()
        dialog.ok('Error', 'Could not download from %s' % download_url.split('/')[2])
        xbmc.log('%s: Failed to download from  %s'% (__addonname__, download_url))
        xbmc.log('%s: %s'% (__addonname__, e.reason))
        return
    progress = xbmcgui.DialogProgress()
    progress.create('Downloading PyDev', "Opening %s" % download_url)
    output = open(download_file,'wb')
    meta = file.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 8192
    
    while not progress.iscanceled():
        buffer = file.read(block_sz)
        if not buffer:
            break
    
        file_size_dl += len(buffer)
        output.write(buffer)
        percent = file_size_dl * 90 / file_size
        progress.update(percent, "Downloading...")
    
    output.close()

    if progress.iscanceled():
        progress.close()
        return

    xbmc.log("%s: Download finished" % __addonname__)

    #Extract
    progress.update(93, "Extracting zip...")
    xbmc.log("%s: Extracting..." % __addonname__)
    zfile= zipfile.ZipFile(download_file)
    zfile.extractall(download_folder)

    #Copy pysrc code to /lib/
    progress.update(95, "Moving files...")    
    xbmc.log("%s: Moving..." % __addonname__)
    xbmc.log("%s: from %s" % (__addonname__, pysrc_folder))
    xbmc.log("%s: to %s" % (__addonname__, lib_folder))
    shutil.rmtree(lib_folder)
    shutil.copytree(pysrc_folder, lib_folder)

    #Apply the patch
    progress.update(98, "Patching code...")        
    patch = os.path.join(patch_folder, 'pydevd_file_utils.patch')
    file = open(patch, "r")
    content = file.read()
    file.close()
    target = os.path.join(lib_folder, 'pydevd_file_utils.py')
    file = open(target, "a")
    file.write(content)
    file.close()
    progress.close()
    dialog = xbmcgui.Dialog()
    dialog.ok('Done!','PyDev debug has been imported and patched')

xbmc.log("######## Launching Script PyDev Debug........................")
xbmc.log('## Add-on ID   = %s' % str(__addonid__))
xbmc.log('## Add-on Name = %s' % str(__addonname__))
xbmc.log('## Author      = %s' % str(__author__))
xbmc.log('## Version     = %s' % str(__version__))    
dialog = xbmcgui.Dialog()

try:
    import pydevd
    if lib_folder not in pydevd.__file__:
        dialog.ok('Already Installed Elsewhere', 'pydevd is already on sys.path')
    else:
        ret = dialog.yesno('Already Installed', 'Do you want to install and patch PyDev anyway?')
        if ret:
            activate()
except:
    if dialog.yesno('Install PyDev', 'Do you want to install and patch PyDev?'):
        activate()
