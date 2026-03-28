# Name, version, and architecture Info Of Current program announcement Global Plugin for NVDA
# Copyright (C) 2024-2026 Luke Davis <XLTechie@newanswertech.com>
# Original author copyright (C) 2014-2023 Patrick ZAJDA <patrick@zajda.fr>
# This file is covered by the GNU General Public License version 2.
# You can read the licence by clicking Help->Licence in the NVDA menu
# or by visiting http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

import addonHandler
import globalPluginHandler
import api
from scriptHandler import getLastScriptRepeatCount, script
import ui
from globalCommands import SCRCAT_TOOLS
from winVersion import getWinVer


# initialize translations
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super().__init__()

	@script(
		description=_(
			# Translators: Input help mode message for Say Product Name and Version command.
			"Speaks the name, version, and architecture of the application on which you are focused."
			" Press twice to copy the information to the clipboard."
			" Press three times to copy the application name and version, as well as those of Windows and NVDA."
		),
		category=SCRCAT_TOOLS,
		gesture="kb:NVDA+Shift+v",
		speakOnDemand=True
	)
	def script_sayProductNameAndVersion(self, gesture):
		appName: str | None = None
		appVersion: str | None = None
		appArch: str | None = None
		singleLineAppInfo: str = ""
		appVersionAndArch: str = ""
		isWindows: bool = False
		# There are two circumstances in which we might need Windows information; get it in case.
		windowsName: str = f"{getWinVer().releaseName} {getWinVer().productType}"
		windowsbuildAndRev: str = f"{getWinVer().build}.{getWinVer().revision}"
		windowsArch: str = getWinVer().processorArchitecture

		# Translators: A message presented whenever a copy to clipboard operation failed.
		COPY_FAILED_MSG = _("Unable to copy version information to the clipboard.")

		focus = api.getFocusObject()

		try:
			appName = focus.appModule.productName
			if appName is None or appName == "":  # If the retrieved name is invalid
				raise ValueErrorException
		except Exception as e:  # FixMe: What other exceptions can arrive here?
			# Translators: This is used when the name of the focused application cannot be found.
			appName = _("Application unknown")

		# Are we trying to learn the Windows version?
		if appName == "Microsoft® Windows® Operating System":
			isWindows = True
			appName = windowsName
			appVersion = windowsBuildAndRev
			appArch = windowsArch

		try:
			if not isWindows:
				appVersion = focus.appModule.productVersion
			if appVersion is None or appVersion == "":  # If the retrieved version is invalid
				raise ValueErrorException
		except Exception as e:  # FixMe: What other kind of exceptions can arrive here?
			# Translators: This is used when the version of the focused application cannot be found.
			appVersion = _("not detected")

		try:
			if not isWindows:
				appArch = focus.appModule.appArchitecture
			if appArch is None or appArch == "":  # If the retrieved architecture is invalid
				raise ValueErrorException
		except Exception as e:  # Which exceptions can arrive here?
			appArch = ""

		singleLineWinInfo = _(
			# Translators: A single line containing the Windows name, build and revision numbers, and architecture.
			"{winName} build {winBuild} ({winArch})"
		).format(winName=windowsName, winBuild=windowsBuildAndRev, winArch=windowsArch)

		if not isWindows:  # It's an app, not the OS
			singleLineAppInfo = _(
				# Translators: A single line containing the name, version, and architecture of the application in focus.
				"{appName} version {appVer} ({appArch})"
			).format(appName=appName, appVer=appVersion, appArch=appArch)
		else:
			singleLineAppInfo = singleLineWinInfo

		if getLastScriptRepeatCount() == 0:
			# Outputs the application name, version, and architecture (if set)
			ui.message(singleLineAppInfo)

		elif getLastScriptRepeatCount() == 1:
			# Attempts to copy the application name, version, and architecture to the clipboard
			forClip = f"{appName}\n{appVersion}" + ("" if appArch is "" else f"\n{appArch}")
			if api.copyToClip(forClip):
				ui.message(_(
					# Translators: This is the message announced when name and version have been copied.
					"Copied version information for {appName} to the clipboard."
				).format(appName=appName))
			else:  # Copy failure
				ui.message(COPY_FAILED_MSG)

		else:  # getLastScriptRepeatCount() > 1
			# Attempts to copy the name and version for the application, NVDA, and Windows, to the clipboard
			# If the focused application is a Windows component, there is no application, and we don't copy that part.
			forClip = "" if isWindows else f"{singleLineAppInfo}\n"
			forClip += _(
				# Translators: The name of NVDA, the word "version", and NVDA's version.
				"{name} version {version}"
			).format(name=buildVersion.name, version=buildVersion.formatBuildVersionString())
			forClip += f"\n{singleLineWinInfo}"

			if api.copyToClip(forClip):
				if isWindows:
					# Translators: Message reporting that NVDA and Windows versions were copied.
					ui.message(_("Copied version information for NVDA and Windows to the clipboard."))
				else:
					ui.message(_(
						# Translators: A message reporting that application, NVDA, and Windows versions were copied.
						"Copied version information for {appName}, NVDA, and Windows to the clipboard."
					).format(appName=appName))
			else:  # Copy failure
				# Translators: This is the message announced when all information hasn't been copied.
				ui.message(COPY_FAILED_MSG)
