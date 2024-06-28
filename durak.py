# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import string, math, random
from collections.abc import Sequence

class Card:
    RANKS = (6, 7, 8, 9, 10, 11, 12, 13, 14)

    SUITS = ('S', 'D', 'H', 'C')
             #('♠', '♦', '♥', '♣')
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

    def __repr__(self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
             rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)



class Deck:
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card(rank, suit)
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def deal(self):
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)


class Durak:
    def __init__(self, deck=Deck, players=int, phands=list, kozer=str):
        self.deck = deck
        self.deck.shuffle()
        self.phands = []
        for i in range(players):
            hand = []
            for i in range(6):
                hand.append(deck.deal())
            self.phands.append(hand)



    def beat(self, card = Card, p = int, kozer=Card):
        oppcard = cardselect(self, p)

        if card.suit == oppcard.suit and card.rank < oppcard.rank:
            print(str(oppcard) + " beats " + str(card))
        if (oppcard.suit == kozer.suit):
            print(str(oppcard) + " beats " + str(card))
        else:
            if card.suit != oppcard.suit:
                print("Error. Wrong suit. Pick another card to beat " + card +".")
                newcard = cardselect(self, p)
                self.beat(card, p, kozer)
            if card.rank >= oppcard.rank:
                print("Error. Rank too low. Pick another card to beat " + card +".")
                newcard = cardselect(self, p)
                self.beat(card, p, kozer)
        return oppcard

    def printall(self):
      for i in range(len(self.phands)):
          counter = self.phands[i]
          print(*counter, sep = ",")

    def printhand(self, player = int):
        print(*self.phands[player], sep = ",")

    def pickup(self, p = int):
        while len(self.phands[p]) < 6 and self.deck != 0:
            self.phands[p].append(self.deck.deal())


def RankError():
    print("Error. Card must match rank of cards on the table. Select another card or pass")

def cardselect(durak=Durak, p=int):
    pl = str((int(p) + 1))
    print("Player " + pl + ", select a card to play.")

    strcard = input(str(durak.printhand(p)) + "\n Your Card: ")

    suit = strcard[1]
    if strcard[0] == "A":
        rank = 14
    elif strcard[0] == "K":
        rank = 13
    elif strcard[0] == "Q":
        rank = 12
    elif strcard[0] == "J":
        rank = 11
    elif len(strcard) == 3:
        rank = 10
        suit = strcard[2]
    else:
        rank = strcard[0]


    for i in range(len(durak.phands[p])):
        if int(durak.phands[p][i].rank) == int(rank) and str(durak.phands[p][i].suit) == suit:
            print("Player " + pl + " plays " + strcard)
            return durak.phands[p][i]

    print("Error. Choose a card from your deck.")
    cardselect(durak, p)

def beatorpick(durak, a=int, b=int, kozer = Card, card1 =Card):
    print("Player "+ str(b+1) + ", you must beat: " + str(card1) + ". The kozer suit is " + kozer.suit + ". Your hand is: ")
    durak.printhand(b)
    i = input("Beat (B) or pick up (P)?: ")
    if i == "B":
        bc = beata(a, b, durak, kozer, card1)
        return bc
    if i == "P":
        durak.phands[b].append(card1)
        durak.phands[a].remove(card1)
        durak.phands[a].append(durak.deck.deal())
        return None

def beata(player1=int, player2=int, durak=Durak, kozer=Card, card1=Card):
    oppcard = durak.beat(card1, player2, kozer)
    durak.phands[player1].remove(card1)
    durak.phands[player2].remove(oppcard)

    print("Player " + str(player1 + 1) + ", play another card? Your remaining hand is: ")
    durak.printhand(player1)
    p1input = input("Select Y/N: ")

    #note make a list of ranks
    cardranks = []
    cardranks.append(card1.rank)
    cardranks.append(oppcard.rank)

    cards2remove1 = []
    cards2remove2 = []
    if p1input == "N":
        returnlist = [oppcard, cardranks]
        return returnlist
    while p1input == "Y":
        p1card = cardselect(durak, player1)
        if p1card.rank not in cardranks:
            raise Exception("Error. Rank must match.")
        p2card = beatorpick(durak, player1, player2, kozer, p1card)
        cards2remove1.append(p1card)
        cards2remove2.append(p2card[0])

        cardranks.append(p2card[1])

    for i in cards2remove1:
        durak.phands[player1].remove(i)
    for j in cards2remove2:
        durak.phands[player2].remove(j)



def play_round(durak=Durak, kozer=Card, players=list, a=int, b=int):
    card1 = cardselect(durak, players[a])
    cardranks = beatorpick(durak, a, b, kozer, card1)[1]
    cards2removeb = []
    cards2removec = []
    cards2removed = []
    if len(players) > 2:
        if b == 1:
            c=2
            d=3
        if b == 2:
            c=3
            d=0
        if b == 3:
            c=0
            d=1

        if len(players) >= 3:
            print( "Player 3 hand: ")
            durak.printhand(2)
            ask = input("Player 3. Do you have cards to play? Y/N: ")
            while ask == "Y":
                p3card = cardselect(durak, c)
                if p3card.rank not in cardranks:
                    raise Exception("Error. Rank must match.")
                p2card = beatorpick(durak, c, a, kozer, p3card)[0]
                cards2removeb.append(p2card)
                cards2removec.append(p3card)
        if len(players) == 4:
            cards2removed = []
            print( "Player 4 hand: ")
            durak.printhand(3)
            ask = input("Player 4. Do you have cards to play? Y/N: ")
            while ask == "Y":
                p3card = cardselect(durak, d)
                if p3card.rank not in cardranks:
                    raise Exception("Error. Rank must match.")
                p1card = beatorpick(durak, d, a, kozer, p3card)[0]
                cards2removeb.append(p3card)
                cards2removed.append(p1card)
    for i in cards2removeb:
        durak.phands[b].remove(i)
    for j in cards2removec:
        durak.phands[c].remove(j)
    for k in cards2removed:
        durak.phands[d].remove(k)



    durak.pickup(b)
    durak.pickup(c)
    durak.pickup(d)


def play():
    players = int(input("Enter how many players will be playing. 2-4 allowed: "))
    deck = Deck()
    durak = Durak(deck, players)
    kozer = durak.deck.deal()
    print("The kozer is " + str(kozer))
    #player 1 = 0, p2 = 1, p3 =2, p4 = 3
    playerslist = []
    for i in range(int(players)):
        playerslist.append(i)

    while len(deck) != 0 :
        play_round(durak, kozer, playerslist, 0, 1)
        durak.printall()

        play_round(durak, kozer, playerslist, 1, 2)
        durak.printall()

        play_round(durak, kozer, playerslist, 2, 3)
        durak.printall()

        play_round(durak, kozer, playerslist, 3, 0)
        durak.printall()


    durak.printall()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    play()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
