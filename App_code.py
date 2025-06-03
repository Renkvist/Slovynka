import customtkinter as ctk
from PIL import Image
import tkinter as tk
from customtkinter import CTkComboBox
import sqlite3
import re
import random

# --- DB ---
conn = sqlite3.connect('word_base.db')
c = conn.cursor()

# --- Завантаження налаштувань користувача ---
def load_user(user_id=None):
	global current_language, current_interface, font_size, current_theme

	if user_id is None:
		c.execute("SELECT * FROM Users WHERE current = 1")
		row = c.fetchone()
	else:
		c.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
		row = c.fetchone()
		if not row:
			c.execute("""INSERT INTO Users (name, studied_lang, translation_lang, interface_lang, font_size, theme, current) VALUES 
				(?, ?, ?, ?, ?, ?, ?)""", ("User", "ukr", "eng", "eng", 64, 0, 0))
			conn.commit()
			user_id = c.lastrowid
			c.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
			row = c.fetchone()
		c.execute("UPDATE Users SET current = 0")
		c.execute("UPDATE Users SET current = 1 WHERE user_id = ?", (user_id,))
		conn.commit()

	if row:
		current_language = row[4]
		font_size = row[5]
		current_theme = "dark" if row[6] == 1 else "light"
		current_interface = load_interface_texts(current_language)

		ctk.set_appearance_mode(current_theme)
		update_texts()
		update_users()				
		apply_font_size()









# --- Клас для зручної роботи з елементами ---
class LabeledWidget:
	def __init__(self, widget, label_id, add_text1, add_text2):
		self.widget = widget
		self.label_id = label_id
		self.add_text1 = add_text1
		self.add_text2 = add_text2

	def update_text(self, text):
		self.widget.configure(text=text)

interface_elements = []
user_elements = []
all_buttons = []







# --- Функція для завантаження текстів ---
def load_interface_texts(language_code):
	c.execute("SELECT label_id, label FROM Interface_labels WHERE language = ? ORDER BY label_id", (language_code,))
	results = c.fetchall()
	max_id = max(row[0] for row in results)
	labels = [""] * (max_id + 1)
	for label_id, label in results:
		labels[label_id] = label
	return labels








# --- Стартові налаштування ---
current_language = "ukr"
current_interface = load_interface_texts(current_language)
font_size = 64


# --- Зовнішній вигляд ---
ctk.set_default_color_theme("blue")

