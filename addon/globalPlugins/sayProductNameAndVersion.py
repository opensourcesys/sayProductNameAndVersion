# -*- coding: utf-8 -*-
# Name and version Info Of Current program announcement Global Plugin for NVDA
# Copyright (C) 2024 Luke Davis <XLTechie@newanswertech.com>
# Original author copyright (C) 2014-2023 Patrick ZAJDA <patrick@zajda.fr>
# This file is covered by the GNU General Public License version 2.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

import addonHandler
import globalPluginHandler
import api
from scriptHandler import getLastScriptRepeatCount
from ui import message
from globalCommands import SCRCAT_TOOLS

# initialize translations
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__()

	# Can't use @script while remaining compatible with NVDA 2017.3.
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
			isSameScript = getLastScriptRepeatCount()
			if isSameScript == 0:
				# Translators: This is the message which will be spoken if the key is pressed once.
				# {name} is the app name, {version} is the version.
				message(_("{name} version {version}").format(name=productName, version=productVersion))
			else:
				if api.copyToClip("{name} {version}".format(name=productName, version=productVersion)):
					# Translators: This is the message announced when all information has been copied..
					# {name} is the app name, {version} is the version.
					message(_("Copied {name} {version} to the clipboard").format(
						name=productName, version=productVersion
					))
				else:
					# Translators: This is the message announced when all information hasn't been copied.
					message(_("Cannot copy version information to the clipboard."))
		else:
			# Translators: this will be spoken if version information was not available.
			message(_("Unable to get version info"))

	script_sayProductNameAndVersion.category = SCRCAT_TOOLS
	script_sayProductNameAndVersion.__doc__ = _(
		# Translators: Input help mode message for say product name and version command.
		"Speaks the product name and version of the application which ownes the focused window."
		" If pressed twice, copies this information to the clipboard"
	)
	__gestures = { "kb:NVDA+Shift+v": "sayProductNameAndVersion" }
