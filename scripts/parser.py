import os
import json
import pprint

def parseByte(bytes):
	return int.from_bytes(bytes, byteorder="little")

def getMetaData(data):
	num_strings = parseByte(data[0:2])
	
	pointers = []
	
	if num_strings < 500:
		for i in range(num_strings):
			start = i * 2 + 2
			end = start + 2
			pointers.append(parseByte(data[start:end]))
	
	return pointers

def getStringAtOffset(data, pointer):
	try:
		start = pointer
		end = data.index(b"\x00", pointer)
		bytes = data[start:end]
		return bytes.decode(encoding="shift-jisx0213")
		
	except Exception as err:
		print('At {}: '.format(pointer), err)


if __name__ == "__main__":
	rom_filepath = input("Provide the entire (or relative) filepath to your expanded rom file: ")
	rom_filepath = "D:\\ecdp\\eCDP_i18n_Base\\" if rom_filepath == "" else rom_filepath
	
	internal_filepath = input("Specify a folder within the rom (such as \"data/soc/\"): ")
	internal_filepath.replace("/","\\")
	internal_filepath = internal_filepath + '\\' if internal_filepath[:-2] != "\\" else internal_filepath
	
	filenames=os.listdir(rom_filepath + internal_filepath)
	filenames = [f[:-4] for f in filenames if f[-4:] == ".bin"]
	
	for filename in filenames:
		print(filename, end=': ')
		
		with open('{}{}{}.bin'.format(rom_filepath,internal_filepath,filename),"rb") as file:
			contents = file.read()

		pointers = getMetaData(contents)
		print('{} (n={})'.format(pointers, len(pointers)))
		
		strings = []
		for pointer in pointers:
			string_data = {
				"original_japanese":getStringAtOffset(contents, pointer),
				"original_pointer":pointer,
				"translations":{},
				}
			strings.append(string_data)
			
		pprint.pprint(strings)
		
		with open(".\\{}{}.json".format(internal_filepath, filename),"w",encoding='utf-8') as file:
			json_data = {"name":filename,"strings":strings}
			json_data = json.dumps(json_data, ensure_ascii=False, indent=2)
			
			file.write(json_data)
