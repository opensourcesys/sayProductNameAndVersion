# -*- coding: utf-8 -*-
# Version Info Of Current program announcement Global Plugin for NVDA
# Authors: Patrick ZAJDA
# Shortcut: NVDA+Shift+V
# Press it twice to copy version informations to the clipboard

import addonHandler
import scriptHandler
import globalPluginHandler
from ui import message
import api
from globalCommands import SCRCAT_SPEECH

# initialize translations
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# We initialize the scripts category shown on input gestures dialog
	scriptCategory = SCRCAT_SPEECH

	def script_sayProductNameAndVersion(self, gesture):
		focus = api.getFocusObject()
		try:
			productName = focus.appModule.productName
		except Exception:
			productName = ""
		try:
			productVersion = focus.appModule.productVersion
		except Exception:
			productVersion = ""

		if productName == "":
			# Translators: This is used when the name of the focused application cannot be found.
			productName = _("Application")
		if productName != "" and productVersion != "":
			isSameScript = scriptHandler.getLastScriptRepeatCount()
			if isSameScript == 0:
				# Translators: This is the message which will be spoken or copied to the clipboard.
				# {name} is the app name, {version} its the version.
				message(_("{name} version {version}").format(name=productName, version=productVersion))
			else:
				if api.copyToClip(_("{name} version {version}").format(name=productName, version=productVersion)):
					# Translators: This is the message announced when all informations has been copied.
					message(_(u"{name} version {version} copied to the clipboard").format(
						name=productName, version=productVersion
					))
				else:
					# Translators: This is the message announced when all informations hasn't been copied.
					message(_("Cannot copy version informations to the clipboard."))
		else:
			# Translators: this will be spoken if version informations were not available.
			message(_("Unable to get version info"))

	# Documentation
	# Translators: Input help mode message for say product name and version command.
	script_sayProductNameAndVersion.__doc__ = _(
		"Announce the version of the executable of the focused window "
		"or copy it to the clipboard if pressed twice"
	)

	__gestures = {
		"kb:NVDA+Shift+V": "sayProductNameAndVersion",
	}
