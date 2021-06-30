import os, json
from pprint import pprint

code_files = ["header.bin", "banner.bin", "y7.bin", "y9.bin", "arm7.bin", "arm9.bin"]
code_folders = ["dwc", "dscpd", "overlay"]
app_files = ["app_data"]

def formatRootFolder(root):
	root = root.replace("/","\\")
	if root[-1:] != "\\":
		root = root + "\\"
		
	return root

def crawl(root, ext, exclude=[]):
	root = formatRootFolder(root)

	files = []
	
	entries = os.scandir(root)
	for e in entries:

		should_exclude = e.name in exclude
		extension_matches = False
		if len(e.name) >= len(ext):
			extension_matches = e.name[-1 * len(ext):] == ext

		if e.is_dir() and not should_exclude:
			subdir_files = crawl(root + e.name, ext, exclude=exclude)
			files.extend(subdir_files)
		elif extension_matches and not should_exclude :
			files.append("{}{}".format(root,e.name))

	return files

def checkLanguageValidity(existing, new):

	for e in existing:
		if e["ISO_name"] == new["ISO_name"]:
			msg = "The following data already exists in our system: \"{}\"".format(new["ISO_name"])
			raise Exception(msg)
		elif e["native_name"] == new["native_name"]:
			msg = "The following data already exists in our system: \"{}\"".format(new["native_name"])
			raise Exception(msg)
		elif not new["meaning_validation"]:
			msg = "New language does not provide a translation for \"The meaning is accurate\""
			raise Exception(msg)
		elif not new["fluency_validation"]:
			msg = "New language does not provide a translation for \"The translation sounds natural\""
			raise Exception(msg)
	
	return (True, None)

# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
def addLanguage(ISO_name, native_name, meaning_validation, fluency_validation):
	filename = ".\\data\\app_data\\app_data.json"
	with open(filename, 'r', encoding="utf-8") as file:
		data = json.loads(file.read())

	language = {
		"ISO_name": ISO_name,
		"native_name": native_name,
		"meaning_validation": meaning_validation,
		"fluency_validation": fluency_validation,
	}
	
	checkLanguageValidity(data['languages'], language)

	data['languages'].append(language)

	with open(filename, 'w', encoding="utf-8") as file:
		file.write(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
	test_crawl = False
	test_add_language = False
	
	if test_add_language:
		print('Adding language')
		addLanguage("Spanish","Español", "El significado es exacto", "La traducción parece natural")
		# addLanguage("English","English","The meaning is accurate", "The translation sounds natural")
	
	if test_crawl:
		to_ignore = code_files + code_folders + app_data

		files = crawl("D:\\ecdp\\eCDP_i18n_Base\\", ".bin", exclude=to_ignore)	
		# files = crawl("D:\\ecdp\\eCDP-translation\\data", ".json", exclude=to_ignore)
		pprint(files)