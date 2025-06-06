import sqlite3
import stanza


conn = sqlite3.connect('word_base.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Interface_labels
	(label_id INTEGER,
	label TEXT,
	language TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS Ukrainian
	(word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT,
	part_of_speech TEXT,
	category TEXT,
	subcategory TEXT,
	add_info TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS English
	(word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT,
	part_of_speech TEXT,
	category TEXT,
	subcategory TEXT,
	add_info TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS Users
	(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	studied_lang TEXT,
	translation_lang TEXT,
	interface_lang TEXT,
	font_size INTEGER,
	theme INTEGER,
	current INTEGER)""")

c.execute("""CREATE TABLE IF NOT EXISTS User_progress
	(user_id INTEGER,
	word_id INTEGER,
	word TEXT,
	lang TEXT)""")


####################################

interface_ukr = [
	"Вітаю, ",					# 0
	"Категорії",				# 1
	"Іменники",					# 2
	"Дієслова",					# 3
	"Прикметники",				# 4
	"Прислівники",				# 5
	"Назад",					# 6
	"Підкатегорія",				# 7
	"Налаштування",				# 8
	"Розмір шрифту",			# 9
	"Тема",						# 10
	"Мова інтерфейсу",			# 11
	"Частини мови",				# 12
	"Людина",					# 13
	"Дім",						# 14
	"Технології",				# 15
	"Місто й село",				# 16
	"Побут",					# 17
	"Навчання",					# 18
	"Проведення часу",			# 19
	"Час",						# 20
	"Подорожі",					# 21
	"Географічні назви",      	# 22
	"Покупки",					# 23
	"Продукти",					# 24
	"Одиниці вимірювання",		# 25
	"Гроші",					# 26
	"Ресторан та страви",		# 27
	"Здоров'я",					# 28
	"Природа",					# 29
	"Традиції, звичаї, свята",	# 30
	"Числа",					# 31
	"Кольори",					# 32
	"Питальні слова",			# 33
	"Займенники",				# 34
	"Комунікативні фрази",		# 35
	"Службові частини мови",	# 36
	"Особиста інформація",		# 37
	"Країна, мова",				# 38
	"Зовнішність і характер",	# 39
	"Частини тіла",				# 40
	"Професії",					# 41
	"Сім'я та родина",			# 42
	"Інші особи",				# 43
	"Напрямки",					# 44
	"Місця",					# 45
	"Транспорт",				# 46
	"Предмети в домі",			# 47
	"Посуд",					# 48
	"Засоби гігієни",			# 49
	"Одяг, взуття, аксесуари",	# 50
	"Щоденні дії",				# 51
	"Робочий день",				# 52
	"Вільний час і відпочинок",	# 53
	"Спорт",					# 54
	"Рух",						# 55
	"Перейменувати",			# 56
	"Погода",					# 57
	"Рослини",					# 58
	"Домашні тварини",			# 59
	"Природні об'єкти",			# 60
	"Змінити профіль",			# 61
	"Зберегти",					# 62
	"Малий",					# 63
	"Середній",					# 64
	"Великий",					# 65
	"Почати",					# 66
	"Раунд",					# 67
	"чоловічий та жіночий роди",# 68
	"паралельні форми",			# 69
	"однина та множина",		# 70
	"інфінітив та звертання",	# 71
	"місце й напрямок до нього",# 72
	"Кількісні числівники",		# 73
	"Порядкові числівники",		# 74
	"роди однини та множина",	# 75
	"звертання в однині та множині",	# 76
	"",							# -2
	"Вихід"						# -1
]

interface_eng = [
	"Welcome, ",					# 0
	"Categories",					# 1
	"Nouns",						# 2
	"Verbs",						# 3
	"Adjectives",					# 4
	"Adverbs",						# 5
	"Back",							# 6
	"Subcategory",					# 7
	"Settings",						# 8
	"Font Size",					# 9
	"Theme",						# 10
	"Interface language",			# 11
	"Parts of speech",				# 12
	"Person",						# 13
	"Home",							# 14
	"Technology",					# 15
	"City and village",				# 16
	"Everyday life",				# 17
	"Education",					# 18
	"Spending time",				# 19
	"Time",							# 20
	"Traveling",					# 21
	"Geographical names",			# 22
	"Shopping",						# 23
	"Groceries",					# 24
	"Units of measurement",			# 25
	"Money",						# 26
	"Restaurant and food",			# 27
	"Health",						# 28
	"Nature",						# 29
	"Traditions, customs, holidays",# 30
	"Numbers",						# 31
	"Colors",						# 32
	"Question words",				# 33
	"Pronouns",						# 34
	"Communicative phrases",		# 35
	"Functional parts of speech",	# 36
	"Personal information",			# 37
	"Country, language",			# 38
	"Appearance and character",		# 39
	"Parts of the body",			# 40
	"Professions",					# 41
	"Family and relatives",			# 42
	"Other people",					# 43
	"Directions",					# 44
	"Places",						# 45
	"Transport",					# 46
	"Objects in the house",			# 47
	"Dishes",						# 48
	"Hygiene products",				# 49
	"Clothes, shoes, accessories",	# 50
	"Daily activities",				# 51
	"Working day",					# 52
	"Leisure and rest",				# 53
	"Sports",						# 54
	"Movement",						# 55
	"Rename",						# 56
	"Weather",						# 57
	"Plants",						# 58
	"Pets",							# 59
	"Natural objects",				# 60
	"Change profile",				# 61
	"Save",							# 62
	"Small",						# 63
	"Medium",						# 64
	"Big",							# 65
	"Start",						# 66
	"Round",						# 67
	"masculine and feminine genders",	# 68
	"parallel forms",				# 69
	"singular and plural",			# 70
	"infinitive and adressed",		# 71
	"place and direction to it",	# 72
	"Quantitative numerals",		# 73
	"Ordinal numerals",				# 74
	"singular genders and plural",	# 75
	"adressed to singular and plural",	# 76
	"",								# -2
	"Exit"							# -1
]

####################################


# stanza.download('uk')
# nlp = stanza.Pipeline(lang = 'uk', processors = 'tokenize,mwt,pos')
# word_pos = {}

# with open(r"wordlist_ukr.txt", "r", encoding = "utf-8") as data:
# 	global ukr_pos_list
# 	wordlist = data.read().split('\n')

# 	text = ". ".join([f"Це слово: {word}" for word in wordlist]) + "."
# 	doc = nlp(text)

# 	for sentence in doc.sentences:
# 		for token in sentence.words:
# 			if token.text in wordlist:
# 				word_pos[token.text] = token.upos
# 	ukr_pos_list = [word_pos.get(word, "UNKNOWN") for word in wordlist]

# 	for word, pos in zip(wordlist, ukr_pos_list):
# 		c.execute("INSERT INTO Ukrainian (word, part_of_speech) VALUES (?, ?)", (word, pos))


# with open(r"wordlist_eng.txt", "r", encoding = "utf-8") as data:
# 	wordlist = data.read().split('\n')
# 	for word, pos in zip(wordlist, ukr_pos_list):
# 		c.execute("INSERT INTO English (word, part_of_speech) VALUES (?, ?)", (word, pos))

# counter = 0
# for x in range(3):
# 	c.execute("""INSERT INTO Users (name, studied_lang, translation_lang, interface_lang, font_size, theme, current) VALUES
# 	(?, "ukr", "eng", "eng", "64", "0", "0")""", ("User"+str(counter+1),))
# 	counter += 1

# counter = 0
# for x in interface_ukr:
# 	c.execute("INSERT INTO Interface_labels VALUES (?, ?, ?)",
# 	(counter, x, "ukr"))
# 	counter += 1

# counter = 0
# for x in interface_eng:
# 	c.execute("INSERT INTO Interface_labels VALUES (?, ?, ?)",
# 	(counter, x, "eng"))
# 	counter += 1

# (word, part_of_speech, category, subcategory, add_info)

# c.execute("""SELECT * FROM English""")
# table_info1 = c.fetchall()
# conn.close()

# conn = sqlite3.connect('word_base2.db')
# c = conn.cursor()
# c.execute("""SELECT * FROM English""")
# table_info2 = c.fetchall()
# for i, x in enumerate(table_info2):
# 	print(i)
# 	print(x)
# 	if x[1] == table_info1[i][1]:
# 		try:
# 			c.execute("""UPDATE English SET part_of_speech = ?, category = ?, subcategory = ?, add_info = ?
# 				WHERE word = ?""", (table_info1[i][2], table_info1[i][3], table_info1[i][4], table_info1[i][5], table_info1[i][1]))
# 		except:
# 			i += 1
# 			continue


conn.commit()


conn.close()