import random

#card info
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#classes

#card
#suit/rank/value
class Card():
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"

#deck
class Deck():
    def __init__(self):
        self.main_deck = []
        
        for suit in suits:
            for rank in ranks:
                temp_card = Card(suit, rank, values[rank])
                self.main_deck.append(temp_card)
        
    def __str__(self):
        return f"Deck is {len(self.main_deck)} cards long"
    
    def shuffle(self):
        random.shuffle(self.main_deck)
    
    def deal_one(self):
        return self.main_deck.pop()

#hand
#the dealer and player will each have a hand
class Hand():
    def __init__(self):
        self.curr_cards = []
        self.curr_sum = 0
        self.num_aces = 0
        
    def __str__(self):
        return f"Current Sum: {self.curr_sum}"
    
    def add_card(self, new_card):
        self.curr_sum = self.curr_sum + new_card.value
        self.curr_cards.append(new_card)
        if new_card.rank == "Ace":
            self.num_aces += 1
        
    def return_sum(self):
        return self.curr_sum
    
    def ace_lower(self):
        if self.num_aces > 0:
            self.curr_sum -= 10
            self.num_aces -= 1

#bank
class Bank():
    def __init__(self, balance=250):
        self.balance = balance
    
    def __str__(self):
        return f"Bank Balance: ${self.balance}"
    
    def add_win(self, amount):
        self.balance += amount
    
    def remove_bet(self, amount):
        self.balance -= amount

#functions

def bet_menu(balance):
    
    while True:
        try:
            bet_val = int(input("Input the amount you would like to bet: "))
            
        except:
            print("\tNot a valid number, try again\n")
            continue

        else:
            if bet_val > balance:
                print("\tAmount is greater than current bank balance of ${}, try again\n".format(balance))
                continue
            elif bet_val == 0:
                print("\tCannot bet zero amount, try again\n")
                continue
            elif bet_val < 0:
                print("\tCannot bet negative amount, try again\n")
                continue
            else:
                print("\tValid bet")
                return bet_val

def choice_menu(deck, hand):
    
    while True:
        choice = input("\nWould you like to hit or stand? Input (h)it or (s)tand: ")
        
        if choice.lower() == 'h':
            hit(deck, hand)
            print_cards("player", player_hand)
            return True
        
        elif choice.lower() == 's':
            return False
        
        else:
            print("\tInvalid choice, try again\n")
            continue

        break

def print_cards(identity, hand):
    
    if identity == "player":
        print("\nPlayer Cards:")
        
    else:
        print("\nDealer Cards:")
        
    for num in range(len(hand.curr_cards)):
        print(hand.curr_cards[num])
        
def hit(deck, hand):
    hand.add_card(deck.deal_one())

def end_menu():
    
    while True:
        choice = input("Would you like to play again? (y)es or (n)o: ")
        
        if choice.lower() == 'y':
            return True
        
        elif choice.lower() == 'n':
            return False
        
        else:
            print("\tInvalid option, try again\n")
            continue

#game logic
if __name__ == "__main__":
    #random.seed(99) #99 has natural with two aces

    game_loop = True
    player_bank = Bank() #default is $250, can add feature if desired

    #Output Welcome message
    print("Welcome to Blackjack")

    #game loop, exits when player quits or out of money
    while game_loop:
        
        #define all paramters
        play_deck = Deck()
        play_deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        
        #set loop variables
        choice_loop = True
        dealer_loop = True
        natural = False
        play_win = False
        push = False
        
        print("\n")
        print(player_bank)
        
        #menu for bets
        curr_bet = bet_menu(player_bank.balance)
        player_bank.remove_bet(curr_bet)
        
        #print both cards for the player
        print("\nPlayer Cards:")
        
        #deal two cards to each player
        for num in range(2):
            play_temp = play_deck.deal_one()
            player_hand.add_card(play_temp)
            print(play_temp)
        
        #print only one of dealer cards, deal_temp holds facedown card
        print("\nDealer Card:")
        deal_temp = play_deck.deal_one()
        dealer_hand.add_card(deal_temp)
        print(deal_temp)
        deal_temp = play_deck.deal_one()
        
        #natural hand
        if player_hand.return_sum() == 21:
                choice_loop = False
                dealer_loop = False
                natural = True
                play_win = True
                print("\nPlayer has natural")
                
                #check if dealer has natural
                dealer_hand.add_card(deal_temp)
                print_cards("dealer", dealer_hand)
                if dealer_hand.curr_sum == 21:
                    play_win = False
                    push = True
        
        #player then chooses to hit or stay
        while choice_loop:
            
            #blackjack
            if player_hand.return_sum() == 21:
                choice_loop = False
                play_win = True
                print("Player got blackjack")
            
            #player over 21
            elif player_hand.return_sum() > 21:
                #adjust for aces
                player_hand.ace_lower()
                
                #player busts
                if player_hand.return_sum() > 21:
                    dealer_loop = False
                    choice_loop = False
                    print("\nPlayer went bust")
                
            #choice
            else:
                choice_loop = choice_menu(play_deck, player_hand)
        
        #add and print dealer's cards
        if dealer_loop:
            dealer_hand.add_card(deal_temp)
            print_cards("dealer", dealer_hand)
        
        #once player is done, dealer loop
        #hits until 17 or more
        #first ace is 11
        #if ace would make sum 17 or more, but less than 21, must make 11
        while dealer_loop:
            
            if dealer_hand.curr_sum == 21:
                dealer_loop = False
                print("Dealer got blackjack")
                
                #dealer and player got blackjack, push
                if play_win == True:
                    push = True
            
            #check if over
            elif dealer_hand.curr_sum > 21:
                #adjust for aces
                dealer_hand.ace_lower()
                
                #dealer busts
                if dealer_hand.return_sum() > 21:
                    dealer_loop = False
                    play_win = True
                    print("\nDealer went bust")
            
            #if dealer has higher sum than player
            elif dealer_hand.curr_sum > player_hand.curr_sum:
                dealer_loop = False
                print("\nDealer has higher sum, dealer wins")
            
            #dealer stand if sum is over 17
            elif dealer_hand.return_sum() >= 17:
                if dealer_hand.curr_sum == player_hand.curr_sum:
                    push = True
                    dealer_loop = False
                    print("Dealer stands with same sum as player")
                
                else:
                    play_win = True
                    dealer_loop = False
                    print("Dealer stands with sum less than player")
            
            #dealer hits
            else:
                print("\nDealer hits")
                hit(play_deck, dealer_hand)
                print_cards("dealer", dealer_hand)
        
        #conditional statements for all possible combinations
        #push, natural, win, lose
        if push:
            player_bank.add_win(curr_bet)
            print("\nGame is a tie, bets are pushed\n")
        
        elif natural:
            winnings = int(1.5 * curr_bet) #truncates decimals
            player_bank.add_win(winnings)
            print(f"\nPlayer wins with natural\nWinnings are ${winnings}\n")
        
        elif play_win:
            winnings = 2 * curr_bet
            player_bank.add_win(winnings)
            print(f"\nPlayer wins\nWinnings are ${winnings}\n")
        
        else:
            player_bank.remove_bet(curr_bet)
            print(f"\nDealer wins\nPlayer lost ${curr_bet}\n")
        
        print(player_bank)
        
        if player_bank.balance > 0:
            game_loop = end_menu()
        else:
            game_loop = False
        
        #if game_loop:
        #clear_output()

    print(f"\nThanks for playing\nFinal Score: ${player_bank.balance}")

