#UNO

from random import choice
from random import randint
from time import sleep

def makingFancy(string):
	list1 = list()
	output = str()
	for ch in string:
		list1.append(ch)
	for i in range(len(list1)):
		if i == 0:
			output += list1[i].upper()
		else:
			output += list1[i].lower()
	return output

class Uno:

	def __init__(self):
		self.shouldPlay = bool()
		self.compShouldPlay = bool()
		self.haveTaken = False
		self.choice = int()
		self.playerInven = list()
		self.compInven = list()
		self.playerCard = str()
		self.playerColor = str()
		self.compCard = str()
		self.compColor = str()
		self.cards = {
		'1' : 1,
		'2' : 2,
		'3' : 3,
		'4' : 4,
		'5' : 5,
		'6' : 6,
		'7' : 7,
		'8' : 8,
		'9' : 9,
		'Skip' : 10,
		'Reverse' : 11,
		'+4' : 12,
		'+2' : 13,
		'Color Change' : 14
		}
		self.colors = {
		'Red' : 1,
		'Blue' : 2,
		'Green' : 3,
		'Yellow' : 4
		}
		self.specialCards = ['+4', 'Color Change']
		self.plusCard = ['+2', '+4']
		self.skipCards = ['Skip', 'Reverse']
		self.DELAY = 1

	def compPlayCard(self):
		cardsNormal = list()
		compColors = list()
		compCards = list()
		cardsSpecial = list()
		for ch in self.compInven:
			if len(ch) == 1:
				cardsSpecial.append(ch)
			else:
				cardsNormal.append(ch)
		for i in range(len(cardsNormal)):
			compColors.append(cardsNormal[i][1])
			compCards.append(cardsNormal[i][0])
		if self.topColor in compColors or self.topColor == 'None':
			if len(cardsSpecial) != 0:
				compChoice = randint(0, 1)
			else:
				compChoice = 0
		else:
			compChoice = 2
		if compChoice == 0:
			cardPlayed = ['None', 'None']
			if self.topColor != 'None':
				while cardPlayed[1] != self.topColor:
					cardPlayed = choice(cardsNormal)
				compCard = cardPlayed[0]
				compColor = cardPlayed[1]
				print("The computer played {} {}".format(compCard, compColor))
				self.compInven.remove(cardPlayed)
				return compCard, compColor
			else:
				cardPlayed = choice(cardsNormal)
				self.compInven.remove(cardPlayed)
				compCard = cardPlayed[0]
				compColor = cardPlayed[1]
				return compCard, compColor
		elif compChoice == 2:
			compCard , compColor = self.takeCard()
			if compColor == self.topColor:
				print("The computer played {} {}".format(compCard, compColor))
				return compCard, compColor
			elif compColor != self.topColor:
				print("The computer took one card from the stack but it was not good .")
				self.compInven.append([compCard, compColor])
				return 'None', 'None'
			elif compCard in self.specialCards:
				return compCard, compColor
			else:
				pass
		else:
			cardPlayed = choice(cardsSpecial)
			compColor = 'None'
			compCard = cardPlayed[0]
			print("The computer played {}".format(compCard))
			self.compInven.remove(cardPlayed)
			return compCard, compColor

	def fillInven(self, inven, NO_OF_CARDS):
		cards = list(self.cards.keys())
		colors = list(self.colors.keys())
		for i in range(NO_OF_CARDS):
			card = choice(cards)
			if card in self.specialCards:
				inven.append([card])
			else:
				inven.append([card, choice(colors)])

	def plusTwo(self, inven):
		self.fillInven(inven, 2)

	def takeCard(self):
		cards = list(self.cards.keys())
		color = list(self.colors.keys())
		card = choice(cards)
		if card in self.specialCards:
			return card, 'None'
		else:
			return card, choice(color)

	def getInput(self):
		self.showInstructions()
		self.choice = self.getPlayerInput(1, len(self.playerInven))

	def showWarning(self):
		print("Invalid input !!")

	def showInstructions(self):
		print("Enter the card index to select the card .")
		if not self.haveTaken:
			print("If you don't have a valid card then enter 100")

	def getPlayerInput(self, lowerLimit, upperLimit):
		choice = int()
		while True:
			try:
				choice = int(input("Enter : "))
				if choice >= lowerLimit and choice <= upperLimit:
					return choice
				elif choice == 100:
					if not self.haveTaken:
						print("You are now taking a card from the stack .")
					return choice
				else:
					self.showWarning()
			except ValueError:
				self.showWarning()
		return choice

	def stopGame(self):
		sleep(self.DELAY)

	def showInven(self, list_of_cards):
		count = 1
		for ch in list_of_cards:
			if len(ch) == 2:
				print("{} : {} {}".format(count, ch[0], ch[1]))
			else:
				print("{} : {} ".format(count, ch[0]))
			count += 1

	def plusFour(self, inven):
		self.fillInven(inven, 4)

	def playerColorChange(self):
		colors = ['red', 'blue', 'green', 'yellow']
		print("Enter the new color please .")
		while True:
			color = str(input("Enter :"))
			if color.lower() in colors:
				print("You have chosen the color {}".format(makingFancy(color)))
				self.topColor = makingFancy(color)
				self.topCard = 'None'
				break
			else:
				print("Please enter a valid color .")

	def compColorChange(self):
		colors = list(self.colors.keys())
		self.topCard = 'None'
		return choice(colors)

	def generateTop(self):
		cards = list(self.cards.keys())
		cards.remove('Color Change')
		cards.remove('+4')
		colors = list(self.colors.keys())
		topCard = choice(cards)
		topColor = choice(colors)
		return topCard, topColor

	def showTopCard(self):
		print("The top card is {} {}".format(self.topCard, self.topColor))

	def playGame(self):
		print("----------WELCOME----------")
		print("Shuffling......")
		self.stopGame()
		print("Distributing........")
		self.stopGame()
		self.topCard, self.topColor = self.generateTop()
		self.fillInven(self.playerInven, 7)
		self.fillInven(self.compInven, 7)
		while len(self.playerInven) != 0 or len(self.compInven) != 0:
			self.compShouldPlay = True
			if self.shouldPlay:
				while True:
					self.shouldPlay = False
					self.showInven(self.playerInven)
					self.showTopCard()
					self.getInput()
					if self.choice != 100:
						length = len(self.playerInven[self.choice - 1])
						if length == 2:
							self.playerCard = self.playerInven[self.choice - 1][0]
							self.playerColor = self.playerInven[self.choice -1][1]
							if self.topColor == self.playerColor:
								print("You played {} {}".format(self.playerCard, self.playerColor))
								self.playerInven.remove(self.playerInven[self.choice - 1])
								self.topCard = self.playerCard
								if self.playerCard == '+2':
									self.plusTwo(self.compInven)
									print("The computer recieved two cards .")
								if self.playerCard == 'Skip':
									self.shouldPlay = True
									self.compShouldPlay = False
									print("The computer's chance got skipped .")
								if self.playerCard == 'Reverse':
									self.compShouldPlay = False
									self.shouldPlay = True
									print("The computer's chance got skipped .")
								break
							elif self.topCard == self.playerCard:
								print("You played {} {}".format(self.playerCard, self.playerColor))
								self.playerInven.remove(self.playerInven[self.choice - 1])
								self.topCard = self.playerCard
								self.topColor = self.playerColor
								if self.playerCard == '+2':
									self.plusTwo(self.compInven)
									print("The computer recieved two cards .")
								if self.playerCard == 'Skip':
									self.shouldPlay = True
									self.compShouldPlay = False
									print("The computer's chance got skipped .")
								if self.playerCard == 'Reverse':
									self.compShouldPlay = False
									self.shouldPlay = True
									print("The computer's chance got skipped .")
								break
							elif self.topColor == 'None':
								self.topCard = self.playerCard
								self.topColor = self.playerColor
								self.playerInven.remove(self.playerInven[self.choice - 1])
								if self.playerCard == '+2':
									self.plusTwo(self.compInven)
									print("The computer recieved two cards .")
								if self.playerCard == 'Skip':
									self.shouldPlay = True
									self.compShouldPlay = False
									print("The computer's chance got skipped .")
								if self.playerCard == 'Reverse':
									self.compShouldPlay = False
									self.shouldPlay = True
									print("The computer's chance got skipped .")
								break
							else:
								print("Please select a card with the same top color or number .")
						if length == 1:
							self.playerCard = self.playerInven[self.choice- 1][0]
							print("You played {}".format(self.playerCard))
							if self.playerCard == 'Color Change':
								self.playerColorChange()
							if self.playerCard == '+4':
								print("The computer recieved four cards .")
								self.plusFour(self.compInven)
							self.playerInven.remove(self.playerInven[self.choice - 1])
							break
					else:
						answers = ['y', 'n']
						if not self.haveTaken:
							card, color = self.takeCard()
							if color == 'None':
								print("You got {}".format(card))
								self.playerInven.append([card])
							else:
								print("You got {} {}".format(card, color))
								self.playerInven.append([card, color])
							print("You have recieved a card if you want to play press Y else press N")
							while True:
								try:
									playerChoice = str(input("Enter :"))
									if playerChoice.lower() in answers:
										break
									else:
										self.showWarning()
								except ValueError:
									self.showWarning()
							if playerChoice == 'n':
								self.shouldPlay = False
								break
							else:
								self.shouldPlay = True
							self.haveTaken = True
						else:
							print("You have already taken one card .")
							print("If you don't want to play then press N .")
							while True:
								try:
									playerChoice = str(input("Enter :"))
									if playerChoice.lower() in answers:
										break
									else:
										self.showWarning()
								except ValueError:
									self.showWarning()
							if playerChoice.lower() == 'n':
								self.shouldPlay = False
								break
							else:
								print("Ok play .")
								self.shouldPlay = True
			if self.compShouldPlay:
				self.compShouldPlay = False
				if not self.shouldPlay:
					self.haveTaken = False
					self.shouldPlay = True
					self.compCard, self.compColor = self.compPlayCard()
					if self.compCard != 'None':
						self.topCard = self.compCard
						self.topColor = self.compColor
					if self.compColor == 'None':
						if self.compCard == '+4':
							print("Oh no you recieved four cards !!")
							self.plusFour(self.playerInven)
						if self.compCard == 'Color Change':
							self.topColor = self.compColorChange()
							print("The computer chose the color {}".format(self.topColor))
						if self.compCard == 'None':
							pass
					if self.compCard == '+2':
						self.plusTwo(self.playerInven)
						print("You recieved two cards !!")
					if self.compCard == 'Reverse':
						print("Your chance got skipped .")
						self.shouldPlay = False
					if self.compCard == 'Skip':
						print("Your chance got skipped .")
						self.shouldPlay = False

					
