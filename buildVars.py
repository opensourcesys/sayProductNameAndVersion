# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct, whenever possible.

# Full getext (please don't change)
# Since some strings in `addon_info` are translatable,
# we need to include them in the .po files.
# Gettext recognizes only strings given as parameters to the `_` function.
# To avoid initializing translations in this module we simply roll our own "fake" `_` function
# which returns whatever is given to it as an argument.
def _(arg):
	return arg

# Add-on information variables
addon_info = {
	# add-on Name
	"addon_name" : "sayProductNameAndVersion",
	# Add-on summary
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Say Product Name and Version"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""Speak the name and version of the application you are currently focused on, by pressing NVDA+Shift+v.
Pressing twice will copy this information to the clipboard, to paste in bug reports, etc.
Pressing three times copies only the version.
The key can be remapped.
Read help to find tips for hearing NVDA and Windows versions."""),
	# version
	"addon_version" : "2025.1.0",
	# Author(s)
	"addon_author" : "Luke Davis <XLTechie@newanswertech.com>, Patrick ZAJDA <patrick@zajda.fr>",
	# URL for the add-on documentation support
	"addon_url" : "https://github.com/opensourcesys/sayProductNameAndVersion#readme",
	# URL for the add-on repository where the source code can be found
	"addon_sourceURL": "https://github.com/opensourcesys/sayProductNameAndVersion",
	# Documentation file name
	"addon_docFileName" : "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
	"addon_minimumNVDAVersion" : "0.0.0", # Was 2017.3
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion" : "2025.1.1",
	# Add-on update channel (default is None, denoting stable releases, and for development releases, use "dev"; do not change unless you know what you are doing)
	"addon_updateChannel" : None,
	# Add-on license such as GPL 2
	"addon_license": "GPL V2",
	# URL for the license document the ad-on is licensed under
	"addon_licenseURL": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
}

# Define the python files that are the sources of your add-on.
# You can either list every file (using ""/") as a path separator,
# or use glob expressions.
# For example to include all files with a ".py" extension from the "globalPlugins" dir of your add-on
# the list can be written as follows:
# pythonSources = ["addon/globalPlugins/*.py"]
# For more information on SCons Glob expressions please take a look at:
# https://scons.org/doc/production/HTML/scons-user/apd.html
pythonSources = ["addon/globalPlugins/*.py"]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []

# Base language for the NVDA add-on
# If your add-on is written in a language other than english, modify this variable.
# For example, set baseLanguage to "es" if your add-on is primarily written in spanish.
baseLanguage = "en"

# Markdown extensions for add-on documentation
# Most add-ons do not require additional Markdown extensions.
# If you need to add support for markup such as tables, fill out the below list.
# Extensions string must be of the form "markdown.extensions.extensionName"
# e.g. "markdown.extensions.tables" to add tables.
markdownExtensions = []
