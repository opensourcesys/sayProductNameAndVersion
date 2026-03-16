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
from winVersion import getWinVer


# initialize translations
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__()

	# Can't use @script while remaining compatible with NVDA 2017.3, as original author strongly requested.
	def script_sayProductNameAndVersion(self, gesture):
		appName = None
		appVersion = None
		appArch = None
		appVersionAndArch = ""
		isWindows = False
		# Translators: The word version.
		versionWord = _("version") + " "
		focus = api.getFocusObject()

		try:
			appName = focus.appModule.productName
			if appName is None or appName == "":  # If the retrieved name is invalid
				raise ValueErrorException
		except Exception as e:
			# Translators: This is used when the name of the focused application cannot be found.
			appName = _("Application unknown")

		# Are we trying to learn the Windows version?
		if appName == "Microsoft® Windows® Operating System":
			appName = "{0} {1}".format(getWinVer().releaseName, getWinVer().productType)
			appVersion = "Build: {0}.{1}".format(getWinVer().build, getWinVer().revision)
			appArch = getWinVer().processorArchitecture
			appVersionAndArch = "{0} ({1})".format(appVersion, appArch)
			versionWord = ""
			isWindows = True

		try:
			if not isWindows:
				appVersion = focus.appModule.productVersion
			if appVersion is None or appVersion == "":  # If the retrieved version is invalid
				raise ValueErrorException
		except Exception as e:
			# Translators: This is used when the version of the focused application cannot be found.
			appVersion = _("not detected")

		try:
			if not isWindows:
				appArch = focus.appModule.appArchitecture
				if appArch is None or appArch == "":  # If the retrieved architecture is invalid
					raise ValueErrorException
				else:
					appVersionAndArch = "{version} ({arch})".format(version=appVersion, arch=appArch)
		except Exception as e:
			appVersionAndArch = appVersion
			appArch = ""

		pressCount = getLastScriptRepeatCount()

		if pressCount == 0:
			# Outputs the application name, version, and architecture (if set)
			ui.message(
				"{name}, {vWord}{versionAndArch}".format(  # Missing space between tokens is intended
					name=appName, vWord=versionWord, versionAndArch=appVersionAndArch
				)
			)

		elif pressCount == 1:
			# Attempts to copy the application name, version, and architecture to the clipboard
			clipContents = "{name}\n{version}".format(name=appName, version=appVersion)
			if appArch is not None:
				clipContents += "\n{arch}".format(arch=appArch)
			if api.copyToClip(clipContents):
				ui.message(_(
					# Translators: This is the message announced when all information has been copied.
					"Copied {name} {vWord}{versionAndArch} to the clipboard"  # Missing space between tokens is intended
				).format(name=appName, vWord=versionWord, versionAndArch=appVersionAndArch))
			else:  # Copy failure
				ui.message(_(
					# Translators: This is the message announced when all information hasn't been copied.
					"Failed to copy application information to the clipboard."
				))

		else:  # pressCount > 1
			# Attempts to copy the application version (and architecture, if available) to the clipboard
			if api.copyToClip(appVersionAndArch):
				ui.message(_(
					# Translators: The message reporting that only the application's version (and arch) has been copied.
					"Copied {versionAndArch} to the clipboard."
				).format(versionAndArch=appVersionAndArch))
			else:  # Copy failure
				# Translators: This is the message announced when all information hasn't been copied.
				ui.message(_("Cannot copy version information to the clipboard."))


	script_sayProductNameAndVersion.category = SCRCAT_TOOLS
	script_sayProductNameAndVersion.__doc__ = _(
		# Translators: Input help mode message for Say Product Name and Version command.
		"Speaks the name and version of the application on which you are focused."
		" Press twice to copy the information to the clipboard."
		" Press three times to copy only the version number."
	)
	__gestures = { "kb:NVDA+Shift+v": "sayProductNameAndVersion" }
