
# Imports
import os
ROOT: str = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
IGNORE_UNSET: bool = True							# If True, the program will ignore unset optionnal values in the configuration dictionnary

# Folders
ASSETS_FOLDER: str = f"{ROOT}/assets"			# Folder where the assets are stored
MERGE_FOLDER: str = f"{ROOT}/merge"				# Folder where the merged files are stored
BUILD_FOLDER: str = f"{ROOT}/build"				# Folder where the final datapack and resource pack are built
BUILD_COPY_DESTINATIONS: tuple[list, list] = (["D:/latest_snapshot/world/datapacks"], ["D:/minecraft/snapshot/resourcepacks"])	# Can be empty lists if you don't want to copy the generated files to other folders.

# Dev constants
DATABASE_DEBUG: str = f"{ROOT}/database_debug.json"	# Dump of the database for debugging purposes
ENABLE_TRANSLATIONS: bool = False					# Will convert all the text components to translate and generate a lang file in the resource pack. Meaning you can easily translate the datapack in multiple languages!


# Datapack related constants
AUTHOR: str = "Stoupy51"				# Author(s) name(s) displayed in pack.mcmeta, also used to add convention.debug tag to the players of the same name(s) <-- showing additionnal displays like datapack loading
PROJECT_NAME: str = "ShoppingKart"		# Name of the datapack, used for messages and items lore
VERSION: str = "1.3.2"					# Datapack version in the following mandatory format: major.minor.patch, ex: 1.0.0 or 1.21.615
NAMESPACE: str = "shopping_kart"		# Used to namespace functions, tags, etc. Should be the same you use in the merge folder.
DESCRIPTION = f"{PROJECT_NAME} [{VERSION}] by {AUTHOR}"	# Pack description displayed in pack.mcmeta

# Technical constants
SOURCE_LORE: list[dict] = [{"text":"ICON"},{"text": f" {PROJECT_NAME}","italic":True,"color":"blue"}]	# Appended lore to any custom item, can be an empty string


# Configuration dictionnary
configuration = {
	"ignore_unset": IGNORE_UNSET,

	"assets_folder": ASSETS_FOLDER,
	"merge_folder": MERGE_FOLDER,
	"build_folder": BUILD_FOLDER,
	"build_copy_destinations": BUILD_COPY_DESTINATIONS,

	"database_debug": DATABASE_DEBUG,
	"enable_translations": ENABLE_TRANSLATIONS,

	"author": AUTHOR,
	"project_name": PROJECT_NAME,
	"version": VERSION,
	"namespace": NAMESPACE,
	"description": DESCRIPTION,
	"source_lore": SOURCE_LORE,
}

