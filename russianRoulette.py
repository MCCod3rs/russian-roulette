#**** RUSSIAN ROULETTE ****#
import random
import time

class Player: #Class to hold player name and if they are alive or not
    def __init__(self, player_name):
        self.name = player_name
        self.eliminated = False
        self.passed = False

class RussianRoulette: #Class holding the actions of the game
    def __init__(self):
        self.players = []
        self.round = 0 #round zero, signups
        self.chamber = 6 #chamber with 6 bullets
        #self.passed = {} #only 1 pass per game

    def add_player(self, player_name):
        player = Player(player_name)
        self.players.append(player)
        print(f"{player_name} has joined the game!")

    def handle_turn(self, player):
        if player.eliminated: #Checks if player status in 'Player' class is eliminated (True or False)
            return #if player eliminated is true; the function returns; skipping them.

        print(f"\n{player.name}'s turn!")
        time.sleep(1)
        if self.chamber == 1:
            print('Only 1 bullet left...')
        else:
            print(f'Chamber is at {self.chamber}')
        action = input(f'{player.name}, is up! Do you want to Pull or Pass?').lower()

        if action == 'pull':
            self.pull_trigger(player)
        elif action == 'pass':
            self.pass_turn(player)
        else:
            print("Invalid action. Please choose Pull or Pass")
            self.handle_turn(player)

    def pull_trigger(self, player):
        if self.chamber <= 1: #If only 1 chamber left; auto-eliminated
            time.sleep(1)
            print(f"BANG! {player.name} was shot. RIP!")
            player.eliminated = True #player status set to eliminated
            if self.remaining_players() == 1:
                return
        else:
            print(f"{player.name} pulls the trigger!")
            time.sleep(1)
            roll = random.randint(1, 6)
            if roll == 1:
                print(f"BANG! {player.name} was shot. RIP!")
                time.sleep(1)
                player.eliminated = True
                if self.remaining_players() == 1:
                    return
                else:
                    print(f'Chamber has reset!')
                    self.chamber = 6
            else:
                print(f"{player.name} lives! They are safe for now.")
                self.chamber -= 1  # Reduce the chamber count

    def pass_turn(self, player):
        if not player.passed:
            player.passed = True
            print(f"{player.name} passes!")
        else:
            print(f"{player.name}, you've already used your pass!")
            time.sleep(1)
            print(f'{player.name} is forced to pull!')
            self.pull_trigger(player)

    def remaining_players(self):
        remaining_players = [player for player in self.players if not player.eliminated]
        return len(remaining_players)

    def next_round(self):
        # Check if only one player is left
        remaining_players = [player for player in self.players if not player.eliminated]
        #creates list 'remaining_players' by checking if players ".eliminated" is "False"
        if self.remaining_players() == 1:
            print(f"\n{remaining_players[0].name} is the lone survivor! GG")
            return
        # Reset the round and chamber for the next round
        #self.chamber = 6
        time.sleep(1)  # Short pause before the next round begins

    def start_game(self):
        print("Good Luck!")
        time.sleep(1)
        while self.remaining_players() > 1:
            self.round += 1
            print(f"\n--- Round {self.round} ---")
            for player in self.players:
                if not player.eliminated:#If player not eliminated, take turn
                    self.handle_turn(player)
                if self.remaining_players() == 1:
                    break
            # End the round
            self.next_round()

        if self.remaining_players() == 1:
            print(f'{self.remaining_players()} is the lone survivor! GG')

#TODO: Showcase PL and if pass is used up or not at the start of each new round.
#TODO: add and define 'Steal' function

if __name__ == "__main__":
    print('Welcome to Russian Roulette! Hope you\'re feeling lucky...')
    time.sleep(.5)
    game = RussianRoulette()

    num_players = int(input("How many players do you want to add? "))
    for player_number in range(num_players):
        player_name = input("Enter player name: ")
        game.add_player(player_name)
    time.sleep(1.5)
    game.start_game()

