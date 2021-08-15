import os, json, random, string
from pprint import pprint

# ###########################
# 
# Setup things:
# - Create user data file if it doesn't exist
# 
# Export things: 
# - Check for git pulls
# - Read data files, build binary files, save to new version of ecdp folder
# - Generate new statistics
# 
# App Data: 
# - Language: create (only update/delete by asking me)
# 
# User Data: 
# - Add translation: filename, line index, language, index of translation
# 	- Need to check user's language proficiencies
# - Add verification: filename, line index, language, index of translation, verification type
# 	- Need to check user's language proficiencies
# - ROM filepath: create, update
# - Languages: create, delete
# 
# File Data: 
# - Add translation: append to end of list of translations
# - Add verification: add to verifications of last in list of translations, verification type
# 
# ###########################



code_files = ["header.bin", "banner.bin", "y7.bin", "y9.bin", "arm7.bin", "arm9.bin"]
code_folders = ["dwc", "dscpd", "overlay"]
app_files = ["app_data"]

def formatRootFolder(root):
	win = "\\"
	unix = "/"
	
	if os.name == 'nt':
		root = root.replace(unix, win)
		if root[-1:] != win:
			root = root + win
	elif os.name == 'posix':
		root = root.replace(win, unix)
		if root[-1] != unix:
			root = root + unix
	
	return root

def crawl(root, ext, exclude=[]):
	root = formatRootFolder(root)

	files = []
	
	entries = os.scandir(root)
	for e in entries:

		should_exclude = e.name in exclude

		if should_exclude:
			continue

		if e.is_dir():
			subdir_files = crawl(root + e.name, ext, exclude=exclude)
			files.extend(subdir_files)
			continue
		
		extension_matches = len(e.name) >= len(ext) and e.name[-1 * len(ext):] == ext

		if extension_matches:
			files.append("{}{}".format(root,e.name))

	return files

def checkLanguageValidity(existing, new):

	for e in existing:
		if e["ISO_name"] == new["ISO_name"]:
			msg = "The following data already exists in our system: \"{}\"".format(new["ISO_name"])
		elif not new["ISO_name"]:
			msg = "New language does not provide an ISO name"
		elif e["native_name"] == new["native_name"]:
			msg = "The following data already exists in our system: \"{}\"".format(new["native_name"])
		elif not new["native_name"]:
			msg = "New language does not provide a native name"
		elif not new["meaning_verification"]:
			msg = "New language does not provide a translation for \"The meaning is accurate\""
		elif not new["fluency_verification"]:
			msg = "New language does not provide a translation for \"The translation sounds natural\""
		else:
			continue
			
		raise Exception(msg)
	
def getData(filepath):
	with open(filepath, 'r', encoding="utf-8") as file:
		data = json.loads(file.read())
	
	return data
	
def saveData(data, filepath):
	with open(filepath, 'w', encoding="utf-8") as file:
		file.write(json.dumps(data, indent=2, ensure_ascii=False))

# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
def addLanguage(data, ISO_name, native_name, meaning_verification="", fluency_verification=""):
	language = {
		"ISO_name": ISO_name,
		"native_name": native_name,
		"meaning_verification": meaning_verification,
		"fluency_verification": fluency_verification,
	}

	checkLanguageValidity(data['languages'], language)

	data['languages'].append(language)

def updateROMFilepath(data, filepath):
	data['rom_filepath'] = filepath

def checkUserLanguages(data, dest_language, intermediate_language=None, fluency_required=False):
	source_language = 'Japanese'
	
	if not fluency_required:
		if not isUserLanguage(data, dest_language):
			msg = "Only those who are fluent in or learning {} can contribute to the translations".format(dest_language)
			raise Exception(msg)
	else:
		if not isUserFluentLanguage(data, dest_language):
			msg = "Only those who are fluent in {} can contribute to fluency verifications".format(dest_language)
		
	if intermediate_language:
		if not isUserLanguage(data, intermediate_language):
			msg = "Only those who are fluent in or learning {} can contribute to the translations".format(intermediate_language)
			raise Exception(msg)
	else:
		if not isUserLanguage(data, source_language):
			msg = "Only those who are fluent in or learning {} can contribute to the translations".format(source_language)
			raise Exception(msg)

