# importing libraries
import turtle as tr
import random
import time
import math

# allows custom gif files to be used as turtle shapes
tr.register_shape('aliveflower.gif')

# currentTask used to access indexes of tasks list during Interact function
global currentTask
currentTask = 0
# shapes list contains all gif files of items that will be created in the spawnItem function
global shapes
shapes = ['wateringcan.gif','grayflower.gif','bongacat.gif','treehive.gif','bee.gif']
# tasks list holds all the messages that will be displayed for user when they must complete a goal to move on or to mark the end of the game
tasks = ['Get the watering can!', 'Water the wilting flower!', 'Find the Bonga Cat, do the rain dance!', 'Obtain nectar from the flower!','Bring the honey back to the hive!','GAME OVER!']

# initializing screen
# fullscreen, title, background color light green
wn = tr.Screen()
wn.setup(width = 1.0, height = 1.0)
wn.title('Untitled Bee Game')
wn.bgcolor('#638C5D')

# prompts user for the name of their garden
# collects user input as a string
gardenName = tr.textinput('  :)', 'What will you name your garden?')

# printturtle's purpose is to display the introduction story and messages in tasks list
printturtle = tr.Turtle()
printturtle.hideturtle()
printturtle.penup()
printturtle.setpos(-300,100)
printturtle.color('#A63117')

# garden list will store all items so they can be accessed after they are spawned
global garden
garden = []

# variable i is used to keep track of which item is being spawned
global i
i=0

# proximity checking
# ensures that no items spawn within 100 units of each other
def proxcheck():
  global x
  global y
  global i
  global prox
  global checkpass
  # checkpass must be 0 every time so it counts correctly as well as allows while loop in spawnItem to happen after the first object
  checkpass = 0
  # produces random coordinates that the turtle will spawn at
  x = random.randint(-310,310)
  y = random.randint(-150,150)
  # checks distance of the object that is currently being spawned to each object that has already been spawned
  if exempt==False:
    for obj in garden:
      prox = math.sqrt(((obj.ycor()-y)**2)+((obj.xcor()-x)**2))
      # checks if distance is more than 100 hundred units
      if prox>100:
        checkpass+=1
  
# spawnItem function
def spawnItem(shape):
  global i
  global x
  global y
  global checkpass
  global exempt
  # allows each GIF file to be used as a turtle shape
  tr.register_shape(shape)
  # first item gets spawned without proximity checking
  if i==0:
    checkpass=-1
    exempt = True
    # as long as the object is not far away enough from all objects that have already spawned, coordinates will be randomized again and rechecked
  while checkpass<i:
    proxcheck()
  i+=1
  #after first object, no other objects will be exempt from proximity checking
  exempt = False
  # turtles gets initalized with coordinates and respective shape, then added to the garden list so that it's distance to the next object can be checked
  item = tr.Turtle()
  item.penup()
  item.shape(shape)
  item.setpos(x,y)
  garden.append(item)


style = ('small-caps', 14, 'normal')
# called to display the introduction story and task messages or the game over message
def write(text):
  printturtle.clear()
  printturtle.write(text, font=style)

printturtle.clear()
# output of user input
# story to provide context and player immersion
# explains UI that user can use to play the game
printturtle.write("It's a cloudy day in " + gardenName.upper() + " and the flowers are sad. You must\ntake care of the flower in order to obtain honey to bring\nback to the hive. Use the arrow keys to move and the X key\nto interact with objects.", font=('arial',12,'italic'))
# 4 seconds to read the text
time.sleep(4)
printturtle.setpos(-250, 160)
# first task gets presented
write("New Task: " + tasks[currentTask])

# uses shapes list to make a turtle for each shape
n = 0
for element in shapes:
  shape = shapes[n]
  # allows each gif file to be used as a turtle shape
  spawnItem(shape)
  n = n + 1
  
# bee is the turtle that the user can control
bee = garden[4]

# output of user input
# moves bee 10 pixels in the direction that the user has pressed with the arrow keys
def up():
  bee.sety(bee.ycor() + 10)
def left():
  bee.setx(bee.xcor() - 10)
def right():
  bee.setx(bee.xcor() + 10)
def down():
  bee.sety(bee.ycor() - 10)

# output of user input
# called when user presses 'x' button
def interact():
  global currentTask
  gameover = False

  # makes hitbox to determine whether the bee sprite is close enough to the object to interact with it
  # special cases for story-development, using same object for different tasks
  if currentTask==3:
    hitboxy = garden[1].ycor()
    hitboxx = garden[1].xcor()
  elif currentTask==4:
    hitboxy = garden[3].ycor()
    hitboxx = garden[3].xcor()
  # normal cases, objects spawned in order of tasks so variable currentTask can be used  to access the correct object in the list garden
  else:
    hitboxy = garden[currentTask].ycor()
    hitboxx = garden[currentTask].xcor()

  # checks to see if the bee within 40 units of the object that it needs to be next to
  if abs(bee.xcor()-hitboxx)<=40 and abs(bee.ycor()-hitboxy)<=40 and currentTask!=4:
    
    write('Task complete!')
    # move onto next task
    currentTask += 1

    time.sleep(1)

    if currentTask==2:
      # after recieivng water, the flower looks more full of life
      garden[1].shape('aliveflower.gif')
    elif currentTask==3:
      # after the 'bonga dance', the rain stops so the grass becomes lighter to imply that the sun has been uncovered by the clouds
      wn.bgcolor('#86DB79')
      # as long as the game isn't completed, write new task for user to see
    if gameover==False:
      write('New Task: ' + tasks[currentTask])
  # display only the game over meessage once all tasks are completed
  elif currentTask==4:
    write("Game over! The bees are happy!")
  # if the bee is not in range of the object that needs to be interacted with for the current task then instruct player to move closer
  else:
    write('Not in range, move closer.\n' + tasks[currentTask])

# allows user input
# calls the up/down/left/right/x functions when the respective key is pressed by user
wn.onkey(up, "Up")
wn.onkey(left, "Left")
wn.onkey(right, "Right")
wn.onkey(down, "Down")
wn.onkey(interact, "x")

wn.listen()

wn.mainloop()