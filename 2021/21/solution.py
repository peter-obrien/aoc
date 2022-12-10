from functools import lru_cache
import sys
import time
import re
from itertools import product

class DeterministicDice():

    def __init__(self, sides: int) -> None:
        self.sides: int = sides
        self.roll_count: int = 0
        self.current_position: int = sides

    def roll(self):
        self.roll_count += 1
        self.current_position = (self.current_position % self.sides) + 1
        return self.current_position

class Game:

    def __init__(self, starting_positions: dict, winning_score: int) -> None:
        self.winning_score = winning_score
        self.board_size = 10
        self.scores = dict()
        self.positions = starting_positions
        self.num_players = len(starting_positions)
        for p in starting_positions:
            self.scores[p] = 0
        self.current_player = min(starting_positions.keys())

    def take_turn(self, die: DeterministicDice):
        roll_total: int = die.roll() + die.roll() + die.roll()
        self.positions[self.current_player] += roll_total
        self.positions[self.current_player] = 10 if self.positions[self.current_player] % 10 == 0 else self.positions[self.current_player] % 10
        self.scores[self.current_player] += self.positions[self.current_player]
        self.current_player = (self.current_player % self.num_players) + 1

    def game_complete(self):
        return max(self.scores.values()) > self.winning_score

class DiracGame:
    def __init__(self, starting_positions: dict) -> None:
        self.DIRAC_POSSIBILITIES = set((roll1, roll2, roll3) for roll1, roll2, roll3 in product(range(1,4), repeat=3))
        self.winning_score = 21
        self.starting_positions = starting_positions

    def move(self, player_state: tuple, combined_roll: tuple):
        position = player_state[0] + sum(combined_roll)
        position = 10 if position % 10 == 0 else position % 10
        return (position, player_state[1] + position)

    def play_game(self):
        results = self.take_turn(1, (self.starting_positions[1], 0), (self.starting_positions[2],0))
        return max(results)

    # Memoize the results so that revisited recursive calls are short circuited to the previously cached result
    @lru_cache(maxsize=None)
    def take_turn(self, active_player: int, p1_state: tuple, p2_state: tuple):
        if p1_state[1] >= self.winning_score:
            return (1,0)
        elif p2_state[1] >= self.winning_score:
            return (0,1)
        else:
            result = (0,0)
            for roll_permutation in self.DIRAC_POSSIBILITIES:
                if active_player == 1:
                    temp_result = self.take_turn(2, self.move(p1_state, roll_permutation), p2_state)
                else:
                    temp_result = self.take_turn(1, p1_state, self.move(p2_state, roll_permutation))
                result = (result[0] + temp_result[0], result[1] + temp_result[1])
            return result

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    # Players are 1 & 2, not 0 & 1
    players = dict()

    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            inputs = re.findall(r'(\d+)', line)
            players[int(inputs[0])] = int(inputs[1])

    D = DeterministicDice(100)
    G = Game(players.copy(), 1000)

    while not G.game_complete():
        G.take_turn(D)

    result = D.roll_count * min(G.scores.values())
    print(f"Part 1: {result} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    result = DiracGame(players).play_game()
    print(f"Part 2: {result} (took {(time.time() - start_time)}s)")