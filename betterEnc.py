# Making a better encode using the json, random and os modules
# and making it a gui application using the tkinter module

import json
from time import sleep
import random
import os
from tkinter import Tk, Button, Label, Entry, Text, END, StringVar
import ttkbootstrap as ttk

class NoSuchPath(Exception):

	def __init__(self, string):
		pass


class Encode:

	def __init__(self, string, path):
		if not os.path.exists(path):
			raise NoSuchPath('There is no such path , enter a path to a directory')

		self.characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ]
		uppercase_chars = [ch.upper() for ch in self.characters if ch != ' ']
		self.characters.extend(uppercase_chars)

		self.encode_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '"', "'", '|', '/', '\\', '`', '~']
		self.string = str(string)
		self.path = path
		self.depth = random.randint(4, 6)

		self.make_encode_dict()
		self.make_file()
		self.make_decode_dict()
		self.encode()
		self.write()


	def get_depth(self):
		return self.depth

	def get_new_path(self):
		return self.path + '\\' + 'Encoded String File'

	def make_encode_dict(self):
		self.encode_dict = dict()
		used_chars = []
		for ch in self.characters:
			while True:
				char = str()
				for i in range(self.depth):
					char += random.choice(self.encode_chars)
				if char not in used_chars:
					used_chars.append(char)
					break
				else:
					pass
			self.encode_dict[ch] = char

	def make_decode_dict(self):
		self.decode_dict = dict()
		for keys, items in self.encode_dict.items():
			self.decode_dict[items] = keys

	def encode(self):
		self.output = str()
		for ch in self.string:
			if ch in self.characters:
				self.output += self.encode_dict.get(ch)
			else:
				pass

	def write(self):
		with open('encoded_string.txt', 'w') as file:
			file.write(self.output)
		with open('key.json', 'w') as file:
			json.dump(self.decode_dict, file, indent=4, sort_keys=True)

	def make_file(self):
		try:
			os.chdir(self.path)
			os.mkdir('Encoded String File')
			os.chdir(self.path + '\\' + 'Encoded String File')
		except WindowsError as e:
			print("Windows is preventing the making of the file that will contain the encoded strings")


class Decode:

	def __init__(self, path, depth):
		if not os.path.exists(path):
			raise NoSuchPath("Enter a path to directory containing the key and the encoded text")

		os.chdir(path)
		self.list_of_folders = os.listdir(path)
		self.depth = depth

		self.load()
		self.take_content()
		self.give_output()

	def load(self):
		for ch in self.list_of_folders:
			if ch.endswith('.json'):
				self.jsonFile = ch
			if ch.endswith('.txt'):
				self.textFile = ch

	def get_output(self):
		return self.output

	def take_content(self):
		self.string = str()
		self.decode_dict = dict()
		with open(self.textFile, 'r') as file:
			self.string = file.read()
		with open(self.jsonFile, 'r') as file:
			self.decode_dict = json.load(file)

	def give_output(self):
		self.output = str()
		strs = list()
		while self.depth <= len(self.string):
			temp = str()
			for i in range(self.depth):
				temp += self.string[i]
			strs.append(temp)
			self.string = self.string[self.depth:]
		for ch in strs:
			char = self.decode_dict.get(ch)
			if char != None:
				self.output += self.decode_dict.get(ch)
			else:
				pass


class GuiEncoder(Encode):

	def __init__(self):
		self.root = Tk()
		self.root.title("Gui Encoder")
		self.root_size = "500x350"
		self.root.geometry(self.root_size)
		self.font = ("MV BOLI", 17)

		Label(self.root,
			text="Enter a string to encode pls",
			font=self.font).pack()

		self.text_entry = Text(self.root,
			bg="black",
			fg="green",
			relief="raised",
			bd=10,
			width=self.root.winfo_screenmmwidth(),
			font=self.font,
			height=3)

		self.text_entry.pack()

		Label(self.root,
			text="Enter a path to a directorty pls",
			font=self.font).pack()

		self.directtory_path = Entry(self.root,
			bg="black",
			fg="green",
			font=self.font,
			relief="sunken",
			bd=10,
			width=self.root.winfo_screenmmwidth())

		self.directtory_path.pack()

		Button(self.root,
			text="Create Encoded Text",
			font=self.font,
			relief="raised",
			bd=10,
			command=self.go).place(x=500 / 2 - 135,y= 250)

		self.root.mainloop()

	def go(self):
		if os.path.exists(self.directtory_path.get()):
			if os.path.isdir(self.directtory_path.get()):
				super().__init__(self.text_entry.get(1.0, END), self.directtory_path.get())
		else:
			pass


class GUIDecoder(Decode):

	def __init__(self):
		self.root = Tk()
		self.root.title("Decode")
		self.root.geometry("550x350")

		self.text = StringVar(value="The decoded message will appear here")
		self.font = ("Calibri 24 Bold", 20)

		ttk.Label(self.root,
			text="Please enter the path to the encrypted text file \n and pls make sure that there are no other files other than the original\n ones in there .",
			font=("Calibri 24 bold", 18),
			relief="groove",
			border=10,
			background="black",
			foreground="cyan").pack(padx=5, pady=10)

		self.path = ttk.Entry(self.root,
		   width=self.root.winfo_screenmmwidth(),
		   font=self.font,
		   background="dark blue",
		   foreground="dark cyan")

		self.output = ttk.Label(self.root,
			textvariable=self.text,
			font=self.font,
			relief="sunken",
			border=10,
			width=self.root.winfo_screenmmwidth(),
			foreground="cyan",
			background="black")

		self.root.configure(bg="#F0F0F0")
		self.path.pack(pady=10)

		ttk.Button(self.root, text="Submit", command=self.get_text).pack()

		self.output.pack(pady=10)
		self.root.mainloop()

	def get_text(self):
		self.dir_path = self.path.get()
		if(os.path.exists(self.dir_path)):
			list_of_folders = os.listdir(self.path.get())
			for folder in list_of_folders:
				if folder.endswith(".json"):
					with open(self.path.get() + "\\" + folder, 'r') as file:
						json_file = json.load(file)
					keys = json_file.keys()
					self.depth = len(list(keys)[0])
					self.get_output()
		else:
			self.text.set("Please enter a valid path to a directory")
			self.root.after(3000, lambda: self.text.set("The decoded message will appear here"))

	def get_output(self):
		super().__init__(self.path.get(), self.depth)
		self.text.set(super().get_output())
			
