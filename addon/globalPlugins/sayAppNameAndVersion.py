# -*- coding: utf-8 -*-
# Name and version Info Of Current program announcement Global Plugin for NVDA
# Copyright (C) 2024-2026 Luke Davis <XLTechie@newanswertech.com>
# Original author copyright (C) 2014-2023 Patrick ZAJDA <patrick@zajda.fr>
# This file is covered by the GNU General Public License version 2.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

import addonHandler
import globalPluginHandler
import api
from scriptHandler import getLastScriptRepeatCount
import ui
from globalCommands import SCRCAT_TOOLS

# initialize translations
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__()

	# Can't use @script while remaining compatible with NVDA 2017.3, as original author strongly requested.
	def script_sayAppNameAndVersion(self, gesture):
		focus = api.getFocusObject()
		appName: Optional[str] = None
		appVersion: str = ""

		try:
			appName = focus.appModule.productName
			if appName is None or appName == "":  # If the retrieved name is invalid
				raise ValueErrorException
		except Exception as e:
			# Translators: This is used when the name of the focused application cannot be found.
			appName = _("Application unknown")

		try:
			appVersion = focus.appModule.productVersion
			if appVersion is None or appVersion == "":  # If the retrieved version is invalid
				raise ValueErrorException
		except Exception as e:
			# Translators: This is used when the version of the focused application cannot be found.
			appVersion = _("not detected")

		pressCount = getLastScriptRepeatCount()

		if pressCount == 0:
			# Outputs the application name and version
			ui.message(_(
				# Translators: This is the message which will be spoken containing both the application's name and version.
				"{name} version {version}"
			).format(name=appName, version=appVersion))

		elif pressCount == 1:
			# Attempts to copy the application name and version to the clipboard
			if api.copyToClip("{name} {version}".format(name=appName, version=appVersion)):
				ui.message(_(
					# Translators: This is the message announced when all information has been copied.
					"Copied {name} {version} to the clipboard"
				).format(name=appName, version=appVersion))
			else:  # Copy failure
				ui.message(_(
					# Translators: This is the message announced when all information hasn't been copied.
					"Failed to copy application name and version information to the clipboard."
				))

		else:  # pressCount > 1
			# Attempts to copy the application version to the clipboard
			if api.copyToClip(appVersion):
				ui.message(_(
					# Translators: This is the message announced when only the application's version has been copied.
					"Copied {version} to the clipboard."
				).format(version=appVersion))
			else:  # Copy failure
				# Translators: This is the message announced when all information hasn't been copied.
				ui.message(_("Cannot copy version information to the clipboard."))


	script_sayAppNameAndVersion.category = SCRCAT_TOOLS
	script_sayAppNameAndVersion.__doc__ = _(
		# Translators: Input help mode message for say application name and version command.
		"Speaks the name and version of the application on which you are focused."
		" Press twice to copy the information to the clipboard."
		" Press three times to copy only the version number."
	)
	__gestures = { "kb:NVDA+Shift+v": "sayAppNameAndVersion" }
