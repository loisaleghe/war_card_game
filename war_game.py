from random import shuffle
import numpy as np


# Two useful variables for creating Cards.
SUITE = 'H D S C'.split() # this returns ["H", "D", "S", "C"]
# H - Hearts D - Diamonds S- Spades C-Clubs
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

class Deck():
    """
    This is the Deck Class. This object will create a deck of cards to initiate
    play. You can then use this Deck list of cards to split in half and give to
    the players. It will use SUITE and RANKS to create the deck. It should also
    have a method for splitting/cutting the deck in half and Shuffling the deck.

    There are 4 suites: Hearts, Diamonds, Spades and Clubs. Each suit contains 13
    cards: 10 numbered cards (A-10) and 3 face cards (Jack, Queen and King)
    """

    def __init__(self):
        # loop through suite and ranks and append to game deck
        print("CREATE DECK")
        self.card_deck = [(s,r) for s in SUITE for r in RANKS]

        # the above code is the same as this below
        # self.card_deck = []
        # for r in RANKS:
        #     for s in SUITE:
        #         self.card_deck.append((s,r))

    def shuffle_deck(self):
        # shuffle deck
        return shuffle(self.card_deck)

    def split_deck(self):
        # split in half
        # this will return a tuple of the split cards, we already kbow there are
        # 52 cards in a deck and half of that is 26
        return (self.card_deck[:26], self.card_deck[26:])


class Hand:
    '''
    This is the Hand class. Each player has a Hand, and can add or remove
    cards from that hand. There should be an add and remove card method here.
    '''

    # initialize the hand of the game which will take the cards for the hand
    def __init__(self, cards):
        self.cards = cards

    # special string method to know how many cards the player has in their hand
    def __str__(self):
        return str(len(self.cards))

    # so this is the middle where both cards from the two players are added
    def add_card(self, added_cards):
        self.cards.extend(added_cards)

    # when a player plays, this returns the removed card
    def remove_card(self):
        return self.cards.pop()


class Player:
    """
    This is the Player class, which takes in a name and an instance of a Hand
    class object. The Player can then play cards and check if they still have cards.
    """

    # here we are initializing the name of the player which we will be taking
    # and their hand as well that they will be playing with
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play_cards(self):
        drawn_cards = self.hand.remove_card()
        return drawn_cards

    # in case there is war
    def war_cards(self):
        # we are making this an if else statement because if the user only has
        # like 2 cards left, we would have an out of range error
        war_cards = []
        if len(self.hand.cards) < 3:
            return self.hand.cards
        else:
            for x in range(3):
                war_cards.append(self.hand.remove_card())
            return war_cards

    # to store cards won
    def store_wins(self, cards):
        wins = []
        wins.extend(cards)
        return wins

    # this will return a boolean
    def still_has_cards(self):
        return len(self.hand.cards) != 0


######################
#### GAME PLAY #######
######################
print("Welcome to War, let's begin...")

# Use the 3 classes along with some logic to play a game of war!
# create deck, shuffle and assign hand
d = Deck()
d.shuffle_deck()
hand1, hand2 = d.split_deck()
# remember hand is a tuple that takes in suite and rank
comp_hand = Hand(hand1)
human_hand = Hand(hand2)

# create players
comp_player = Player("Computer", comp_hand)
human_name = input("What is your name? ")
human_player = Player(human_name, human_hand)
# human_wins and comp_wins is where we store who has the most cards to award winner
human_wins = []
comp_wins = []

# start game that runs until one player doesn't have cards anymore
total_game_rounds = 0 # to know how many rounds the game took
war_count = 0 # to know how many times war has happened
while comp_player.still_has_cards() and human_player.still_has_cards():
    total_game_rounds += 1
    c_card = comp_player.play_cards()
    print("Computer plays: ")
    print(c_card)
    h_card = human_player.play_cards()
    print("{} plays: ".format(human_name))
    print(h_card)
    table_cards = [] # where we add each played cards

    # add played cards to table
    table_cards.append(c_card)
    table_cards.append(h_card)

    # let's check for war
    # checking at index 1 because the card returns but suites and ranks (s,r) &
    # ranks is index 1 rather than 0
    if c_card[1] == h_card[1]:
        print("WAR!!!")
        """
        When we have war, you put "3" cards facing down then play again
        """
        war_count += 1

        # remove 3 cards each from players
        # key that we use extend here rather than append, so it doesn't add all
        # as a single element but separate

        table_cards.extend(comp_player.war_cards())
        print("Computer adds three cards facing down")
        table_cards.extend(human_player.war_cards())
        print("{} adds three cards facing down".format(human_name))

        # play again
        c_card = comp_player.play_cards()
        print("Computer plays again")
        print(c_card)
        h_card = human_player.play_cards()
        print("{} plays again".format(human_name))
        print(h_card)

        # Add to table_cards
        table_cards.append(c_card)
        table_cards.append(h_card)
        print("All the cards that have been put down due to war!")
        print(table_cards)

        # convenently enough, the ranks have been arranged in ascending order,
        # so we can check the index to know which is higher
        if RANKS.index(c_card[1]) < RANKS.index(h_card[1]):
            human_player.store_wins(table_cards)
            human_wins.extend(human_player.store_wins(table_cards))
            print("{} wins this war!".format(human_name))

        else:
            comp_player.store_wins(table_cards)
            comp_wins.extend(comp_player.store_wins(table_cards))
            print("Computer wins this war!")

    else:
        if RANKS.index(c_card[1]) < RANKS.index(h_card[1]):
            human_player.store_wins(table_cards)
            human_wins.extend(human_player.store_wins(table_cards))
            print("{} wins this round!".format(human_name))


        else:
            comp_player.store_wins(table_cards)
            comp_wins.extend(comp_player.store_wins(table_cards))
            print("Computer wins this round!")

print("GAME OVER, THE WAR HAS ENDED")
print("Total War Count: " + str(war_count))
print("Total Game Rounds: " + str(total_game_rounds))
if (len(comp_wins) > len(human_wins)):
    print("THE WINNER OF THE WAR IS THE COMPUTER")
    print("Proof below:")
    print(len(comp_wins))
    print(comp_wins)
    print(len(human_wins))
    print(human_wins)
if (len(human_wins) > len(comp_wins)):
    print("THE WINNER OF THE WAR IS {}".format(human_name.upper()))
    print("Proof below:")
    print(len(human_wins))
    print(human_wins)
    print(len(comp_wins))
    print(comp_wins)
