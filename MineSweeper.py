from turtle import Screen, Turtle
from random import randint

class MyTurtle:

    def __init__(self):
        self.trt = Turtle()

    def drawLine(self, x1, y1, x2, y2):
        self.trt.penup()
        self.trt.goto(x1,y1)
        self.trt.pendown()
        self.trt.goto(x2,y2)
        self.trt.penup()

class Tile:

    def __init__(self, x, y, boxSize, setting):
        self.x = x                  #store pixel x value
        self.y = y                  #store pixel y value
        self.boxSize = boxSize      #store universal box size value
        self.setting = setting      #store setting of the tile: "mine","empty","number"     "number" is not added currently

    #creates a turtle and sends it to the center of the tile, makes it look like a turtle
    def drawMine(self):
        mineTurtle = Turtle()
        mineTurtle.penup()
        mineTurtle.goto(self.x+self.boxSize/2, self.y-self.boxSize/2)
        mineTurtle.shape(imageMine)
    
    def setSetting(self, newSetting):
        self.setting = newSetting


class TileMap:
    
    def __init__(self, numberOfBoxes, boxSize, numberOfMines):
        self.tiles = []         #store every tile
        self.trt = MyTurtle()     #store main turtle, probably obselete

        self.numberOfBoxes = numberOfBoxes  #store number of boxes, array with two integers
        self.boxSize = boxSize              #stores universal size of boxes
        self.numberOfMines = numberOfMines  #stores number of mines to initialize

        #store screen width and height pixelwise
        self.screenWidth = numberOfBoxes[0]*(boxSize+1)-1   
        self.screenHeight = numberOfBoxes[1]*(boxSize+1)-1

        self.tilesWithMine = [] #store coordinates of boxes with mine

        #initialize every tile and store them in tiles array
        for y in range(numberOfBoxes[1]):
            subTiles = []
            for x in range(numberOfBoxes[0]):
                subTiles.append(Tile(x*(boxSize+1),-y*(boxSize+1),boxSize, "empty"))
            self.tiles.append(subTiles)

        self.drawTileMap()  #draw tileMap
        self.fillTileMap()  #add mines

    def drawTileMap(self):
        for y in range(numberOfBoxes[1]+1): #draw vertical lines
            self.trt.drawLine(0, -(self.boxSize+1)*y, screenWidth, -(self.boxSize+1)*y)

        for x in range(numberOfBoxes[0]+1): #draw horizonral lines
            self.trt.drawLine((self.boxSize+1)*x, 0, (self.boxSize+1)*x, -screenHeight)

    def getTile(self, x, y):
        return self.tiles[y][x]

    #adds a mine by creating a random integer. If there is a mine on the chosen spot already, calls itself again until it finds an empty spot
    def addMine(self):

        if (self.numberOfBoxes[0]*self.numberOfBoxes[1]==len(self.tilesWithMine)): #abort if there can't be as many mines as we want
            print("ERROR: Can't place more mines to the gamefield")
            return

        var = randint(0,self.numberOfBoxes[0]*self.numberOfBoxes[1]-1)
        cor = [var%numberOfBoxes[0],int(var/numberOfBoxes[0])]

        exists = False
        for i in self.tilesWithMine:
            if (i==cor):
                exists=True

        if (exists):
            self.addMine()
        else:
            self.tilesWithMine.append(cor)
            self.getTile(cor[0], cor[1]).setSetting("mine")

    #fill tile map with mines
    def fillTileMap(self):
        for i in range(self.numberOfMines):
            self.addMine()

    #show mines if the games ends
    def showMines(self):
        for i in range(self.numberOfMines):
            cor = self.tilesWithMine[i]
            self.getTile(cor[0],cor[1]).drawMine()
            

#settings
boxSize = 40
numberOfBoxes = [6,4]
numberOfMines = 5

screenWidth = numberOfBoxes[0]*(boxSize+1)-1
screenHeight = numberOfBoxes[1]*(boxSize+1)-1

screen = Screen()
screen.setup(screenWidth, screenHeight)
screen.setworldcoordinates(0,-screenHeight, screenWidth, 0)
screen.bgcolor("gray")
screen.tracer(0,0) #for making trutle instant

#store shapes
imageMine = "res/Mine.gif"
imageFlag = "res/Flag.gif"
screen.addshape(imageFlag)
screen.addshape(imageMine)

myMap = TileMap(numberOfBoxes, boxSize, numberOfMines)

myMap.showMines()

screen.update() #for making trutle instant
screen.mainloop()