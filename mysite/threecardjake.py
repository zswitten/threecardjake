from flask import Flask, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["DEBUG"] = True

initialCardsInHand=3

class Card:
	def __init__(self, rank, suit):
		self.rank=rank
		self.suit=suit

	def toString(self):
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
	def __init__ (self,name_):
		self.scorePile=[]
		self.hand=[]
		self.name = name_
		self.currentMove = ""

	def getMove(self,prizeCard):
		pass

	def addScoreCard(self,scoreCard):
		self.scorePile.append(scoreCard)

	def removeHandCards(self, cards):
		for card in cards:
			self.hand.remove(card)

	def pickCardForHand(self,handCard):
		self.hand.append(handCard)

	def getHandLength(self):
	    return len(self.hand)

	def toString(self):
		return 'Cards in hand: ' + [c.toString() for c in self.hand] + '\nCards in score pile: '+ [c.toString() for c in self.scorePile]

class HumanPlayer(Player):
	def getMove(self, prizeCard):
		print(self.toString())
		print('Prize card is: '+prizeCard.toString())
		response=input("What cards would you like to play?")
		cardsToPlay=[]
		for i in range(len(response)):
			char=response[i]
			if char == 'y':
				cardsToPlay.append(self.hand[i])
		return cardsToPlay

class Game:
    def __init__(self, playernames):
        self.players = []
        self.playerDict = {}
        for n in playernames:
            p = HumanPlayer(n)
            self.players.append(p)
            self.playerDict[n] = p
        self.deck = self.getDeck()
        for p in self.players:
            for i in range(3):
                p.pickCardForHand(self.deck.pop())
        self.prizeCard = self.deck.pop()
        self.previousRound = {}
        self.gameStatus = 1
        self.winner = None

    def getDeck(self):
        ranks = [r for r in range(2, 15, 1)]
        suits = ["c", "d", "h", "s"]
        deck_=[Card(rank,suit) for rank in ranks for suit in suits]
        random.shuffle(deck_)
        return deck_

    def sumCardRanks(self, cards):
	    scoreSoFar=0
	    for card in cards:
		    scoreSoFar += card.getRank()
	    return scoreSoFar

    def getDeckLength(self):
	    return len(self.deck)

    def doMove(self):
        winners = [[], 0]
        moves = {}
        for p in self.players:
            move = []
            if len([a for a in p.currentMove if a != "y" and a != "n"]) == 0:
                for i, c in enumerate(p.hand):
                    if i < len(p.currentMove) and p.currentMove[i] == "y":
                        move.append(c)
            moves[p] = move
            if self.sumCardRanks(move) > winners[1]:
                winners[1] = self.sumCardRanks(move)
                winners[0] = [p]
            elif self.sumCardRanks(move) == winners[1]:
                winners[0] = winners[0] + [p]
        for p in winners[0]:
            p.removeHandCards(moves[p])
        if len(winners[0]) == 1:
            winners[0][0].addScoreCard(self.prizeCard)
        for p in moves:
            self.previousRound[p] = moves[p]
        self.previousRound["prizeCard"] = self.prizeCard
        if len(self.deck)>len(self.players):
            for p in self.players:
                p.pickCardForHand(self.deck.pop())
        if len(self.deck) > 0:
	        self.prizeCard = self.deck.pop()
        else:
            self.gameStatus = -1
            self.winner = sorted(game.players, key = lambda x: self.sumCardRanks(x.scorePile))[-1]



playernames = []
game = Game([])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "startgame" in request.form:
            game.__init__(playernames)
            s = "Game started. \n Players: "
            for n in playernames:
                s += n + "\n"
            s += " Go to zswitten2.pythonanywhere.com/player/thenameyouchose"
            return s
        pname = request.form["playername"]
        if len(pname) > 0:
            playernames.append(pname)
    return render_template("start_page.html", playernames=playernames)

@app.route('/player/<playername>/', methods=["GET", "POST"])
def show_user_profile(playername):
    if len(game.players) == 0:
        return "Game hasn't started"
    if playername not in game.playerDict:
        return "Please enter a valid player"
    thisPlayer = game.playerDict[playername]
    if game.gameStatus == -1:
        return render_template("end_page.html", hand=thisPlayer.hand, game=game)
    if request.method == "POST":
        thisPlayer.currentMove = request.form["move"]
    allPlayersMoved = True
    for p in game.players:
        if len(p.currentMove) == 0:
            allPlayersMoved = False
    if allPlayersMoved:
        game.doMove()
        for p in game.players:
            p.currentMove = ""
    if game.gameStatus == -1:
        return render_template("end_page.html", hand=thisPlayer.hand, game=game)
    return render_template("main_page.html", hand=thisPlayer.hand, game=game, currentmove=thisPlayer.currentMove)

@app.route('/test/<testvar>/', methods=["POST", "GET"])
def testTheVar(testvar):
    if request.method == "POST":
        pass
    return render_template("test_page.html")


