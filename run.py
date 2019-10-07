import pydealer
import math
import getpass
import sys
import time
import os


class Player:

    def __init__(self, id):
        self.id = id
        self.current_hand = None
        self.books = 0
        self.password = ""


def wait(prompt, seconds):
    for i in range(seconds):
        print(prompt + str(seconds - i))
        time.sleep(1)
        sys.stdout.write("\033[F")


def clear():
    os.system('cls')  # For Windows
    os.system('clear')  # For Linux/OS X


num_players = None

print("Welcome to Goldfish!!\n\n")
while type(num_players) is not int:
    num_players = input("How many players are there? You can play with a maximum of five people\n")
    try:
        try_num_players = int(num_players)
        test_min_2 = math.sqrt(try_num_players - 2)
        test_max_5 = math.sqrt(5 - try_num_players)
        num_players = try_num_players
    except:
        print("Please enter a valid positive integer greater than one and less than five!")

players = [Player(x + 1) for x in range(num_players)]

current_deck = pydealer.Deck()

start_cards = None
if num_players in [2, 3]:
    start_cards = 7
else:
    start_cards = 5

for p in players:
    p.current_hand = current_deck.deal(start_cards)
    p.password = getpass.getpass("Player {}! Enter a password (Keep blank for no password):".format(p.id))

wait("Please hand to Player 1. Starting in ", 5)
clear()

log_actions = []
current_player = 0
while current_deck.size > 0:
    tried_pwd = getpass.getpass("Player {}! Please Enter your Password:".format(p.id))
    while tried_pwd != players[current_player].password:
        print("Incorrect password!'")
        tried_pwd = getpass.getpass("Player {}! Please Enter your Password:".format(p.id))

    print(
        "Welcome! To see your current cards, type 'cards'. To request a type of card from someone, type 'fish' - you can only fish for ranks that you own yourself!\n")
    command = None
    while (command != "fish"):
        command = input()
        if (command == 'cards'):
            print(p.current_hand)
            card_counts = {}
            for c in p.current_hand:
                if c.value in card_counts.keys():
                    card_counts[c.value] += 1
                else:
                    card_counts[c.value] = 1
            for c in card_counts.keys():
                print("You have {} cards of type {}".format(card_counts[c], c))
            wait("This will disappear in ", 8)
            clear()
        elif (command == 'fish'):
            player = None
            while type(player) is not int:
                player = input("Which player do you want to ask? Player ")
                try:
                    try_player = int(player)
                    test_min_1 = math.sqrt(try_player - 1)
                    test_max_count = math.sqrt(len(players) - try_player)
                    player = try_player
                except:
                    print("Please enter a valid player!")

            print(
                "Choose what card type you are asking for. For example, if you are asking for a King, choose one of your King cards.")
            for i, c in enumerate(players[current_player].current_hand):
                print("{}: {}".format(i, c))
            card_asked = input()
            while type(card_asked) is not int:
                try:
                    try_card = int(card_asked)
                    test_min_0 = math.sqrt(try_card)
                    test_max_count = math.sqrt(len(players[current_player].current_hand) - try_card-1)
                    card_asked = try_card
                except:
                    print("Please enter an actual card number based on your current hand!")
                    card_asked = input()
            card = players[current_player].current_hand[card_asked]

            stolen_cards = []
            for c in players[player - 1].current_hand:
                if c.value == card.value:
                    stolen_cards.append(c)
            for c in stolen_cards:
                players[player - 1].current_hand.remove(c)

            if len(stolen_cards) == 0:
                print(
                    "Unfortunately, this player did not have this card on them! You have 'Go-Fished'. Please hand it to the next player, Player {}.".format(
                        current_player + 1 % len(players)))
                wait("Transfer to the next player will happen in: ", 5)
                clear()
                current_player = (current_player+1)%len(players)
                continue

            log_actions.append(
                "Past Action: Player {} stole {} cards from Player {} of type {}".format(current_player + 1, player,
                                                                                         card.value))
            print("You have stolen {} cards! Good job.".format(len(stolen_cards)))
            card_counts = {}
            for c in p.current_hand:
                if c.value in card_counts.keys():
                    card_counts[c.value] += 1
                else:
                    card_counts[c.value] = 1
            card_types = []
            books = 0
            for c in card_counts.keys():
                if card_counts[c] >= 4:
                    print("You have a book of type {}! We have taken it from your hand.".format(c))
                    log_actions.append("Past Action: Player {} created a book of type {}".format(current_player + 1, c))
                    books += 1
                    card_types.append(c)
                    card_counts[c] = 0
            new_hand = players[current_player].current_hand
            for c in players[current_player].current_hand:
                if c.value in card_types and card_counts[c.value] > 0:
                    new_hand.remove(c)
                    card_counts[c.value] -= 1
            players[current_player].current_hand = new_hand
            players[current_player].books += books

            print(
                "Your turn has ended! Please hand it to the next player, Player {}.".format(
                    current_player + 1 % len(players)))
            wait("Transfer to the next player will happen in: ", 5)
            clear()
            current_player = (current_player + 1) % len(players)
            continue
        else:
            print("That is not a valid command!")

