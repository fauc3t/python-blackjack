"""
Created by Nicholas Horn when he was bored on an airplane on his way to San Diego...
Why didn't I just used classes...?

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

def createHands():
	for x in range(0,num_players+1):
		hands.append([])

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

def shuffle(deck):
	for x in range(51,-1,-1):
		temp = deck[x]
		rand = random.randint(0,51)
		deck[x] = deck[rand]
		deck[rand] = temp

	return deck

def deal(num_players):
	for x in range(0,2):
		for y in range(0, (num_players+1)):
			dealCard(y)

def showHands(num_players):
	for x in range(0,num_players+1):
		if(x == 0):
			if reveal_dealer == False:
				print "DEALER: " + str(hands[x][0]) #+ ": " + str(calculateHand(x))
			else:
				print "DEALER: " + str(hands[x]) + ": " + str(calculateHand(x))
		else:
			print "PLAYER " + str(x) + ": " + str(hands[x]) + ": " + str(calculateHand(x))

def dealCard(player_num):
	rand = random.randint(0,len(deck)-1)
	hands[player_num].append(deck[rand])
	deck.pop(rand)

def playOutGame():
	for x in range(0, num_players):
		print "PLAYER " + str(x+1)+ " HIT?"
		line = ""
		while (line.lower()!="n"):
			line = sys.stdin.readline().strip()
			if(line.lower() == "y"):
				dealCard(x+1)
				showHands(num_players)
				if str(calculateHand(x+1)) == "BUST":
					break


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

def getNumAces(player_num):
	num_aces = 0
	for card in hands[player_num]:
		if str(card[0].lower()) == "a":
			num_aces += 1
	return num_aces

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

def cardScore(card):
	try:
		if int(card) > 2 or int(card)<=10:
			return int(card)
	except:
		if card.lower() == "a":
			return 11
		else:
			return 10

def playDealer():
	while calculateHand(0) < max_score:
		dealCard(0)

def findMaxScore():
	max_score = 0
	global max_Score_player_num
	for x in range(0, num_players):
		hand = calculateHand(x+1)
		if hand > max_score:
			max_score = hand
	return max_score


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
