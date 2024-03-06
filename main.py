from tkinter import *
import random 
import simpleaudio as sa

pop = sa.WaveObject.from_wave_file("pop.wav")
uhhhh = sa.WaveObject.from_wave_file("uhhhh.wav")

SPACE_SIZE = 20
BODY_SIZE = 2

game_over_flag = False

score = 0
direction = 'down'

#keeping track of high score, and speed of game in which high score was achieved
high_score = 0
high_speed = 0

color_map = {
    "black": "#000000",  #hex numbers represents colors
    "white": "#FFFFFF", 
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "pink": "#FFC0CB",
    "orange": "#FFA500",
    "purple": "#800080",
    "grey": "#808080",
}


def get_window_size_input():
    size_map = {
        "small": 500,
        "medium": 650,
        "large": 800
    }

    while True:
        size_input = input("Enter window size (small, medium, large):\n").lower()
        if size_input in size_map:
            return size_map[size_input]
        else:
            print("Please enter 'small', 'medium', or 'large'.")

window_size = get_window_size_input()
WIDTH = window_size
HEIGHT = window_size

def get_speed_input():
   
    while True:
        
        user_input = input("\nSelect speed (25-200), lower is faster\nDefault (no input) is 100.\n\nSpeed: \n")
        
        if user_input.strip() == "":
            print("speed set to 100\n")
            return 100  #default
        
        try:
            speed = int(user_input)
            #hard
            if speed > 0 and speed <=50:
               print("good luck lol")
            #redundant
            elif speed == 100:
               print("couldve just entered but ok")
               print("speed set to 100\n")
            
            if 25 <= speed <= 200:
                return speed
            
            else:
               raise ValueError
            
        #not valid
        except ValueError:
            print("\n**Ivalid input**\n")

# set the speed to input
speed = get_speed_input()


def get_unique_color_input(prompt):
    while True:
        color = input(prompt).lower()
        if color in color_map:  
            return color
        else:
            print("Color is not mapped, please try another color: ")

def get_all_colors():
    
    while True:
        
        snake_color = get_unique_color_input("Set snake color: ")
        food_color = get_unique_color_input("Set food color: ")
        background_color = get_unique_color_input("Set background color: ")

        if snake_color != food_color and snake_color != background_color and food_color != background_color:
            return snake_color, food_color, background_color
        else:
            print("You cannot use the same color for more than one element. Please choose different colors.")

# Use the function to get the colors
SNAKE, FOOD, BACKGROUND = get_all_colors()

def start_game():
  start_canvas.pack_forget()
  setup_game()
  next_turn(snake, food)


def setup_game():
    global canvas, snake, food, score, direction
    score = 0
    direction = 'down'
    canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
    canvas.pack()
    load_high_score()
    update_score_label()
    snake = Snake()
    food = Food()
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))
    window.bind('r', restart_game)


#functions for score and highscore handling
def update_score_label():
    label.config(text=f"Points: {score}")

def save_high_score():
  with open('highscore.txt', 'w') as file:
    file.write(f"{high_score},{high_speed}")

def load_high_score():
    global high_score, high_speed
    try:
       with open('highscore.txt', 'r') as file:
          high_score, high_speed = map(int, file.read().split(','))
    ##no highscore file yet, make one w initial highscore,speed = 0
    except FileNotFoundError:
        high_score, high_speed = 0, 0
        with open('highscore.txt', 'w') as file:
            file.write(f"{high_score},{high_speed}")
    #file exists, cant be read, overwrite it with initial vals
    except ValueError:
        high_score, high_speed = 0, 0
        with open('highscore.txt', 'w') as file:
            file.write(f"{high_score},{high_speed}")


#constants user chooses: SPEED, COLORS: SNAKE, FOOD, BACKGROUND, WIDTH, HEIGHT

class Snake: 

  def __init__(self): 
    self.body_size = BODY_SIZE 
    self.coordinates = [] 
    self.squares = [] 

    for i in range(0, BODY_SIZE): 
      self.coordinates.append([0, 0]) 

    for x, y in self.coordinates: 
      square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE, tag="snake") 
      self.squares.append(square) 


