script.pydev.debug
==================

XBMC support for PyDev debugging in Eclipse/Aptana.

How to use:
-----------

Install in your addons directory and enable the addon in XBMC.

Under XBMC navigate to Program Add-ons and click the "PyDev Debug" icon to download pydev.

Now follow the usual instructions for remote debugging:
http://pydev.org/manual_adv_remote_debugger.html

Eg,
	import pydevd
	pydevd.settrace('192.168.0.2')
