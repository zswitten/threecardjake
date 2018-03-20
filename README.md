# threecardjake
Web App For Playing the Card Game 3-Card Jake

**Rules of the Game**

Three-Card Jake is a card game for a standard 52 card deck invented by my brother Jacob. Here are the rules:

1. Deal 3 cards to each player.
2. Flip over the top card of the deck
3. Each player secretly selects some cards in their hand to bid for the card.
4. The player who bid the highest adds the card to their score pile.
4a. Jack = 11, Queen = 12, King = 13, Ace = 14
4b. In the event of a tie for highest bid, neither player gets the card.
5. The player who bid the highest puts the cards in their bid in a shared discard pile.
5a. In the event of a tie for highest bid, all players who bid the highest put their bids in the discard pile.
6. Each player draws one card from the deck.
7. Repeat 1-5 until no cards are left in the deck.
8. Each player counts their score pile, using the values from 4a. The player with the highest total wins.

Example of how a game might start:
Alice and Bob begin their game.

- Alice is dealt a 7, an 8, and a Jack. (Suits omitted because they play no role in the game.) Bob is dealt a 2, a 6, and a Queen.
- The top card is flipped; it's a 10.
- Alice and Bob count to 3 and reveal their bids. Alice bids an 8 and a Jack for a total of 19. Bob bids a 6 and a Queen for 18.
- Alice has the highest bid, so she adds the 10 to her score pile and puts her 8 and Jack in the discard pile.
- Alice and Bob both draw a card, and the top card of the deck is flipped again.

ABOUT THIS REPO
`mysite/threecardjake.py` is a flask app for playing this game over the internet. Host it using a service of your choosing (I used PythonAnywhere, although my free account there expired), and go to the page and join a game. Once multiple players have joined, hit the start button and you'll be off and running.