# Class to design the food 
class Food: 

  def __init__(self): 

    x = random.randint(0, (WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
    y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE 

    self.coordinates = [x, y] 

    canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD, tag="food") 


# Function to check the next move of snake 
def next_turn(snake, food): 
  x, y = snake.coordinates[0] 

  if direction == "up": 
    y -= SPACE_SIZE 
  elif direction == "down": 
    y += SPACE_SIZE 
  elif direction == "left": 
    x -= SPACE_SIZE 
  elif direction == "right": 
    x += SPACE_SIZE 

  snake.coordinates.insert(0, (x, y)) 

  square = canvas.create_rectangle( 
    x, y, x + SPACE_SIZE, 
        y + SPACE_SIZE, fill=SNAKE) 

  snake.squares.insert(0, square) 

  if x == food.coordinates[0] and y == food.coordinates[1]: 
    global score 
    score += 1
    pop.play()
    update_score_label()
    canvas.delete("food") 
    food = Food() 
  #creates movement effect
  else: 
    del snake.coordinates[-1] 
    canvas.delete(snake.squares[-1]) 
    del snake.squares[-1] 

  if check_collisions(snake): 
    game_over() 
    uhhhh.play()

  else: 
    window.after(speed, next_turn, snake, food) 


# Function to control direction of snake 
def change_direction(new_direction): 
  global direction 

  if new_direction == 'left': 
    if direction != 'right': 
      direction = new_direction 
  elif new_direction == 'right': 
    if direction != 'left': 
      direction = new_direction 
  elif new_direction == 'up': 
    if direction != 'down': 
      direction = new_direction 
  elif new_direction == 'down': 
    if direction != 'up': 
      direction = new_direction 


# function to check snake's collision and position 
def check_collisions(snake): 
  x, y = snake.coordinates[0] 

  if x < 0 or x >= WIDTH: 
    return True
  elif y < 0 or y >= HEIGHT: 
    return True

  for body_part in snake.coordinates[1:]: 
    if x == body_part[0] and y == body_part[1]: 
      return True

  return False

def game_over(): 
    
    global game_over_flag, high_score, high_speed, score
    game_over_flag = True

    if score > high_score:
      high_score = score
      high_speed = speed
      save_high_score()

    canvas.delete(ALL)
    # Determine rectangle and text color
    rect_color = "black" if BACKGROUND == "red" else "red"
    text_color = "white"
    rect_x1 = WIDTH // 8  # Start more to the left
    rect_y1 = HEIGHT // 3  # Start lower than before
    rect_x2 = 7 * WIDTH // 8  # End more to the right
    rect_y2 = 2 * HEIGHT // 3  # End higher than before

    # Create a rectangle in the middle of the screen with adjusted dimensions
    canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill=rect_color, outline="black")
    # Create game over text
    canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="You died! Press 'r' to retry.", fill=text_color, font=('Helvetica', 20, 'bold'))

    # Create high score text
    highscore_text = f"Highscore: {high_score} with speed: {high_speed}"
    canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, text=highscore_text, fill=text_color, font=('Helvetica', 16))

   
def restart_game(event):
  global game_over_flag, snake, food, score, direction
  if game_over_flag:
    canvas.delete(ALL)
    score = 0
    direction = 'down'
    update_score_label()
    snake = Snake()
    food = Food()
    next_turn(snake, food)
    game_over_flag = False


def update_button_style(event=None):
    play_button.config(bg="green", activebackground="green")

#setting shit up
# Setting up the main window
window = Tk()
window.title("Snake Game")

label = Label(window, text=f"Points: {score}  Highscore: {high_score} with speed: {high_speed}", font=('consolas', 20))
label.pack(side=TOP)

# Start screen setup
start_canvas = Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
start_canvas.pack()

play_button = Button(window, text=u"\u25B6", font=("Helvetica", 20), 
                     bg="green", fg="white", activebackground="green", 
                     highlightbackground="green", command=start_game, 
                     highlightthickness=0)
play_button_window = start_canvas.create_window(WIDTH // 2, HEIGHT // 2, window=play_button)

window.bind("<FocusIn>", update_button_style)

# Main game setup (deferred until the play button is clicked)
setup_game()
canvas.pack_forget()

# Set window size explicitly to be slightly larger than the canvas
window_size_padding = 40  # Extra space to accommodate other elements
window.geometry(f"{WIDTH}x{HEIGHT + window_size_padding}")

# Center the window on the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (WIDTH // 2)
y = (screen_height // 2) - ((HEIGHT + window_size_padding) // 2)
window.geometry(f"+{x}+{y}")

# Start the main event loop
window.mainloop()