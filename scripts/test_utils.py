from pprint import pprint
import copy, time
import utils

def test_add_verification():
	# ARRANGE
	file_data = {
		"name": "soc_tp00",
		"strings": [
			{
				"original_japanese": "マックフライポテトのバスケッティング",
				"original_pointer": 142,
				"translations": {}
			}
		]
	}
	app_data = utils.getData("D:\\ecdp\\eCDP-translation\\app_data\\app_data.json")
	utils.addLanguage(app_data, 'Spanish', 'Español', 'El significado es exacto', 'La traducción parece natural')
	user_data = {
		"languages": {
			"learning": [
				"Japanese"
			],
			"fluent": [
				"English"
			]
		},
		"user_translations": {},
		"user_verifications": {}
	}
	dest_language = "English"
	index = 0
	translation = "Basketing McFries"
	intermediate_language = 'Spanish'
	utils.addTranslation(file_data, app_data, user_data, dest_language, index, translation)
	
	check_failed1 = False
	check_failed2 = False
	
	# ACT
	utils.addMeaningVerification(file_data, app_data, user_data, dest_language, index)
	try:
		utils.addMeaningVerification(file_data, app_data, user_data, dest_language, index, intermediate_language=intermediate_language)
	except:
		pass
	else:
		check_failed1 = True
		
	utils.addFluencyVerification(file_data, app_data, user_data, dest_language, index)
	utils.addUserLearningLanguage(user_data, app_data, 'English')
	try:
		utils.addFluencyVerification(file_data, app_data, user_data, dest_language, index, intermediate_language=intermediate_language)
	except:
		pass
	else:
		check_failed1 = True
	
	# ASSERT
	pprint(file_data)
	pprint(user_data)
	if check_failed1:
		msg = "Test add meaning verification unexpectedly succeeded for language \"Spanish\""
		raise Exception(msg)
	if check_failed2:
		msg = "Test add fluency verification unexpectedly succeeded for learning language \"English\""
		raise Exception(msg)
	
def test_add_translation():
	# ARRANGE
	file_data = {
		"name": "soc_tp00",
		"strings": [
			{
				"original_japanese": "マックフライポテトのバスケッティング",
				"original_pointer": 142,
				"translations": {}
			}
		]
	}
	app_data = utils.getData("D:\\ecdp\\eCDP-translation\\app_data\\app_data.json")
	utils.addLanguage(app_data, 'Spanish', 'Español', 'El significado es exacto', 'La traducción parece natural')
	user_data = {
		"languages": {
			"learning": [
				"Japanese"
			],
			"fluent": [
				"English"
			]
		},
		"user_translations": {}
	}
	dest_language = "English"
	index = 0
	translation = "Basketing McFries"
	intermediate_language = 'Spanish'
	
	check_failed = False
	
	# ACT
	utils.addTranslation(file_data, app_data, user_data, dest_language, index, translation)
	utils.addTranslation(file_data, app_data, user_data, dest_language, index, translation)
	try:
		utils.addTranslation(file_data, app_data, user_data, dest_language, index, translation, intermediate_language=intermediate_language)
	except:
		pass
	else:
		check_failed = True
	
	# ASSERT
	if file_data != {
		'name': 'soc_tp00',
		'strings': [{
			'original_japanese': 'マックフライポテトのバスケッティング',
			'original_pointer': 142,
			'translations': {
				'English': [
					{
						'fluency_verification': 0,
						'meaning_verification': 0,
						'translation': 'Basketing McFries'
					},
					{
						'fluency_verification': 0,
						'meaning_verification': 0,
						'translation': 'Basketing McFries'
					}
				]
			}
		}]
	}:
		mst = "Test add translation did not work as expected"
		raise Exception(msg)
	if check_failed:
		msg = "Test add translation unexpectedly succeeded for language \"Spanish\""
		raise Exception(msg)

