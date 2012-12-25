# -*- coding: utf-8 -*-
# Version Info Of Current program announcement Global Plugin for NVDA
# Authors: Patrick ZAJDA
# Shortcut: NVDA+Shift+V
# Press it twice to copy version informations to the clipboard

import os, win32api, win32con, win32process

def GetExePathFromPID(pid):
	processes = win32process.EnumProcesses()    # get PID list
	try:
		handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,False, pid)
		return win32process.GetModuleFileNameEx(handle, 0)
	except:
		pass
	return False

def GetProductNameAndVersion (filename):
	try:
		pairs=win32api.GetFileVersionInfo(filename, '\\VarFileInfo\\Translation')
		lang,codepage=pairs[0][0],pairs[0][1]

		str_info=u'\\StringFileInfo\\%04X%04X\\ProductVersion' %(lang,codepage)
		productVersion=win32api.GetFileVersionInfo(filename, str_info)

		str_info=u'\\StringFileInfo\\%04X%04X\\ProductName' %(lang,codepage)
		productName=win32api.GetFileVersionInfo(filename, str_info)
		return productName,productVersion
	except:
		pass
	return "", ""

import globalPluginHandler
import addonHandler
import scriptHandler
from ui import message
import api
from appModuleHandler import getAppNameFromProcessID

# initialize translations
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def script_sayProductNameAndVersion(self, gesture):
		focus=api.getFocusObject()
		appName=GetExePathFromPID(focus.processID)
		productName, productVersion = GetProductNameAndVersion(appName)
		if productName is None or productName=="":
			# Translators: This is used when the name of the focused application cannot be found.
			productName = _("Application")
		if productName is not None and productVersion is not None and productName != "" and productVersion != "":
			isSameScript =scriptHandler.getLastScriptRepeatCount()
			if isSameScript==0:
				# Translators: This is the message which will be spoken or copied to the clipboard. {name} is the app name, {version} its the version.
				message(_("{name} version {version}").format(name=productName,version=productVersion))
			else:
				if api.copyToClip(_("{name} version {version}").format(name=productName,version=productVersion)):
					# Translators: This is the message announced when all informations has been copied.
					message(_(u"{name} version {version} copied to the clipboard").format(name=productName,version=productVersion))
				else:
					# Translators: This is the message announced when all informations hasn't been copied.
					message(_("Cannot copy version informations to the clipboard."))
		else:
			# Translators: this will be spoken if version informations were not available.
			message(_("Unable to get version info"))

		# Documentation
		# Translators : the script description.
	script_sayProductNameAndVersion.__doc__ = _("Announce the version of the executable of the focused window or copy it to the clipboard if pressed twice")

	__gestures={
		"kb:NVDA+Shift+V": "sayProductNameAndVersion",
	}

