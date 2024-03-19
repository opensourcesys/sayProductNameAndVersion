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
			self.productName = focus.appModule.productName
		except Exception:
			self.productName = ""
		try:
			self.productVersion = focus.appModule.productVersion
		except Exception:
			self.productVersion = ""

		if self.productName == "":
			# Translators: This is used when the name of the focused application cannot be found.
			self.productName = _("Application")
		if self.productName != "" and self.productVersion != "":
			pressCount = getLastScriptRepeatCount()
			if pressCount == 0:
				self.sayBoth()
			elif pressCount == 1:
				self.copyBoth()
			else:  # pressCount > 1
				self.copyVersion()
		else:
			# Translators: this will be spoken if version information was not available.
			message(_("Unable to get version info"))

	def sayBoth(self):
		"""Speaks the product name and version."""
		# Translators: This is the message which will be spoken containing both the product name and version.
		# {name} is the app name, {version} is the version.
		message(_("{name} version {version}").format(name=self.productName, version=self.productVersion))

	def copyBoth(self):
		"""Attempts to copy the product name and version to the clipboard."""
		if api.copyToClip("{name} {version}".format(name=self.productName, version=self.productVersion)):
			# Translators: This is the message announced when all information has been copied..
			# {name} is the app name, {version} is the version.
			message(_("Copied {name} {version} to the clipboard").format(
				name=self.productName,
				version=self.productVersion
			))
		else:
			# Translators: This is the message announced when all information hasn't been copied.
			message(_("Cannot copy version information to the clipboard."))

	def copyVersion(self):
		"""Attempts to copy the product version to the clipboard."""
		if api.copyToClip(self.productVersion):
			# Translators: This is the message announced when only the version has been copied..
			# {version} is the version.
			message(_("Copied {version} to the clipboard.").format(
				version=self.productVersion
			))
		else:
			# Translators: This is the message announced when all information hasn't been copied.
			message(_("Cannot copy version information to the clipboard."))

	script_sayProductNameAndVersion.category = SCRCAT_TOOLS
	script_sayProductNameAndVersion.__doc__ = _(
		# Translators: Input help mode message for say product name and version command.
		"Speaks the name and version of the application on which you are focused."
		" Press twice to copy the information to the clipboard."
		" Press three times to copy only the version number."
	)
	__gestures = { "kb:NVDA+Shift+v": "sayProductNameAndVersion" }
