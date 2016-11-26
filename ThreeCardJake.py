import random

initialCardsInHand=3

class Card:
	def __init__ (self, rank, suit):
		self.rank=rank
		self.suit=suit

	def __repr__ (self):
		letters={14:'A',13:'K',12:'Q',11:'J'}
		letter=letters.get(self.rank,str(self.rank))
		return letter+self.suit

	def getRank(self):
		return self.rank

	def getSuit(self):
		return self.suit

	def __eq__ (self, other):
		return self.rank == other.rank and self.suit == other.suit

	def __ne__ (self,other):
		return not self.__eq__(other)

class Player:
	def __init__ (self,):
		self.scorePile=[]
		self.hand=[]

	def getMove(self,prizeCard):
		pass

	def addScoreCard(self,scoreCard):
		self.scorePile.append(scoreCard)

	def removeHandCards(self, cards):
		for card in cards:
			self.hand.remove(card)

	def pickCardForHand(self,handCard):
		self.hand.append(handCard)

	def getTotalScore(self):
		return sumCardRanks(self.scorePile)

	def __repr__(self):
		return 'Cards in hand: '+repr(self.hand)+'\nCards in score pile: '+repr(self.scorePile)

class HumanPlayer(Player):
	def getMove(self,prizeCard):
		print repr(self)
		print 'Prize card is: '+repr(prizeCard)
		response=input("What cards would you like to play?")
		cardsToPlay=[]
		for i in range(len(response)):
			char=response[i]
			if char == 'y':
				cardsToPlay.append(self.hand[i])
		return cardsToPlay


class AIPlayer(Player):
	def getMove(self,prizeCard):
		return [self.hand[0]]

def getDeck():
	deck=[Card(rank,suit) for rank in ranks for suit in suits]
	random.shuffle(deck)
	return deck

def sumCardRanks(cards):
	scoreSoFar=0
	for card in cards:
		scoreSoFar += card.getRank()
	return scoreSoFar

def deal(deck):
	cardsFor1=[]
	cardsFor2=[]
	for i in range(initialCardsInHand-1):
		cardsFor1.append(deck.pop())
		cardsFor2.append(deck.pop())
	return cardsFor1,cardsFor2

def doMove(deck,player1,player2):
	if len(deck)>=3:
		player1.pickCardForHand(deck.pop())
		player2.pickCardForHand(deck.pop())
	playForScoreCard(deck.pop(),player1,player2)

def playForScoreCard(prizeCard,player1,player2):
	cards1=player1.getMove(prizeCard)
	cards2=player2.getMove(prizeCard)
	sum1=sumCardRanks(cards1)
	sum2=sumCardRanks(cards2)
	print "Player 1 played: "+repr(cards1)+' for a total of: '+str(sum1)
	print "Player 2 played: "+repr(cards2)+' for a total of: '+str(sum2)
	if sum1==sum2:
		player1.removeHandCards(cards1)
		player2.removeHandCards(cards2)
	elif sum1>sum2:
		player1.removeHandCards(cards1)
		player1.addScoreCard(prizeCard)
	else:
		player2.removeHandCards(cards2)
		player2.addScoreCard(prizeCard)
	

def main():
	deck=getDeck()

	player1=HumanPlayer()
	player2=HumanPlayer()

	cardsToAdd1,cardsToAdd2=deal(deck)
	for card in cardsToAdd1:
		player1.pickCardForHand(card)
	for card in cardsToAdd2:
		player2.pickCardForHand(card)

	while len(deck)>0:
		doMove(deck,player1,player2)
		print "Length of deck: "+str(len(deck))

	print "Player 1 got: "+str(player1.getTotalScore())
	print "Player 2 got: "+str(player2.getTotalScore())

ranks=range(2,15)
suits='cdhs'
main()

# print(sortedDeck)
# print len(sortedDeck)