def test_add_user_language():
		# ARRANGE
		app_data = utils.getData("D:\\ecdp\\eCDP-translation\\app_data\\app_data.json")
		user_data = {'languages':{'learning':[],'fluent':[]}}
		language1 = "Japanese"
		language2 = "English"

		# ACT
		utils.addUserFluentLanguage(user_data, app_data, language1)
		result1 = copy.deepcopy(user_data)
		utils.addUserLearningLanguage(user_data, app_data, language1)
		result2 = copy.deepcopy(user_data)
		utils.addUserFluentLanguage(user_data, app_data, language2)
		result3 = copy.deepcopy(user_data)
		utils.addUserLearningLanguage(user_data, app_data, language2)
		result4 = copy.deepcopy(user_data)
		
		# ASSERT
		if result1 != {'languages':{'learning':[],'fluent':[language1]}} or \
			result2 != {'languages':{'learning':[language1],'fluent':[]}} or \
			result3 != {'languages':{'learning':[language1],'fluent':[language2]}} or \
			result4 != {'languages':{'learning':[language1,language2],'fluent':[]}}:
			msg = "Error occurred in test add user language"
			raise Exception(msg)
	
def test_remove_user_language():
	# ARRANGE
	user_data = {'languages':{'learning':['Japanese'],'fluent':['English']}}
	language1 = 'Japanese'
	language2 = 'English'
	
	# ACT
	utils.removeUserLanguage(user_data, language1)
	result1 = copy.deepcopy(user_data)
	utils.removeUserLanguage(user_data, language2)
	result2 = copy.deepcopy(user_data)

	# ASSERT
	if result1 != {'languages':{'learning':[],'fluent':['English']}} or \
		result2 != {'languages':{'learning':[],'fluent':[]}}:
		msg = "Error occurred in test remove user language"
		raise Exception(msg)
	
def test_add_language():
		# ARRANGE
		check_failed = False
		app_data = utils.getData("D:\\ecdp\\eCDP-translation\\app_data\\app_data.json")
		
		# ACT
		utils.addLanguage(app_data, 'Spanish', 'Español', 'El significado es exacto', 'La traducción parece natural')
		try:
			utils.addLanguage(app_data, "English","English","The meaning is accurate", "The translation sounds natural")
		except:
			pass
		else:
			check_failed = True
		
		# ASSERT
		if app_data['languages'][-1] != {
			'native_name':native_name,
			'ISO_name':ISO_name,
			'meaning_verification':meaning_verification,
			'fluency_verification':fluency_verification
			}:
			msg = "Test add language did not succeed for language \"Spanish\""
			raise Exception(msg)
		if check_failed:
			msg = "Test add language unexpectedly succeeded for language \"English\""
			raise Exception(msg)
	
def test_crawl():
		# ARRANGE
		filepath = "D:\\ecdp\\eCDP_i18n_Base\\"
		extension = ".bin"
		exclude = utils.code_files + utils.code_folders + utils.app_files
		
		# ACT
		files = utils.crawl(filepath, extension, exclude=exclude)	
		# files = utils.crawl("D:\\ecdp\\eCDP-translation\\data", ".json", exclude=exclude)
		
		# ASSERT
		correct_files = utils.getData('D:\\ecdp\\eCDP-translation\\app_data\\filenames.txt')
		missing_files = [cf for cf in correct_files if filepath + cf + extension not in files]
		extra_files = [f for f in files if f.replace(filepath, '').replace(extension, '') not in correct_files]

		if missing_files and extra_files:
			msg = "crawl responded with {} missing files and {} unexpected files".format(
				len(missing_files), len(extra_files))
		elif missing_files:
			msg = "{} expected files not found from crawl".format(len(missing_files))
		elif extra_files:
			msg = "{} unexpected files found from crawl".format(len(extra_files))
		else:
			return
			
		raise Exception(msg)

if __name__ == "__main__":
	def run_test(message, fxn, skip=False):
		sleep_time = 1
		if not skip:
			print(message, end=' ... ')
			time.sleep(sleep_time)
			
			try:
				fxn()
			except:
				print('FAIL')
				raise
			else:
				print('SUCCESS')

	run_test('Testing util function crawl', test_crawl, 
		# skip=False)
		skip=True)
	run_test('Testing util function add language', test_add_language, 
		# skip=False)
		skip=True)
	run_test('Testing util function add user language', test_add_user_language, 
		# skip=False)
		skip=True)
	run_test('Testing util function remove user language', test_remove_user_language, 
		# skip=False)
		skip=True)
	run_test('Testing util function add translation', test_add_translation, 
		skip=False)
		# skip=True)
	run_test('Testing util function add verification', test_add_verification, 
		skip=False)
		# skip=True)
