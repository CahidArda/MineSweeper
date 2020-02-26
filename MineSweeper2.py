#Changes made after first edition:
#'Setting' value is removed from Tile objects, instead we only use 'number'. -1 is mine, 0 (default) is empty, positive values are 'tiles with number'
#Changed parameters of functions such that they always take indexes (indx) or pixel coordinates (cor) in an array

from turtle import Screen, Turtle
from random import randint

#purpose is to have a method for drawing a line
class MyTurtle:
    
    def __init__(self):
        self.trt = Turtle()
        self.trt.hideturtle()

    def drawLine(self, cor1, cor2):
        self.trt.penup()
        self.trt.goto(cor1[0], cor1[1])
        self.trt.pendown()
        self.trt.goto(cor2[0], cor2[1])
        self.trt.penup()

#an object for every tile on the game board
class Tile:

    def __init__(self, indx, tileSize):
        self.cor = [indx[0]*(tileSize+1), -indx[1]*(tileSize+1)]    #store pixel coordinates of the tile
        self.indx = indx                                            #store index values of the tile
        self.tileSize = tileSize                                    #store universal tile size
        self.number = 0                                             #number is: -1 when tile is a mine, 0 when it is empty, is a positive value when it is a number

        #a turtle to go to the middle of the tile as the tile is initiated, will be used to display values on the tile
        self.trt = Turtle()         
        self.trt.penup()
        self.trt.goto(self.cor[0]+tileSize/2, self.cor[1]-tileSize/2-10)
        self.trt.hideturtle()

    #fills the tile with the given colour when called
    def fillTile(self, color):
    	fillerTurtle = Turtle()
    	fillerTurtle.penup()
    	fillerTurtle.goto(self.cor[0]+1, self.cor[1]-1)

    	fillerTurtle.color(color)
    	fillerTurtle.begin_fill()
    	for i in range(3):
    		fillerTurtle.forward(self.tileSize)
    		fillerTurtle.right(90)
    	fillerTurtle.forward(self.tileSize)
    	fillerTurtle.end_fill()
    	fillerTurtle.hideturtle()

    #displays the content of the tile when called
    def showTileContent(self):
        if (self.number==-1):   #if tile is a mine
            self.trt.color("red")
            self.trt.write("X", False, "center", font=('bold'))
        elif (self.number==0):  #if tile is empty
            self.fillTile("white")
        elif (self.number==-2):
            self.trt.color("red")
            self.trt.write("You Are Die", False, "center", font=("Arial", 20, 'bold'))
        else:
            self.trt.write(self.number, False, "center")


