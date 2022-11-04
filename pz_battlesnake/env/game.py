

class Snake():
  def __init__(self):
    self.id
    self.health

class Game():
  """
  A class for representing a battlesnake game

  Hopefully I can use this for a non broken observation state, but worst case 
  maybe I can make a quick AB prune tree :) (maybe both :eyes:)
  """
  EMPTY = 0
  SNAKE_HEAD = 1
  SNAKE_BODY = 2
  FOOD = 3 
  HAZARD = 4

  def __init__(
    self, 
    width: int = 11, 
    height: int = 11
  ):
    self.board = [[0 for x in range(width)] for y in range(height)] 
  
  def load_from_dict(self, game):
    food = game["food"]
    hazards = game["hazards"]
    snakes = game["snakes"]
    self.populate_food(food)
    self.populate_hazards(hazards)
    self.populate_snakes(snakes)
  
  def populate_food(self, food):
    for piece in food:
      x = piece["x"]
      y = piece["y"]
      self.place_item(x, y, self.FOOD)

  def populate_hazards(self, hazards):
    for hazard in hazards:
      x = hazard["x"]
      y = hazard["y"] 
      self.place_item(x, y, self.HAZARD)

  def populate_snakes(self, snakes):
    for snake in snakes:
      self.populate_snake(snake)

  def populate_snake(self, snake):
    head_x = snake["head"]["x"]
    head_y = snake["head"]["y"]
    self.place_item(head_x, head_y, self.SNAKE_HEAD)
    for body in snake["body"]:
      x = body["x"]
      y = body["y"]
      self.place_item(x, y, self.SNAKE_BODY)

  def place_item(self, x, y, what):
    self.board[x][y] = what

      