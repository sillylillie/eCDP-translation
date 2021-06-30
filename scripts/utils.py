import os
from pprint import pprint

code_files = ["header.bin", "banner.bin", "y7.bin", "y9.bin", "arm7.bin", "arm9.bin"]
code_folders = ["dwc", "dscpd", "overlay"]

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

if __name__ == "__main__":
	files = crawl("D:\\ecdp\\eCDP_i18n_Base\\", ".bin", exclude=code_files + code_folders)	
	# files = crawl("D:\\ecdp\\eCDP-translation\\data", ".json", exclude=code_files + code_folders)
	pprint(files)