"""
Created by Nicholas Horn while I was bored on an airplane on my way to San Diego
Why didn't I just use classes...?

Adding these comments to test git

"""


import random
import sys
num_players = 1
num_decks = -1
hands = [[]]
deck = []
max_score = 0

reveal_dealer = False
max_Score_player_num = 0

"""
Create a multi dimensional array based on the number of players to keep track of hands.
The dealer is always the 0 index. 
""" 
def createHands():
	for x in range(0,num_players+1):
		hands.append([])

"""
Creates one 52 card deck as a list and returns it.
Examples of cards: 
2H - 2 of Hearts
9S - 9 of Spades
KH - King of Hearts
"""
def createDeck():
	deck = []
	suits = ["H","S","C","D"]
	faces = ["J", "Q", "K","A"]
	for x in range(0,4):
		for y in range (2,15):
			if y<=10:
				card = str(y) + suits[x]
				deck.append(card);
			else:
				deck.append(faces[y-11]+suits[x])
			
	return deck

"""
	Shuffle all cards in the deck. Starts from the last card in the deck and iterates to the first card;
	swapping the card at the current index with a card at a random index.
	I'm pretty positive this is the same algorithm as the python .shuffle() method for lists.
"""
def shuffle(deck):
	for x in range(len(deck)-1,-1,-1):
		temp = deck[x]
		rand = random.randint(0,len(deck)-1)
		deck[x] = deck[rand]
		deck[rand] = temp

	return deck

"""
Begin the game by dealing 2 cards to each player including the dealer by adding the card to the 
player's corresponding hand.
"""
def deal(num_players):
	for x in range(0,2):
		for y in range(0, (num_players+1)):
			dealCard(y)

"""
Prints out all players hands including the dealers (Only shows one card for the dealer)
The dealer's hand is always the 0 index in the 'hands' list.
"""
def showHands(num_players):
	for x in range(0,num_players+1):
		if(x == 0):
			if reveal_dealer == False:
				print "DEALER: " + str(hands[x][0]) #+ ": " + str(calculateHand(x))
			else:
				print "DEALER: " + str(hands[x]) + ": " + str(calculateHand(x))
		else:
			print "PLAYER " + str(x) + ": " + str(hands[x]) + ": " + str(calculateHand(x))

"""
Deal a random card to the corresponding player. 
I don't really know why I programmed it this way, it should really just pop the index 0 card
and give it to the player...
"""
def dealCard(player_num):
	rand = random.randint(0,len(deck)-1)
	hands[player_num].append(deck[rand])
	deck.pop(rand)

"""
Once all players have been dealt cards, the game begins starting with Player 1. 
The player can either hit or hold. Normal BLACKJACK rules apply. 
"""
def playOutGame():
	for x in range(0, num_players):
		print "PLAYER " + str(x+1)+ " HIT? y/n"
		line = ""
		while (line.lower()!="n"):
			line = sys.stdin.readline().strip()
			if(line.lower() == "y"):
				dealCard(x+1)
				showHands(num_players)
				if str(calculateHand(x+1)) == "BUST":
					break

"""
Calculate the score of each players hand and return it. 
This method takes into account any aces in a player's hand which become 1 (from 11) if the player's score
goes over 21. 
If multiple ace's exist, only one ace's value you will be reduced to 1 until it is necessary 
for the next and so on.
"""
def calculateHand(player_num):
	score = 0
	for card in hands[player_num]:
		if(len(card) == 2):
			score += cardScore(card[0])
		else:
			score += 10

	num_aces = getNumAces(player_num)
	if score > 21: 
		for x in range(0,num_aces):
			score -= 10
			if score < 21:
				break
	if score > 21:
		return "BUST"

	return score

"""
Helper method for the calculateHand() method.
Determines the number of ace's in the corresponding player's hand and return it.
"""
def getNumAces(player_num):
	num_aces = 0
	for card in hands[player_num]:
		if str(card[0].lower()) == "a":
			num_aces += 1
	return num_aces

"""
Asks the player how many decks they would like to play with. They can choose any number from 1 to 10. 
If input is incorrect they will be asked again.
"""
def getNumDecks():
	print "HOW MANY DECKS? 1 - 10"
	num_decks = -1
	while num_decks<0:
		try:
			num_decks = int(sys.stdin.readline().strip())
		except:
			num_decks = -1
		if num_decks<1 or num_decks>10:
			num_decks = -1
	return num_decks

"""
Determines the score of a card and returns it.
If a card is from 2-10 it is the face value.
If the card is a face card (Jack, Queen or King) it is 10.
If the card is an Ace, it starts as 11 (seen here) but can eventually be reduced to 1 
	if the player were to go over 21 with it in hand.
"""
def cardScore(card):
	try:
		if int(card) > 2 or int(card)<=10:
			return int(card)
	except:
		if card.lower() == "a":
			return 11
		else:
			return 10

"""
Forces the dealer to play until he either beats the maximum score of the players or BUSTs (goes over 21)
"""
def playDealer():
	while calculateHand(0) < max_score:
		dealCard(0)
"""
Determines the highest score between all players (besides the dealer)
"""
def findMaxScore():
	max_score = 0
	global max_Score_player_num
	for x in range(0, num_players):
		hand = calculateHand(x+1)
		if hand > max_score and hand<=21:
			max_score = hand
	return max_score

"""
This is where the program begins.
Currently only one game is played before exiting, however this can easily be added to continue 
until the user decides to quit.
Also I need to declare a winner at the end.
"""

print "WELCOME TO BLACKJACK"
print "HOW MANY PLAYERS?"

num_players = int(sys.stdin.readline().strip())
createHands()
num_decks = getNumDecks()

for x in range(0, num_decks):
	deck.extend(createDeck())

deck = shuffle(deck)


deal(num_players)
showHands(num_players)

playOutGame()
reveal_dealer = True

print "DEALER'S TURN"
showHands(num_players)
print max_score
print "PRESS ENTER TO PLAY OUT DEALER"
line =sys.stdin.readline()
max_score = findMaxScore()
playDealer()
showHands(num_players)