def center_window(window, width, height):
	screen_width = window.winfo_screenwidth()
	screen_height = window.winfo_screenheight()

	x = (screen_width // 2) - (width // 2)
	y = (screen_height // 2) - (height // 2)

	window.geometry(f"{width}x{height}+{x}+{y}")

root = ctk.CTk()
root.title("Словинка")
app_width = 1260
app_height = 720
center_window(root, app_width, app_height)

# --- Стилі ---
font_sizes = {63: 20, 64: 25, 65: 30}
font_names = {label_id: current_interface[label_id] if label_id < len(current_interface) else f"Size {size}"
	for label_id, size in font_sizes.items()}
reverse_font_names = {v: k for k, v in font_names.items()}
TITLE_FONT = ctk.CTkFont(size=30, weight="bold")
BUTTON_FONT = ctk.CTkFont(size=font_sizes[font_size])
GAME_BUTTON_FONT = ctk.CTkFont(size=50, weight="bold")

# --- Фрейми ---
frames = {}
for name in ["menu", "category1", "category2", "category3", "category4", "settings", "pos", "cat_13",
	"cat_16", "cat_17", "cat_19", "cat_29", "users", "game"]:	# Тут додавати назву фрейму
	frames[name] = ctk.CTkFrame(root)
	frames[name].place(relwidth=1, relheight=1)

current_frame = frames["menu"]
previous_frame = None

def show_frame(frame):
	global previous_frame
	if frame != frames["settings"]:
		previous_frame = frame
	frame.tkraise()

def open_game_frame(label_id):
	global game_wordlist_ukr, game_wordlist_eng, game_title
	game_wordlist_ukr = []
	game_wordlist_eng = []

	if not game_labels:
		create_game_labels(label_id)

	c.execute("""SELECT word FROM Ukrainian WHERE subcategory = ? OR (subcategory IS NULL AND category = ?)""", (label_id, label_id))
	game_wordlist_ukr = [row[0] for row in c.fetchall()]

	# Отримання англійських слів
	c.execute("""SELECT word FROM English WHERE subcategory = ? OR (subcategory IS NULL AND category = ?)""", (label_id, label_id))
	game_wordlist_eng = [row[0] for row in c.fetchall()]

	show_frame(frames["game"])
	update_game_labels(label_id)







# --- Оновлення текстів ---
def update_texts():
	global font_names, reverse_font_names
	for item in interface_elements:
		try:
			item.update_text(item.add_text2+current_interface[item.label_id]+item.add_text1)
		except IndexError:
			pass
	font_names = {label_id: current_interface[label_id] for label_id, size in font_sizes.items()}
	reverse_font_names = {v: k for k, v in font_names.items()}
	font_combo.set(current_interface[font_size])
	font_combo.configure(values=list(font_names.values()))
	lang_combo.set(current_language)


def update_game_labels(label_id):
	all_ukr = game_wordlist_ukr[:6] + [""] * (6 - len(game_wordlist_ukr))
	all_eng = game_wordlist_eng[:6] + [""] * (6 - len(game_wordlist_eng))

	combined = all_ukr[:3] + all_eng[:3] + all_ukr[3:] + all_eng[3:]
	for i in range(12):
		game_labels[i].configure(text=combined[i])


# --- Розмір шрифту ---
def apply_font_size():
	global BUTTON_FONT
	size = font_sizes[font_size]
	BUTTON_FONT.configure(size=size)
	TITLE_FONT.configure(size=size + 5, weight="bold")
	GAME_BUTTON_FONT.configure(size=size * 2, weight="bold")
	for btn in all_buttons:
		if btn._text != "":
			btn.configure(width=size * 14, height=60 + (size - 25) * 2 )
		else:
			pass

# --- Зміна користувача ---
def select_user(user_id):
	load_user(user_id)
	show_frame(frames["menu"])

def update_users():
	for i in range(3):
		user_id = i+1
		c.execute("SELECT name FROM Users WHERE user_id = ?", (user_id,))
		text = c.fetchone()[0]
		user_elements[user_id-1].update_text(text)

def rename_user(new_name):
	c.execute("UPDATE Users SET name = ? WHERE current = 1", (new_name,))
	conn.commit()
	entry.delete(tk.ANCHOR, tk.END)
	update_users()

# --- Зміна мови інтерфейсу ---
def change_language(language_code):
	global current_language, current_interface
	current_language = language_code
	current_interface = load_interface_texts(current_language)
	update_texts()
	c.execute("UPDATE Users SET interface_lang = ? WHERE current = 1", (language_code,))
	conn.commit()

# --- Зміна шрифту ---
def change_font(selected_label):
	selected_id = reverse_font_names[selected_label]
	new_size = font_sizes[selected_id]

	global font_size
	font_size = selected_id
	apply_font_size()
	c.execute("UPDATE Users SET font_size = ? WHERE current = 1", (font_size,))
	conn.commit()

# --- Тема ---
def toggle_theme(mode):
	global current_theme
	current_theme = mode
	ctk.set_appearance_mode(mode)
	c.execute("UPDATE Users SET theme = ? WHERE current = 1", (1 if mode == "dark" else 0,))
	conn.commit()









# --- Створення елементів ---
def create_labeled_label(frame, label_id, font, pady=10, add_text1="", add_text2=""):
	lbl = ctk.CTkLabel(frame, text=add_text2+current_interface[label_id]+add_text1, font=font)
	lbl.pack(pady=pady)
	interface_elements.append(LabeledWidget(lbl, label_id, add_text1, add_text2))
	return lbl

def create_labeled_button(frame, label_id, command=None, pady=5, add_text1="", add_text2=""):
	global btn
	btn = ctk.CTkButton(frame, text=add_text2+current_interface[label_id]+add_text1, font=BUTTON_FONT, width=350, height=60, command=command)
	btn.pack(pady=pady)
	interface_elements.append(LabeledWidget(btn, label_id, add_text1, add_text2))
	all_buttons.append(btn)
	return btn

left_icon = ctk.CTkImage(Image.open("left_arrow.png"), size=(50, 50))
right_icon = ctk.CTkImage(Image.open("right_arrow.png"), size=(50, 50))
def create_nav_button(frame, direction, target_frame):
	btn = ctk.CTkButton(
		frame, text="", image=left_icon, width=60, height=60, command=lambda: show_frame(frames[target_frame])
	)
	if direction == "left":
		btn.place(relx=0.25, rely=0.5, anchor="w")
		btn.configure(image=left_icon)
	elif direction == "right":
		btn.place(relx=0.75, rely=0.5, anchor="e")
		btn.configure(image=right_icon)

gear_icon = ctk.CTkImage(Image.open("gear.png"), size=(30, 30))
def create_settings_button(frame):
	btn = ctk.CTkButton(frame, text="", image=gear_icon, width=60, height=60, command=lambda: show_frame(frames["settings"]))
	btn.place(relx=0.94, rely=0.02)








# --- Меню ---
c.execute("SELECT name FROM Users WHERE current = ?", (1,))
text = c.fetchone()[0]
create_labeled_label(frames["menu"], 0, TITLE_FONT, 20, add_text1=text)
create_labeled_button(frames["menu"], 12, lambda: show_frame(frames["pos"]))
create_labeled_button(frames["menu"], 1, lambda: show_frame(frames["category1"]))
create_labeled_button(frames["menu"], 61, lambda: show_frame(frames["users"]), 20)
create_labeled_button(frames["menu"], -1, root.quit, 20)
create_settings_button(frames["menu"])

# --- Користувачі ---
user_name_var = ctk.StringVar()
create_labeled_label(frames["users"], 61, TITLE_FONT, 20)
for i in range(3):
	c.execute("SELECT name FROM Users WHERE user_id = ?", (i+1,))
	text = c.fetchone()[0]
	create_labeled_button(frames["users"], -2, command=lambda i=i: load_user(i+1), pady=10, add_text1=text)
	user_elements.append(LabeledWidget(btn, text, "", ""))

create_labeled_label(frames["users"], 56, TITLE_FONT, 10)
entry = ctk.CTkEntry(frames["users"], textvariable=user_name_var, width=250, font=BUTTON_FONT)
entry.pack(pady=10)
create_labeled_button(frames["users"], 62, lambda: rename_user(user_name_var.get()), 10)
create_labeled_button(frames["users"], 6, lambda: show_frame(frames["menu"]), 20)
create_settings_button(frames["users"])

# --- Частини мови ---
create_labeled_label(frames["pos"], 12, TITLE_FONT, 20)
create_labeled_button(frames["pos"], 2, lambda: open_game_frame(2))
create_labeled_button(frames["pos"], 3, lambda: open_game_frame(2))
create_labeled_button(frames["pos"], 4, lambda: open_game_frame(4))
create_labeled_button(frames["pos"], 5, lambda: open_game_frame(5))
create_labeled_button(frames["pos"], 6, lambda: show_frame(frames["menu"]), 20)
create_settings_button(frames["pos"])

# --- Категорії ---
create_labeled_label(frames["category1"], 1, TITLE_FONT, 20, " (1/4)")
create_labeled_button(frames["category1"], 13, lambda: show_frame(frames["cat_13"]))
create_labeled_button(frames["category1"], 14, lambda: open_game_frame(14))
create_labeled_button(frames["category1"], 15, lambda: open_game_frame(15))
create_labeled_button(frames["category1"], 16, lambda: show_frame(frames["cat_16"]))
create_labeled_button(frames["category1"], 17, lambda: show_frame(frames["cat_17"]))
create_labeled_button(frames["category1"], 18, lambda: open_game_frame(18))
create_labeled_button(frames["category1"], 6, lambda: show_frame(frames["menu"]), 20)
create_nav_button(frames["category1"], "right", "category2")
create_settings_button(frames["category1"])


create_labeled_label(frames["category2"], 1, TITLE_FONT, 20, " (2/4)")
create_labeled_button(frames["category2"], 19, lambda: show_frame(frames["cat_19"]))
create_labeled_button(frames["category2"], 20, lambda: open_game_frame(20))
create_labeled_button(frames["category2"], 21, lambda: open_game_frame(21))
create_labeled_button(frames["category2"], 22, lambda: open_game_frame(22))
create_labeled_button(frames["category2"], 23, lambda: open_game_frame(23))
create_labeled_button(frames["category2"], 24, lambda: open_game_frame(24))
create_labeled_button(frames["category2"], 6, lambda: show_frame(frames["menu"]), 20)
create_nav_button(frames["category2"], "left", "category1")
create_nav_button(frames["category2"], "right", "category3")
create_settings_button(frames["category2"])


create_labeled_label(frames["category3"], 1, TITLE_FONT, 20, " (3/4)")
create_labeled_button(frames["category3"], 25, lambda: open_game_frame(25))
create_labeled_button(frames["category3"], 26, lambda: open_game_frame(26))
create_labeled_button(frames["category3"], 27, lambda: open_game_frame(27))
create_labeled_button(frames["category3"], 28, lambda: open_game_frame(28))
create_labeled_button(frames["category3"], 29, lambda: show_frame(frames["cat_29"]))
create_labeled_button(frames["category3"], 30, lambda: open_game_frame(30))
create_labeled_button(frames["category3"], 6, lambda: show_frame(frames["menu"]), 20)
create_nav_button(frames["category3"], "left", "category2")
create_nav_button(frames["category3"], "right", "category4")
create_settings_button(frames["category3"])


create_labeled_label(frames["category4"], 1, TITLE_FONT, 20, " (4/4)")
create_labeled_button(frames["category4"], 31, lambda: open_game_frame(31))
create_labeled_button(frames["category4"], 32, lambda: open_game_frame(32))
create_labeled_button(frames["category4"], 33, lambda: open_game_frame(33))
create_labeled_button(frames["category4"], 34, lambda: open_game_frame(34))
create_labeled_button(frames["category4"], 35, lambda: open_game_frame(35))
create_labeled_button(frames["category4"], 36, lambda: open_game_frame(36))
create_labeled_button(frames["category4"], 6, lambda: show_frame(frames["menu"]), 20)
create_nav_button(frames["category4"], "left", "category3")
create_settings_button(frames["category4"])

# --- Підкатегорії ---
create_labeled_label(frames["cat_13"], 13, TITLE_FONT, 20)
create_labeled_button(frames["cat_13"], 37, lambda: open_game_frame(37))
create_labeled_button(frames["cat_13"], 38, lambda: open_game_frame(38))
create_labeled_button(frames["cat_13"], 39, lambda: open_game_frame(39))
create_labeled_button(frames["cat_13"], 40, lambda: open_game_frame(40))
create_labeled_button(frames["cat_13"], 41, lambda: open_game_frame(41))
create_labeled_button(frames["cat_13"], 42, lambda: open_game_frame(42))
create_labeled_button(frames["cat_13"], 43, lambda: open_game_frame(43))
create_labeled_button(frames["cat_13"], 6, lambda: show_frame(frames["category1"]), 20)
create_settings_button(frames["cat_13"])

create_labeled_label(frames["cat_16"], 16, TITLE_FONT, 20)
create_labeled_button(frames["cat_16"], 44, lambda: open_game_frame(44))
create_labeled_button(frames["cat_16"], 45, lambda: open_game_frame(45))
create_labeled_button(frames["cat_16"], 46, lambda: open_game_frame(46))
create_labeled_button(frames["cat_16"], 6, lambda: show_frame(frames["category1"]), 20)
create_settings_button(frames["cat_16"])

create_labeled_label(frames["cat_17"], 17, TITLE_FONT, 20)
create_labeled_button(frames["cat_17"], 47, lambda: open_game_frame(47))
create_labeled_button(frames["cat_17"], 48, lambda: open_game_frame(48))
create_labeled_button(frames["cat_17"], 49, lambda: open_game_frame(49))
create_labeled_button(frames["cat_17"], 50, lambda: open_game_frame(50))
create_labeled_button(frames["cat_17"], 6, lambda: show_frame(frames["category1"]), 20)
create_settings_button(frames["cat_17"])

create_labeled_label(frames["cat_19"], 19, TITLE_FONT, 20)
create_labeled_button(frames["cat_19"], 51, lambda: open_game_frame(51))
create_labeled_button(frames["cat_19"], 52, lambda: open_game_frame(52))
create_labeled_button(frames["cat_19"], 53, lambda: open_game_frame(53))
create_labeled_button(frames["cat_19"], 54, lambda: open_game_frame(54))
create_labeled_button(frames["cat_19"], 55, lambda: open_game_frame(55))
create_labeled_button(frames["cat_19"], 6, lambda: show_frame(frames["category2"]), 20)
create_settings_button(frames["cat_19"])

create_labeled_label(frames["cat_29"], 29, TITLE_FONT, 20)
create_labeled_button(frames["cat_29"], 57, lambda: open_game_frame(57))
create_labeled_button(frames["cat_29"], 58, lambda: open_game_frame(58))
create_labeled_button(frames["cat_29"], 59, lambda: open_game_frame(59))
create_labeled_button(frames["cat_29"], 60, lambda: open_game_frame(60))
create_labeled_button(frames["cat_29"], 6, lambda: show_frame(frames["category3"]), 20)
create_settings_button(frames["cat_29"])

# --- Налаштування ---
create_labeled_label(frames["settings"], 8, TITLE_FONT, 20)
create_labeled_label(frames["settings"], 9, BUTTON_FONT)
font_combo = CTkComboBox(frames["settings"], values=list(font_names.values()), command=change_font)
font_combo.set(font_names[font_size])
font_combo.pack(pady=5)

create_labeled_label(frames["settings"], 10, BUTTON_FONT)
frame_theme = ctk.CTkFrame(frames["settings"], fg_color="transparent")
frame_theme.pack(pady=5)

sun_icon = ctk.CTkImage(Image.open("sun.png"), size=(50, 50))
moon_icon = ctk.CTkImage(Image.open("moon.png"), size=(40, 40))
ctk.CTkButton(frame_theme, text="", image=sun_icon, width=100, height=60, command=lambda: toggle_theme("light")).pack(side="left", padx=20)
ctk.CTkButton(frame_theme, text="", image=moon_icon, width=100, height=60, command=lambda: toggle_theme("dark")).pack(side="right", padx=20)

create_labeled_label(frames["settings"], 11, BUTTON_FONT)
language_var = ctk.StringVar()
lang_combo = CTkComboBox(frames["settings"], values=["ukr", "eng"], command=change_language, variable=language_var)
lang_combo.set(current_language)
lang_combo.pack()

create_labeled_button(frames["settings"], 6, lambda: show_frame(previous_frame or frames["menu"]), 20)









# --- Гра ---
game_labels = []
game_word_buttons = {}
buttons_pressed, buttons_left = [], []
words_left, words_built = [], []
def create_game_labels(label_id):
	global game_labels, game_title, center_frame, button_frame, keyboard_frame

	game_title = create_labeled_label(frames["game"], label_id, TITLE_FONT, 15, add_text1="", add_text2="")
	center_frame = ctk.CTkFrame(frames["game"])
	center_frame.pack(expand=True)

	for row_index in range(4):
		if row_index == 2:
			pady_value = (15, 0)
		else:
			pady_value = (5, 0)
		row_frame = ctk.CTkFrame(center_frame)
		row_frame.pack(pady=pady_value)
		for col_index in range(3):
			label_index = row_index * 3 + col_index
			label = ctk.CTkLabel(row_frame, text="", font=BUTTON_FONT, width=150)
			label.pack(side="left", padx=10)
			game_labels.append(label)

	create_settings_button(frames["game"])

	button_frame = ctk.CTkFrame(frames["game"])
	button_frame.pack(pady=20)

	start_button = create_labeled_button(button_frame, 66, command=show_keyboard)
	game_back_button = create_labeled_button(button_frame, 6, command=lambda: show_frame(frames["menu"]))

	keyboard_frame = ctk.CTkFrame(frames["game"])



class GameLetterButton(ctk.CTkButton):
	def __init__(self, master, letter, num, *args, **kwargs):
		super().__init__(master, text=letter, *args, **kwargs)
		self.letter = letter
		self.num = num
		self.configure(command=self.on_click)

	def on_click(self):
		letter_entry.configure(state="normal")
		letter_entry.insert("end", self.letter)
		letter_entry.configure(state="readonly")
		self.configure(state="disabled", fg_color="gray", text_color="black")
		buttons_pressed.append(self.num)
		check_word_validity()


total_buttons = 16
def generate_letter_buttons():
	global letter_entry, check_button, reset_button, chosen_word, original_fg, original_text_color, words_left
	if not game_wordlist_ukr:
		return

	keyboard_frame.pack_forget()
	for btn in game_word_buttons:
		btn.destroy()
	game_word_buttons.clear()

	keyboard_frame.pack(pady=20)

	# 1. Обрати 1 слово гарантовано
	words_left = game_wordlist_ukr[:6]
	chosen_word = random.choice(words_left)
	letters = list(chosen_word)

	# 2. Літери з інших 5 слів — у left_letters
	other_words = [w for w in words_left if w != chosen_word]
	left_letters = [char for word in other_words for char in word]

	# 3. Загальна кількість кнопок
	empty_slots = total_buttons - len(letters)

	# 4. Доповнити до 16 випадковими літерами з left_letters
	letters += left_letters[:empty_slots]

	# 5. Перемішати всі літери
	random.shuffle(letters)

	# 6. Створити кнопки 4x4
	for row in range(4):
		row_frame = ctk.CTkFrame(keyboard_frame)
		row_frame.pack()
		for col in range(4):
			idx = row * 4 + col
			letter = letters[idx] if idx < len(letters) else ""
			btn = GameLetterButton(row_frame, letter=letter, num=idx, font=GAME_BUTTON_FONT, width=80, height=80)
			btn.pack(side="left", padx=5, pady=5)
			game_word_buttons.update({idx: btn})

	# Entry справа від сітки
	letter_entry = ctk.CTkEntry(frames["game"], font=BUTTON_FONT, width=300, height=60, justify="center", state="readonly")
	letter_entry.place(relx=0.82, rely=0.55, anchor="center")  # регулюй relx/rely

	# Кнопка галочка під Entry
	check_button = ctk.CTkButton(frames["game"], text="✔", font=TITLE_FONT, command=submit_word, state="disabled",
		fg_color="gray", text_color="black", width=80, height=60)
	check_button.place(relx=0.77, rely=0.65, anchor="center")

	# Кнопка хрестик під галочкою
	reset_button = ctk.CTkButton(frames["game"], text="✖", font=TITLE_FONT, command=reset_letters, width=80, height=60)
	reset_button.place(relx=0.87, rely=0.65, anchor="center")
	original_fg = reset_button.cget("fg_color")
	original_text_color = reset_button.cget("text_color")


def show_keyboard():
	button_frame.pack_forget()  
	generate_letter_buttons()
	apply_font_size()

def check_word_validity():
	entered = letter_entry.get()
	if entered in game_wordlist_ukr[:6]:
		check_button.configure(state="normal", fg_color=original_fg, text_color=original_text_color)
	else:
		check_button.configure(state="disabled", fg_color="gray", text_color="black")

def field_update(built_word=None):
	global chosen_word

	# 1. Зібрати літери з активних кнопок
	available_letters = [btn.cget("text") for btn in game_word_buttons.values() if btn.cget("state") == "normal"]

    # 2. Визначити найзручніше слово
	temp_letters = available_letters.copy()
	def letters_needed(word):
		need = 0
		for letter in word:
			if letter in temp_letters:
				temp_letters.remove(letter)
			else:
				need += 1
		return need

	chosen_word = min(words_left, key=letters_needed)
	print(chosen_word, available_letters)
	# 3. Сформувати набір із букв chosen_word + випадкові з інших
	letters = list(chosen_word)
	temp_letters = available_letters.copy()
	for l in letters:
		if l in temp_letters:
			letters.remove(l)
			temp_letters.remove(l)
			print("after removal -", letters)
	
	random.shuffle(letters)
	other_words = [w for w in words_left if w != chosen_word]
	left_letters = [char for word in other_words for char in word]
	random.shuffle(left_letters)

	# total_buttons = 16 - len(buttons_pressed)
	empty_slots = len(buttons_pressed) - len(letters)
	letters += left_letters[:empty_slots]
	# random.shuffle(letters)

	# 4. Оновити кнопки
	counter = 0
	for num, b in game_word_buttons.items():
		if num in buttons_pressed:
			idx = counter
			letter = letters[idx] if idx < len(letters) else random.choice(letters)
			b.configure(text=letter)
			b.letter=letter
			counter+=1

	reset_letters()


def reset_letters():
	global buttons_pressed
	letter_entry.configure(state="normal")
	letter_entry.delete(0, "end")
	letter_entry.configure(state="readonly")
	for btn in game_word_buttons.values():
		btn.configure(state="normal", fg_color=original_fg, text_color=original_text_color)
	check_button.configure(state="disabled", fg_color="gray", text_color="black")
	buttons_pressed.clear()

def submit_word():
	built_word = letter_entry.get()
	print("Submitted:", built_word)
	words_built.append(built_word)
	words_left.remove(built_word)
	if built_word:
		for lbl in game_labels:
			if lbl.cget("text") == built_word:
				lbl.configure(text_color="green")
				break
	if words_left == []:
		reset_letters()
		keyboard_frame.pack_forget()
		center_frame.pack_forget()
		letter_entry.pack_forget()
		check_button.pack_forget()
		reset_button.pack_forget()
		button_frame.pack(pady=20)
	else: field_update(built_word)




# --- Запуск ---
load_user()
apply_font_size()
show_frame(frames["menu"])
root.mainloop()
conn.close()
