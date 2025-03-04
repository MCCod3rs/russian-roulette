import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.eliminated = False

class RussianRoulette:
    def __init__(self):
        self.name = "Russian Roulette"
        self.id = self.to_id(self.name)
        self.description = '__"Pass like a puss or Pull like a pro."__ Game rules: https://sites.google.com/view/survivor-ps/themes/russian_roulette'
        self.chamber = 6
        self.players = {}
        self.passed = {}
        self.stole = {}
        self.moved = {}
        self.finals = False
        self.round = 0
        self.turner = 0
        self.cur_player = None
        self.oplayer = None

    def to_id(self, name):
        return name.lower().replace(" ", "_")

    def add_player(self, player_name):
        player = Player(player_name)
        self.players[self.to_id(player_name)] = player

    def start_game(self):
        print(f"**Signups are now closed.** The gun is loaded with a chamber of six, good luck! **Commands:** pull, pass, steal")
        self.next_pick()

    def next_pick(self):
        remaining_players = [player for player in self.players.values() if not player.eliminated]
        if len(remaining_players) == 2:
            if self.finals:
                self.handle_pick(self.cur_player.name)
            else:
                self.finals = True
                self.chamber = 6
                print("**The chamber has been reset.**")
                self.pick_players_for_finalists()
                return
        if self.round == 0:
            self.round += 1
            print(f"**Round {self.round}!**")

        if len(remaining_players) == 1:
            self.handle_pick(remaining_players[0].name)
            return

        if self.turner == 3 or self.round == 1:
            print("Players (" + str(len(remaining_players)) + "): " + ", ".join([p.name for p in remaining_players]))
            self.turner = 0

        self.turner += 1
        self.cur_player = remaining_players[0]
        print(f"{self.cur_player.name}, you're up! Chamber: {self.chamber}")
        self.handle_turn()

    def pick_players_for_finalists(self):
        finalists = random.sample(list(self.players.values()), 2)
        print(f"**{finalists[0].name} and {finalists[1].name} advance to the finals!** Steals can no longer be used.")
        self.passed[finalists[0].name] = True
        self.passed[finalists[1].name] = True
        self.chamber = 6

    def handle_turn(self):
        if self.chamber > 1:
            action = input(f"**{self.cur_player.name}**, choose 'pull', 'pass' or 'steal': ").strip().lower()
            if action == 'pull':
                self.pull()
            elif action == 'pass':
                self.pass()
            elif action == 'steal':
                self.steal()
            else:
                print("Invalid action. You are forced to pass.")
                self.pass()

    def pull(self):
        if self.chamber == 1:
            print("BOOOM! " + self.cur_player.name + " was shot. RIP!")
            self.cur_player.eliminated = True
            self.next_pick()
        else:
            print(f"**{self.cur_player.name} pulls the trigger!**")
            roll = random.randint(1, self.chamber)
            if roll == 1:
                print(f"**BOOM!** {self.cur_player.name} was shot. RIP!")
                self.cur_player.eliminated = True
            else:
                print(f"**{self.cur_player.name} lives!**")
                self.chamber -= 1
            self.next_pick()

    def pass(self):
        print(f"**{self.cur_player.name} has chosen to pass and is safe until the next round!**")
        self.passed[self.cur_player.name] = True
        self.moved[self.cur_player.name] = True
        self.next_pick()

    def steal(self):
        target_name = input(f"{self.cur_player.name}, who would you like to steal from? ").strip()
        target = self.players.get(self.to_id(target_name))
        if not target or target.eliminated or self.passed.get(target_name):
            print("Invalid target or target cannot be stolen from.")
            self.next_pick()
            return

        self.oplayer = target
        print(f"**{self.cur_player.name} attempts to steal from {self.oplayer.name}!**")
        roll1 = random.randint(1, 100)
        roll2 = random.randint(1, 100)

        if roll1 > roll2:
            print(f"{self.cur_player.name} wins the steal! {self.oplayer.name} is eliminated.")
            self.oplayer.eliminated = True
        else:
            print(f"{self.cur_player.name} fails to steal from {self.oplayer.name}. RIP!")
            self.cur_player.eliminated = True
        self.next_pick()

    def end_game(self):
        print("The game is over.")

# Example usage:
game = RussianRoulette()

# Add players (in real scenario, it would come from user input)
game.add_player("Alice")
game.add_player("Bob")
game.add_player("Charlie")

# Start the game
game.start_game()