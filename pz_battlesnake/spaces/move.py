from typing import List
from gym.spaces.space import Space
import random


class Move(Space[str]):
    """
    This class represents the move action in BattleSnake, which is documented under response property of the /move endpoint. Refer to the battlesnake docs: https://docs.battlesnake.com/references/api#post-move

    There's 4 possible moves:
        - "up"
        - "down"
        - "left"
        - "right"
    """

    

    def __init__(self):
        self.moves: List[str] = self.possible_moves
        super().__init__()

    def sample(self) -> int:
        """
        Returns a random move from the list of possible moves.

        Returns:
            str: either "up", "down", "left", or "right"

        Example:
            >>> move = Move()
            >>> move.sample()
            "up"
        """
        return self.possible_moves.index(random.choice(self.moves))

    def contains(self, x) -> bool:
        """
        Check if the input is one of the 4 possible moves.


        Returns:
            bool: True if the input is one of the 4 possible moves, otherwise False.
        """
        return x in self.moves

    def moves_index_to_strings(agents):
        for agent in agents:
            move = agents[agent]
            agents[agent] = Move.possible_moves[move]

    def num_actions(self) -> int:
        return len(self.possible_moves)

    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        return "Move()"

    def __eq__(self, other) -> bool:
        return isinstance(other, Move)
