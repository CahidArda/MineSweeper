from turtle import Screen, Turtle
from random import randint

class MyTurtle:

    def __init__(self):
        self.trt = Turtle()
        self.trt.hideturtle() #hide any MyTurtle

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
        self.number = 0

        self.mineTurtle = Turtle()
        self.mineTurtle.penup()
        self.mineTurtle.goto(self.x+self.boxSize/2, self.y-self.boxSize/2)
        self.mineTurtle.hideturtle()

    #creates a turtle and sends it to the center of the tile, makes it look like a turtle

    def drawMine(self):
        #self.mineTurtle.showturtle()   #didn't work, don't know why
        self.mineTurtle.write("X", False, "center")

    def drawNumber(self):
        self.mineTurtle.write(self.number, False, "center")
        
    #fill tile with a color
    def fillTile(self, color):
    	fillerTurtle = Turtle()
    	fillerTurtle.penup()
    	fillerTurtle.goto(self.x+1, self.y-1)

    	fillerTurtle.color(color)
    	fillerTurtle.begin_fill()
    	for i in range(3):
    		fillerTurtle.forward(self.boxSize)
    		fillerTurtle.right(90)
    	fillerTurtle.forward(self.boxSize)
    	fillerTurtle.end_fill()
    	fillerTurtle.hideturtle()
    
    def setSetting(self, newSetting):
        self.setting = newSetting

        if (newSetting=="mine"):
            self.mineTurtle.shape(imageMine)

    def getSetting(self):
        return self.setting


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

        self.tilesWithMine = [] #store indexes of boxes with mine
        self.numberTiles = []   #store indexes of tiles with number

        self.checkedTiles = []  #used when player clicks on an empty tile, keeps track of opened ("clickable") tiles

        #initialize every tile and store them in tiles array
        for y in range(numberOfBoxes[1]):
            subTiles = []
            subChecledTiles = []
            for x in range(numberOfBoxes[0]):
                subTiles.append(Tile(x*(boxSize+1),-y*(boxSize+1),boxSize, "empty"))
                subChecledTiles.append(False)
            self.tiles.append(subTiles)                 #fill tiles
            self.checkedTiles.append(subChecledTiles)   #fill checked tiles

        self.drawTileMap()  #draw tileMap
        self.fillTileMap()  #add mines

    def drawTileMap(self):
        for y in range(numberOfBoxes[1]+1): #draw vertical lines
            self.trt.drawLine(0, -(self.boxSize+1)*y, screenWidth, -(self.boxSize+1)*y)

        for x in range(numberOfBoxes[0]+1): #draw horizonral lines
            self.trt.drawLine((self.boxSize+1)*x, 0, (self.boxSize+1)*x, -screenHeight)

    #parameters are indexes of the tile
    def getTile(self, x, y):
        return self.tiles[y][x]

    #check if an index is within the tile map
    def withinLimits(self, xIndex, yIndex):
        return not ((xIndex<0) or (xIndex>=self.numberOfBoxes[0]) or (yIndex<0) or (yIndex>=self.numberOfBoxes[1]))

    #checks if we can 'check' (show as a part of the island), must be empty and not checked before
    def canBeChecked(self, cor):
        if (self.getTile(cor[0], cor[1]).getSetting()=="empty"):
            for i in self.checkedTiles:
                if (i==cor):
                    return False    #it is empty, but was checked before
            return True #it is empty and wasn't checked
        else:
            return False    #it isn't empty

    #adds a mine by creating a random integer. If there is a mine on the chosen spot already, calls itself again until it finds an empty spot
    def addMine(self):

        if (self.numberOfBoxes[0]*self.numberOfBoxes[1]==len(self.tilesWithMine)): #abort if there can't be as many mines as we want
            print("ERROR: Can't place more mines to the gamefield")
            return

        var = randint(0,self.numberOfBoxes[0]*self.numberOfBoxes[1]-1)
        cor = [var%numberOfBoxes[0],int(var/numberOfBoxes[0])]  #x and y index

        exists = False
        for i in self.tilesWithMine:
            if (i==cor):
                exists=True

        if (exists):    #if there is a mine on the randomly chosen spot, call yourself again for a new random number
            self.addMine()
        else:           #if there is no mine on the randomly chosen spot, proceed to add the mine
            self.tilesWithMine.append(cor)                      #add mine index to list
            tile = self.getTile(cor[0], cor[1])
            tile.setSetting("mine") #change setting of the mine

            #check surrounding spots to set setting to "number" or increment it's value
            for y in range(3):
                for x in range(3):
                    newCor = [cor[0]-1+x, cor[1]-1+y]
        
                    if (not self.withinLimits(newCor[0],newCor[1])):  #if index is out of bounds, pass
                        pass
                    else:
                        tile = self.getTile(newCor[0], newCor[1])                
                        if (tile.getSetting()=="mine"): #if there is a mine on the spot, pass
                            pass
                        elif (tile.getSetting()=="number"): #if tile is already a number
                            tile.number = tile.number + 1
                        else:   #if there is nothing on the spot, mark it as a number and add it to the list
                            tile.setSetting("number")
                            tile.number = tile.number+1
                            self.numberTiles.append(newCor)
                    
    #fill tile map with mines
    def fillTileMap(self):
        for i in range(self.numberOfMines):
            self.addMine()

    #show mines if the game ends
    def showMines(self):
        for i in range(self.numberOfMines):
            cor = self.tilesWithMine[i]
            self.getTile(cor[0],cor[1]).drawMine()
    
    def showIsland(self, xIndex, yIndex):
        tile = self.getTile(xIndex, yIndex)
        print("{}, {}", xIndex, yIndex)
        tile.fillTile("white")
        self.checkedTiles.append([xIndex, yIndex])        

        coordinatesToTry = [[xIndex-1, yIndex], [xIndex+1, yIndex], [xIndex, yIndex-1], [xIndex, yIndex+1]]

        for i in coordinatesToTry:
            if self.withinLimits(i[0], i[1]):
                if (self.canBeChecked(i)):
                    self.showIsland(i[0], i[1])


    
   #define action for clicking, temporarily set to paint tile white
    def click(self, x, y):
        xIndex = int(x/(self.boxSize+1))
        yIndex = -int(y/(self.boxSize+1))
        
        #three options as an answer: mine, empty, number
        #in case of mine, failiure
        #in case of number, reveal only the number
        #in case of empty, reveal island
        tile = self.getTile(xIndex, yIndex)
        answer = (tile.getSetting())
        print(answer)
        
        if (answer == "mine"):      #clicked on a mine, end game
            print("You need to show mines")
            self.showMines()
        elif (answer == "number"):  #clicked on a number, only show number
            print(tile.number)
            tile.drawNumber()       #clicked on an empty spot, show island
        else: #
            self.showIsland(xIndex, yIndex)
            

#settings
boxSize = 40
numberOfBoxes = [10,10]
numberOfMines = 10

screenWidth = numberOfBoxes[0]*(boxSize+1)-1
screenHeight = numberOfBoxes[1]*(boxSize+1)-1

screen = Screen()
screen.setup(screenWidth, screenHeight)
screen.setworldcoordinates(0,-screenHeight, screenWidth, 0)
screen.bgcolor("gray")

#store shapes
imageMine = "res/Mine.gif"
imageFlag = "res/Flag.gif"
screen.addshape(imageFlag)
screen.addshape(imageMine)

screen.tracer(0,0) #for making turtle instant

myMap = TileMap(numberOfBoxes, boxSize, numberOfMines)
screen.onclick(myMap.click) #set action for clicking
#myMap.showMines()
#myMap.getTile(2,2).drawNumber()

screen.update() #for making turtle instant
screen.mainloop()
