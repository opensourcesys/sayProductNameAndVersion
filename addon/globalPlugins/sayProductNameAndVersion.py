# -*- coding: utf-8 -*-
# Name and version Info Of Current program announcement Global Plugin for NVDA
# Copyright (C) 2023 Luke Davis <XLTechie@newanswertech.com>
# Original author copyright (C) 2014-2023 Patrick ZAJDA <patrick@zajda.fr>
# This file is covered by the GNU General Public License.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# Shortcut: NVDA+Shift+V
# Press it twice to copy version information to the clipboard

import addonHandler
import scriptHandler
import globalPluginHandler
from ui import message
import api
from globalCommands import SCRCAT_TOOLS

# initialize translations
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# We initialize the scripts category shown on input gestures dialog
	scriptCategory = SCRCAT_TOOLS

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
		"Say product name and version of the application which ownes the focused window. "
		"If pressed twice, copy these information to the clipboard"
	)

	__gestures = {
		"kb:NVDA+Shift+V": "sayProductNameAndVersion",
	}