def checkAppLanguages(data, dest_language, intermediate_language=None):
	if not isAppLanguage(data, dest_language):
		msg = "\"{}\" is not a language in our system yet".format(dest_language)
		raise Exception(msg)
	if intermediate_language:
		if not isAppLanguage(data, intermediate_language):
			msg = "\"{}\" is not a language in our system yet".format(intermediate_language)
			raise Exception(msg)
	
def isAppLanguage(data, language):
	app_languages = [l['ISO_name'] for l in data['languages']]
	return language in app_languages

def isUserLanguage(data, language):
	return isUserFluentLanguage(data, language) or \
		isUserLearningLanguage(data, language)
	
def isUserFluentLanguage(data, language):
	return language in data['languages']['fluent']
	
def isUserLearningLanguage(data, language):
	return language in data['languages']['learning']
	
def addToDictIfDNE(dict, key, value):
	if key not in dict:
		dict.update({key:value})
	return dict

def addTranslation(file_data, app_data, user_data, dest_language, index, translation, intermediate_language=None):
	file_name = file_data['name']
	
	checkAppLanguages(app_data, dest_language, intermediate_language=intermediate_language)
	checkUserLanguages(user_data, dest_language, intermediate_language=intermediate_language)

	data = {
		"translation": translation,
		"meaning_verification": 0,
		"fluency_verification": 0,
	}
	
	tr = file_data['strings'][index]['translations']
	addToDictIfDNE(tr, dest_language, [])
	tr[dest_language].append(data)
	new_translation_index = len(tr[dest_language]) - 1
	
	user_tr = user_data["user_translations"]
	addToDictIfDNE(user_tr, file_name, {})
	addToDictIfDNE(user_tr[file_name], index, {})
	addToDictIfDNE(user_tr[file_name][index], dest_language, [])
	user_tr[file_name][index][dest_language].append(new_translation_index)

def addVerification(file_data, app_data, user_data, dest_language, index, type, intermediate_language=None):
	file_name = file_data['name']
	
	if type not in ["meaning_verification", "fluency_verification"]:
		msg = "Verification must be of type \"meaning_verification\" or \"fluency_verification\""
		raise Exception(msg)
		
	checkAppLanguages(app_data, dest_language, intermediate_language=intermediate_language)
	checkUserLanguages(user_data, dest_language, intermediate_language=intermediate_language, fluency_required=type == "fluency_verification")

	tr = file_data['strings'][index]['translations']
	language_index = len(tr[dest_language]) - 1

	tr[dest_language][-1][type] = tr[dest_language][-1][type] + 1
	
	user_val = user_data['user_verifications']
	addToDictIfDNE(user_val, file_name, {})
	addToDictIfDNE(user_val[file_name], index, {})
	addToDictIfDNE(user_val[file_name][index], dest_language, [])
	if language_index not in user_val[file_name][index][dest_language]:
		user_val[file_name][index][dest_language].append(language_index)
	
def addMeaningVerification(file_data, app_data, user_data, dest_language, index, intermediate_language=None):
	addVerification(file_data, app_data, user_data, dest_language, index, "meaning_verification", intermediate_language=intermediate_language)

def addFluencyVerification(file_data, app_data, user_data, dest_language, index, 	intermediate_language=None):
	addVerification(file_data, app_data, user_data, dest_language, index, "fluency_verification", intermediate_language=intermediate_language)

def addUserLearningLanguage(user_data, app_data, language):
	if not isAppLanguage(app_data, language):
		msg = "Cannot add user language \"{}\". Language does not exist in our system. ".format(langauge)

	if language not in user_data["languages"]["learning"]:
		user_data["languages"]["learning"].append(language)
		
		if language in user_data["languages"]["fluent"]:
			user_data["languages"]["fluent"].remove(language)
		
def addUserFluentLanguage(user_data, app_data, language):
	if not isAppLanguage(app_data, language):
		msg = "Cannot add user language \"{}\". Language does not exist in our system. ".format(langauge)

	if language not in user_data["languages"]["fluent"]:
		user_data["languages"]["fluent"].append(language)
		
		if language in user_data["languages"]["learning"]:
			user_data["languages"]["learning"].remove(language)

def removeUserLanguage(user_data, language):
	if language in user_data["languages"]["fluent"]:
		user_data["languages"]["fluent"].remove(language)
		
	if language in user_data["languages"]["learning"]:
		user_data["languages"]["learning"].remove(language)