class GameBoard:

    def __init__(self, numberOfTiles, numberOfMines, tileSize, screenSize, screen):
        self.trt = MyTurtle()   #used to draw the gameBoard
        self.screen = screen    #used to stop player input after failiure

        self.majorTile = Tile([0,0], screenSize[0]) #used to display endgame message
        self.majorTile.number = -2
        

        self.numberOfTiles = numberOfTiles  #stores the dimensions of the board in an array (indexwise)
        self.numberOfMines = numberOfMines  #stores the total number of mines
        self.tileSize = tileSize            #stores universal size of a tile
        self.screenSize = screenSize        #stores dimensions of the board (pixelwise)

        self.tilesWithMine = []     #keeps track of tiles with mine
        self.tilesWithNumber = []   #keeps track of tiles with number

        self.tiles = []             #stores every single tile object
        self.checkedTiles = []      #stores every revealed tile (used when we call recursion to reveal an island)

        #fill 'tiles' with Tile objects and 'checkedTiles' with False
        for y in range(numberOfTiles[1]):
            subTiles = []
            subCheckedTiles = []
            for x in range(numberOfTiles[0]):
                subTiles.append(Tile([x,y], self.tileSize))
                subCheckedTiles.append(False)
            self.tiles.append(subTiles)
            self.checkedTiles.append(subCheckedTiles)

        self.drawGameBoard()                   
        self.fillGameBoardWithMines() 
    
    def drawGameBoard(self):
        for y in range(self.numberOfTiles[1]+1):    #add vertical lines
            self.trt.drawLine( [0, -(self.tileSize+1)*y] , [self.screenSize[0], -(self.tileSize+1)*y] )

        for x in range(self.numberOfTiles[0]+1):     #draw horizonral lines
            self.trt.drawLine( [(self.tileSize+1)*x, 0] , [(self.tileSize+1)*x, -self.screenSize[1]] )

    def getTile(self, indx):
        return self.tiles[indx[1]][indx[0]]

    #checks if a given index is within the boundries of the gameboard
    def withinLimits(self, indx):
        x = indx[0]
        y = indx[1]
        return not ((x<0) or (x>=self.numberOfTiles[0]) or (y<0) or (y>=self.numberOfTiles[1]))

    def fillGameBoardWithMines(self):
        for i in range(self.numberOfMines):
            self.addMine()

    #creates a random index, places a mine if possible, updates neighbouring tiles' number
    def addMine(self):
        #abort if there was a call for addMine even though it is not possible to add more
        if (self.numberOfTiles[0]*self.numberOfTiles[1]==len(self.tilesWithMine)):
            print("ERROR: Can't place more mines to the gamefield")
            return 

        #create a random indx for new mine
        var = randint(0, self.numberOfTiles[0]*self.numberOfTiles[1]-1)
        indx = [var%numberOfTiles[0], int(var/numberOfTiles[0])]

        #check if there is a mine on the chosen spot
        exists = False
        for i in self.tilesWithMine:
            if (i==indx):
                exists=True

        if (exists):
            self.addMine()
        else:
            self.tilesWithMine.append(indx) #add tile index to the list 'tilesWithMine'
            self.getTile(indx).number = -1  #set the 'number' of the tile to be -1, which represents a mine

            #check neighbouring tiles to update them as a number tile
            for dy in range(3):
                for dx in range(3):
                    newIndx = [indx[0]-1+dx, indx[1]-1+dy]  #create an index for the neighbouring tile

                    if (not self.withinLimits(newIndx)):    #if index is out of bounds, pass
                        pass
                    else:
                        neighbourTile = self.getTile(newIndx)
                        if (neighbourTile.number==-1):      #if neighbouring tile was a mine, do nothing
                            pass
                        else:                               #else, it is a number or is empty, increment 'number' once
                            neighbourTile.number = neighbourTile.number+1

    #reveals the tile in given index, checks neighbouring tiles to see if they can be revealed (forming an island)
    def showIsland(self, indx):
        tile = self.getTile(indx)
        tile.showTileContent()          #show content, will fill it white in this case
        self.checkedTiles.append(indx)  #add to previously checked/updated tiles list

        #create an array of indexes of neighbouring tiles to check
        xIndx = indx[0]
        yIndx = indx[1]
        coordinatesToTry = [[xIndx-1, yIndx], [xIndx+1, yIndx], [xIndx, yIndx-1], [xIndx, yIndx+1], [xIndx+1, yIndx+1], [xIndx-1, yIndx-1], [xIndx-1, yIndx+1], [xIndx+1, yIndx-1]]

        #check 8 neighbouring tiles of the tile
        for neighbourIndx in coordinatesToTry:
            if self.withinLimits(neighbourIndx):
                neighbourTile = self.getTile(neighbourIndx)
                if (neighbourTile.number>0):    #if neighbour is a 'number' make it visible
                    neighbourTile.showTileContent()
                    self.checkedTiles.append(neighbourIndx)

                if (neighbourTile.number==0):   #if neighbouring cell is empty
                    #check if it was revealed before
                    itWasRevealed = False
                    for checkedTileIndx in self.checkedTiles:
                        if (checkedTileIndx==neighbourIndx):
                            itWasRevealed = True
                    
                    #if it wasn't revealed before, call method on the neighbouring tile
                    if (not itWasRevealed):
                        self.showIsland(neighbourIndx)                

    #show every mine on the game board in case of failiure
    def showMines(self):
        for i in self.tilesWithMine:
            self.getTile(i).showTileContent()

    #currently only serves the purpose of stopping player after a mine is clicked, will try to make it so that it will display a message everywhere it was called to
    def endGame(self, xCor, yCor):
        trt = Turtle()
        trt.penup()
        trt.goto(xCor, -yCor)
        trt.write("You Are Die", False, "center", font=("Arial", 20, 'bold'))

    #defines the actions after a mouse click
    def click(self, xCor, yCor):
        #convert pixel coordinates to indexes
        xIndex = int(xCor/(self.tileSize+1))
        yIndex = -int(yCor/(self.tileSize+1))

        tile = self.getTile([xIndex, yIndex])   #get the clicked tile
        tileNumber = tile.number
        print(tileNumber)                        #for debugging purposes

        if (tileNumber==-1):    #clicked tile has a mine
            print("show mines")
            self.showMines()
            self.majorTile.showTileContent()    #display "you are die"
            self.screen.onclick(self.endGame)
        elif (tileNumber==0):   #clicked tile is empty
            self.showIsland(tile.indx)
        else:                   #clicked tile is a number
            tile.showTileContent()

#settings
numberOfTiles = [20, 20]
numberOfMines = 40
tileSize = 32

screenSize = [numberOfTiles[0]*(tileSize+1)-1, numberOfTiles[1]*(tileSize+1)-1]

screen = Screen()
screen.setup(screenSize[0], screenSize[1])
screen.setworldcoordinates(0,-screenSize[1], screenSize[0], 0)
screen.bgcolor("gray")
screen.tracer(0,0)          #for making drawing instat

game = GameBoard(numberOfTiles, numberOfMines, tileSize, screenSize, screen)
print(game.tilesWithMine)
screen.onclick(game.click)  #set actions in case of mouse clicking

screen.update()             #for making drawing instat
screen.mainloop()