# Build customizations
# Change this file instead of sconstruct, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
# add-on Name
	"addon-name" : "sayProductNameAndVersion",
	# Add-on description
	# TRANSLATORS: Summary for this add-on to be shown on installation and add-on informaiton.
	"addon-summary" : _("Say Product Name and Version"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on installation and add-on information
	"addon-description" : _("""Say product name and version of the application which ownes the focused window.
Shortcut: Shift+NVDA+V"""),
	# version
	"addon-version" : "1.0.1",
	# Author(s)
	"addon-author" : "Patrick ZAJDA <patrick@zajda.fr>",
# URL for the add-on documentation support
"addon-url" : None
}

import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join("addon", "globalPlugins", "sayProductNameAndVersion", "*.py*")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
