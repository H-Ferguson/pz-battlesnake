import functools
from typing import List
from pettingzoo import ParallelEnv
from pettingzoo.utils import parallel_to_aec, OrderEnforcingWrapper
from gym.spaces import Dict
from gymnasium.spaces import Text, Discrete, Box
import string

# Local Imports
from pz_battlesnake.constants import DEFAULT_COLORS
from pz_battlesnake.types.battlesnake_options import BattlesnakeOptions
from pz_battlesnake.wrapper import env_done, env_render, env_reset, env_setup, env_step
from pz_battlesnake.env.game import Game


def make_env(**kwargs):    
    """ """
    env = BaseEnv(**kwargs)

    # Set the metadata enviorment name
    env.metadata[
        "name"
    ] = f"battlesnake-{env._options.game_map}-{env._options.game_type}_v0"

    # Convert from MARL to AEC API
    env = parallel_to_aec(env)
    # Provides a wide vareity of helpful error checks
    env = OrderEnforcingWrapper(env)

    return env


class BaseEnv(ParallelEnv):
    """
    Implements a BaseEnv for the Battlesnake environment, in which all environments based on

    Args:
        width (int): The width of the environment. Default is 11
        height (int): The height of the environment. Default is 11
        num_agents (int): The number of agents in the environment. Default is 4
        colors (List[str]): The colors of the agents. Default is :py:data:`DEFAULT_COLORS`
        game_map (str): The game map to use. Default is "standard"
        game_type (str): The game type to use. Default is "standard"
    """

    metadata = {
        "render_modes": ["human", "ascii", "color"],
    }

    possible_moves: List[str] = ["up", "down", "left", "right"]

    def __init__(
        self,
        width: int = 11,
        height: int = 11,
        num_agents: int = 4,
        colors: List[str] = DEFAULT_COLORS,
        game_map: str = "standard",
        game_type: str = "standard",
    ):
        self.possible_agents = ["agent_" + str(i) for i in range(num_agents)]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        self.agent_selection = self.possible_agents[0]
        self.game = Game(
            width, 
            height
        )

        self._options = BattlesnakeOptions(
            width=width,
            height=height,
            colors=colors,
            game_map=game_map,
            game_type=game_type,
            names=self.possible_agents,
        )

        self.observation_spaces: Dict = dict(zip(self.possible_agents, [Box(low = 0, high = 5, shape=(width, height)) for _ in self.possible_agents]))
        self.action_spaces: Dict = dict(zip(self.possible_agents, [Discrete(4) for _ in self.possible_agents]))


    @functools.lru_cache(maxsize=0)
    def observation_space(self, agent=None) -> Box:
        """
        Todo:
            * Add Documentation for observation_space
        """
        return self.observation_spaces[agent]

    @functools.lru_cache(maxsize=0)
    def action_space(self, agent=None):
        """

        Todo:
            * Add Documentation for action_space
        """
        return self.action_spaces[agent]

    def render(self, mode="ascii"):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.

        Args:
            mode (str): The mode to render the environment in. Can be ``ascii`` or ``color``
        """
        if mode == "ascii" or mode == "color" or mode == "human":
            env_render(True if mode == "color" else False)
        else:
            assert False, "Valid render modes are 'ascii' and 'color'"


    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.

        Returns the observations for each agent

        Todo:
            * Add Example of return
        """
        self.agents = self.possible_agents[:]

        if seed:
            self._options.seed = seed
        else:
            self._options.seed = None
        observations = env_reset(self._options.options)
        self.game.load_from_dict(observations[self.possible_agents[0]]["observation"]["board"])
        observations = {}
        for agent in self.possible_agents:
            observations[agent] = self.game.board
        return observations

    def step(self, action):
        """
        step(action) takes in an action for each agent and should return the
            - observations
            - rewards
            - terminations
            - truncations
            - infos
        dicts where each dict looks like {agent_0: item_1, agent_1: item_2}

        Todo:
            * Add Example of return
        """
        if not action:
            self.agents = []
            return {}, {}, {}, {}, {}

        agents = env_step(self.moves_index_to_strings(action))

        observations = {}
        rewards = {}
        terminations = {}
        truncations = {}
        infos = {}

        for agent in agents:
            self.game.load_from_dict(agents[agent]["observation"]["board"])
            observations[agent] = self.game.board
            rewards[agent] = agents[agent]["reward"]
            terminations[agent] = agents[agent]["done"]
            truncations[agent] = False # cannot find any documentation for this field lol
            infos[agent] = agents[agent]["info"]

        if env_done():
            self.agents = []

        return observations, rewards, terminations, truncations, infos

    def moves_index_to_strings(self, agents):
        actions = {}
        for agent in agents:
            move = agents[agent]
            actions[agent] = self.possible_moves[move]
        return actions

    def get_board(self):
        return self.game.board

