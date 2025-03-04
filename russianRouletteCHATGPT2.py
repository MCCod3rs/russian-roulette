import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.eliminated = False

class RussianRoulette:
    def __init__(self):
        self.players = {}  # Dictionary to store Player objects by their ID
        self.round = 0
        self.chamber = 6
        self.passed = {}

    def to_id(self, name):
        return name.lower().replace(" ", "")

    def add_player(self, player_name):
        """Add a player to the game."""
        player = Player(player_name)
        self.players[self.to_id(player_name)] = player
        print(f"{player_name} has joined the game!")

    def start_game(self):
        """Start the game, prompting players to take turns."""
        print("Starting the Russian Roulette game!")
        while len(self.players) > 1:
            self.round += 1
            print(f"\n--- Round {self.round} ---")
            for player_id, player in self.players.items():
                if not player.eliminated:
                    self.handle_turn(player)

            # End the round
            self.next_round()

    def handle_turn(self, player):
        """Handle each player's turn."""
        if player.eliminated:
            return

        print(f"\n{player.name}'s turn.")
        action = input(f"{player.name}, it's your turn! Do you want to 'pull', 'pass', or 'quit'? ").lower()

        if action == 'pull':
            self.pull_trigger(player)
        elif action == 'pass':
            self.pass_turn(player)
        elif action == 'quit':
            player.eliminated = True
            print(f"{player.name} has quit the game.")
        else:
            print("Invalid action. Please choose 'pull', 'pass', or 'quit'.")

    def pull_trigger(self, player):
        """Handle pulling the trigger."""
        if self.chamber == 1:
            print(f"**BOOOM!** {player.name} was shot. RIP!")
            player.eliminated = True
        else:
            print(f"{player.name} pulls the trigger!")
            roll = random.randint(1, self.chamber)
            if roll == 1:
                print(f"**BOOM!** {player.name} was shot. RIP!")
                player.eliminated = True
            else:
                print(f"{player.name} lives! They are safe for now.")
                self.chamber -= 1  # Reduce the chamber count

    def pass_turn(self, player):
        """Handle passing the turn."""
        if player.name not in self.passed:
            self.passed[player.name] = True
            print(f"{player.name} has chosen to pass and is safe for this round.")
        else:
            print(f"{player.name}, you already passed in this round!")

    def next_round(self):
        """Handle moving to the next round."""
        # Check if only one player is left
        remaining_players = [player for player in self.players.values() if not player.eliminated]
        if len(remaining_players) == 1:
            print(f"\n{remaining_players[0].name} is the winner! GG!")
            return

        # Reset the round and chamber for the next round
        self.chamber = 6
        self.passed.clear()
        time.sleep(2)  # Short pause before the next round begins

    def list_players(self):
        """List all players currently in the game."""
        print("\nCurrent Players:")
        for player in self.players.values():
            status = "Eliminated" if player.eliminated else "In Game"
            print(f"{player.name}: {status}")

# Main function to simulate the game
if __name__ == "__main__":
    game = RussianRoulette()

    # Add players dynamically
    num_players = int(input("How many players do you want to add? "))
    for _ in range(num_players):
        player_name = input("Enter player name: ")
        game.add_player(player_name)

    # Start the game
    game.start_game()