# Copyright SAGA 2019
# Not to be duplicated without express consent of
# original members. Not for release. 
#
# Note: Layer 0 is for loading screens, layer 1 is for menu text/sprites, layer 2 is for menus, 3-5 for sprites, 6 for background
#
#
#
#
#
#
#
#
#
#
#
#
#.


import random
import gui
import time
import thread
import os




        ####################
        #                  #
        #     CONSTANTS    #
        #                  #
        #    (MIGHT BE     #
        #     MOVED TO     #
        #  STARTUP CLASS)  #
        #                  #
        #                  #
        ####################


        # used for movement animations. Lowest stable is .12
moveAnimationSleep = .12  # any lower and coords get messed up


#BITS is how many pixels are in each texture
BITS = 32
#how many tiles there are wide
WIDTHTILES = 32
#how many tiles there are tall
HEIGHTTILES = 18

TOWNAREA = None
FIELDAREA = None
DUNGEONAREA = None
currentArea = None

class TurnCounter():
    def __init__(self):
        self.turn = 0


counter = TurnCounter()


    #CONTAINERS
#beings	
currentBeingList = []
#interactable objects
objectList = []
#gore pieces	
gibList = []
#animated sprites
animatedSpriteList = []
#light sources
lightSources = []


##class CoreGame():   experimented with a class to hold game data. could be addressed later
#    def __init__(self):
        #add select game folder (to allow more portable loading of assets to path)
try:
           path #test to see if path exists
except NameError: #if path does not exist make new path
           printNow("Please select your game install folder")
           path = pickAFolder()
else: printNow("Welcome Back") #welcome the player back to the game






userSpritePaths = [path + "RobotSprites/botBlueBack.gif",
               path + "RobotSprites/botBlueFront.gif",
               path + "RobotSprites/botBlueSideLeft.gif",
               path + "RobotSprites/botBlueSideRight.gif",
               path + "RobotSprites/botBlueMovingLeft.gif",
               path + "RobotSprites/botBlueMovingRight.gif",]
friendlyGreenSpritePaths = [path + "RobotSprites/botGreenBack.gif",
               path + "RobotSprites/botGreenFront.gif",
               path + "RobotSprites/botGreenSideLeft.gif",
               path + "RobotSprites/botGreenSideRight.gif",
               path + "RobotSprites/botGreenMovingLeft.gif",
               path + "RobotSprites/botGreenMovingRight.gif",]
friendlyOrangeSpritePaths = [path + "RobotSprites/botOrangeBack.gif",
               path + "RobotSprites/botOrangeFront.gif",
               path + "RobotSprites/botOrangeSideLeft.gif",
               path + "RobotSprites/botOrangeSideRight.gif",
               path + "RobotSprites/botOrangeMovingLeft.gif",
               path + "RobotSprites/botOrangeMovingRight.gif",]
blueEnemySpritePaths = [path + "RobotSprites/blueRobotBack.gif",
               path + "RobotSprites/blueRobotFront.gif",
               path + "RobotSprites/BlueRobotSideLeft.gif",
               path + "RobotSprites/BlueRobotSideRight.gif",
               path + "RobotSprites/BlueRobotMovingLeft.gif",
               path + "RobotSprites/BlueRobotMovingRight.gif",]
shopKeeperSpritePaths = [path + "RobotSprites/ShopkeeperbotCloseup.gif",
                         path + "RobotSprites/ShopkeeperbotFront.gif"]
lightpostSpritePaths = [path + "ObjectSprites/lampOff.gif",
                        path + "ObjectSprites/lampOn.gif",
                        path + "ObjectSprites/lampBright.gif"]
torchSpritePaths = [path + "ObjectSprites/metalTorchOff.gif",
                        path + "ObjectSprites/metalTorchOn1.gif.gif",
                        path + "ObjectSprites/metalTorchOn2.gif.gif"]

bigTorchSpritePaths = [path + "ObjectSprites/metalBigTorchOff.gif",
                        path + "ObjectSprites/metalBigTorchOn1.gif",
                        path + "ObjectSprites/metalBigTorchOn2.gif"]

# Dictionaries for items
# Numbers correspond to stats
# arrays in form [attack/def, spritePaths, isBurnable (for weapons only)]
weaponStatsList = {    
    "Stick": [1, [path + "WeaponSprites/Stick/stickUp.gif",
                  path + "WeaponSprites/Stick/stickDown.gif",
                  path + "WeaponSprites/Stick/stickLeft.gif",
                  path + "WeaponSprites/Stick/stickRight.gif"], true, [path + "WeaponSprites/Stick/stickFireUp.gif",
                  path + "WeaponSprites/Stick/stickFireDown.gif",
                  path + "WeaponSprites/Stick/stickFireLeft.gif",
                  path + "WeaponSprites/Stick/stickFireRight.gif"]],
   "Rock": [2, "spritePath"]
   }
helmStatsList = {
    "Hair": [0, "spritePath"],
    "Leaf": [1, "spritePath"]
    }
chestStatsList = {
    "BDaySuit": [0, "spritePath"],
    "Fur Coat": [1, "spritePath"]
    }
legsStatsList = {
    "Shame": [0, "spritePath"],
    "Fur Pants": [1, "spritePath"]
    }
feetStatsList = {
    "Toes": [0, "spritePath"],
    "Fur Boots": [1, "spritePath"]
    }
handStatsList = {
    "Digits": [0, "spritePath"],
    "Fur Gloves": [1, "spritePath"]
    }
itemsList = {}  #potions, etc.


lootTable = {}


directionList = {
    "up": 0,
    "down": 1,
    "left": 2,
    "right": 3,
    "movingLeft": 4,
    "movingRight":5
    }

mapNameList = ["town", "dungeon", "path"]




        ####################
        #                  #
        #    FUNCTIONS     #
        #                  #
        ####################




# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Converts the given rawText to a Label object to be added to the 
# display, then adds at coordsX, coordsY. 



def showText(rawText, coordsX = 1280 * (2/5), coordsY = 0):
    label = gui.Label(rawText)
    display.add(rawText, coordsX, coordsY)








# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Adds the given gui.Label to the display at the Label's coords (default 0, 0)

def showLabel(label):
    display.add(label, 1280*(2/5), 0)





# All actions that depend on the turn counter go here

def turnPass():
    counter.turn += 1
    if counter.turn % 20 == 0 and currentArea != TOWNAREA:
        spawnEnemy()
    for person in currentBeingList:
        if person.hostile == true:
            person.simpleHostileAI()
    if bot1.hp <= 0:
        bot1.coords.x = 0
        bot1.coords.y = 0
        bot1.sprite.spawnSprite()
    clearBadSprites()
    #if coords offscreen, load next screen, clear gore, delete old beings? leave their logic? but then they will move around/spawn.
    #maybe split being list into active and passive? 

    #total action counter to affect shop/store stock
    




    # slides an object to the right one pixel at a time until the object's coords.x == targetXBig.
    # parameters:
    # object        - object to be moved (must have a sprite)
    # targetXBig    - x coord target (must be greater than object.coords.x)

def slideRight(toBeMoved, targetXBig):
    time.sleep(.005)
    toBeMoved.coords.x += 1 
    toBeMoved.forwardCoords.x += 1
    display.add(toBeMoved.sprite, toBeMoved.coords.x, toBeMoved.coords.y)
    if toBeMoved.coords.x < targetXBig:
        thread.start_new_thread(slideRight, (toBeMoved, targetXBig, sprite))





def loadAreaCheck(player):
  global FIELDAREA
  global DUNGEONAREA
  global TOWNAREA
  global currentArea
  if currentArea == TOWNAREA:
    if player.coords.y <= 0:
      loadNewArea(DUNGEONAREA)
      bot1.area = DUNGEONAREA
    elif player.coords.x >= 992:
      loadNewArea(FIELDAREA)
      bot1.area = FIELDAREA
  elif currentArea == FIELDAREA:
    if player.coords.x <= 0:
      loadNewArea(TOWNAREA)
      bot1.area = TOWNAREA
    elif player.coords.y >= 544:
      player.coods.x = -32
      player.coords.y = 256
      player.moveRight()
  elif currentArea == DUNGEONAREA:
    if player.coords.x <= 0:
      player.coords.y = 576
      player.coords.x = 480
      player.moveUp()
    elif player.coords.y >= 544:
      loadNewArea(TOWNAREA)
      bot1.area = TOWNAREA





# Spawns an enemy with the given parameters.  Default is blue enemy lv 1 with stick at random location.

def spawnEnemy(name = ("EnemyBorn" + str(counter.turn)), weap = "Stick", spritePaths = blueEnemySpritePaths,  x = random.randint(0, 10)*32, y =  random.randint(0, 10)*32, species = "orc", level = 1):
    while not isTraversable(x, y):
        x = random.randint(0, 10)*32
        y =  random.randint(0, 10)*32
    enemy = Enemy(name, weap, spritePaths, x, y, species, level)
    enemy.sprite.spawnSprite()
    





# Used to remove objects (labels, sprites, etc.) from the display after a delay.
# only call delayRemoveObject.  threadDelayRemoveObject() is not meant to be called
# directly.
# Parameters:
#   object          - An object on the displays self.items list
#   delay           - the amount of time in seconds to delay the removal

def delayRemoveObject(object, delay):
    thread.start_new_thread(threadDelayRemoveObject, (object, delay))
def threadDelayRemoveObject(object, delay):
    time.sleep(delay)
    display.remove(object)






# cleanup for duplicate sprites created when input is given
# too quickly

def clearBadSprites():
    goodSprites = []
    for being in currentBeingList:
        goodSprites.append(being.sprite)
    for sprite in display.items:
        if sprite not in goodSprites and type(sprite) == BeingSprite:
            display.remove(sprite)







# clears giblets from the display()

def clearGibList():
    for sprite in gibList:
        display.remove(sprite)
        gibList.remove(sprite)
        del sprite






# used with thread.start_new_thread(threadRemoveSprite, (timeToWait, sprite))
# in order to despawn a sprite after a delay. For use with animations.
# parameters:
#   timeToWait      - time in seconds to delay the sprite removal
#   sprite          - sprite to be removed

def threadRemoveSprite(timeToWait, sprite):
    time.sleep(timeToWait)
    display.remove(sprite)






#helper Functions
def spotToCoord(spot):
    #if low set to 0d
    if spot < 0: spot = 0
    #if high set to max (should probably just throw error
    if spot > WIDTHTILES * HEIGHTTILES: spot = WIDTHTILES * HEIGHTTILES - 1
    return Coords(spot % WIDTHTILES, spot / WIDTHTILES)


#given tile Coords give tile Spot in 1d array
def tileCoordToSpot(coord):
    return coord.x + coord.y * WIDTHTILES


#Goes from pixel coords to tile Coords
def coordToTileCoord(coord):
    return Coords(coord.x/bits, coord.y/BITS)


#probably bad?
def coordToTile(coord):
    return coord.x/BITS + (coord.y/BITS) * WIDTHTILES

#takes pixel coordanates and returns if the tile at that location is
def isTraversable(x, y):
    spot = coordToTile(Coords(x,y))
    printNow(spot)
    return currentMap.isTraversable(spot)


#depricated can Delete
def placeTex(tex, spot, back):
    startx = (spot * BITS) % backWidth;
    starty = ((spot * BITS) / backWidth) * bits;
    for x in range(0, BITS):
        for y in range(0, BITS):
            setColor(getPixel(back, startx + x, starty + y), getColor(getPixel(tex, x, y)))




def textCoordToSpot(x, y):
  col = texWidth/32
  row = texHeight/32
  return x + y*col

def getTexture(spot):
    texture = makeEmptyPicture(bits,BITS)
    #spot to coord conversion
    startx = (spot * BITS) % texWidth;
    starty = ((spot * BITS) / texWidth) * bits;
    for x in range(0, BITS):
        for y in range(0, BITS):
            setColor(getPixel(texture, x, y), getColor(getPixel(textureMap, x + startx, y + starty)))
    return texture






# intro credits, adjust to add fade, etc.

def loadIntro():
    display.drawImage(path + "Fullscreens/LogoOmega.png", 0, 0)
    time.sleep(1.5)
    display.drawImage(path + "Fullscreens/dummyStartScreen.png", 0, 0)
    time.sleep(1.5)




def loadingScreen():
    display.removeAll()
    setUpLayers()
    loading.spawnSprite()


def loadNewArea(area):
    loadingScreen()
    setUpLayers()
    bot1.coords = area.spawnCoords
    global currentBeingList
    global gibList
    global animatedSpriteList
    global lightSources
    global text
    global display
    global currentBg
    global currentMap
    global currentArea
    currentArea = area
    bot1.area = area
    currentMap = area.mapObject
    currentBg = area.mapSprite
    currentBg.spawnSprite()
    display.add(text)
    currentBeingList.remove(bot1)
    currentBeingList = area.beingList
    currentBeingList.append(bot1)
    objectList = area.objectList
    gibList = area.gibList
    animatedSpriteList = area.animatedSpriteList
    lightSources = area.lightSources
    for being in currentBeingList:
      being.sprite.spawnSprite()
    for thing in objectList:
        thing.sprite.spawnSprite()
    for gib in gibList:
        gib.spawnSprite
    for sprite in newAnimatedSprites:
        sprite.spawnSprite()
        sprite.animate()
    for light in newLightSources:
        light.sprite.spawnSprite()
    loading.removeSprite()


def setUpLayers():
    # DO NOT REMOVE LAYERS, needed for layer positioning of sprites
    # Layer 0 for menus, 1-3 for sprites, 4 for backgrounds
    layer0.spawnSprite()
    layer1.spawnSprite()
    layer2.spawnSprite()
    layer3.spawnSprite()
    layer4.spawnSprite()
    layer5.spawnSprite()
    layer6.spawnSprite()
                              
# any function passed to onKeyType() must have one and exactly one
# parameter.  This parameter is how the function knows which key is pressed


def keyAction(a):
  bot1Ready = (bot1.weapon.displayed == false and bot1.isMoving == false)
  if a == "w":
    if bot1Ready:        
        bot1.isMoving = true
        bot1.moveUp()
        turnPass()
        loadAreaCheck(bot1)
  elif a == "s":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveDown()
        turnPass()
        loadAreaCheck(bot1)
  elif a == "a":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveLeft()
        turnPass()
        loadAreaCheck(bot1)
  elif a == "d":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveRight()
        turnPass()
        loadAreaCheck(bot1)
  elif a == "W":
        bot1.faceUp()
  elif a == "A":
        bot1.faceLeft()
  elif a == "S":
        bot1.faceDown()
  elif a == "D": 
        bot1.faceRight()

  elif a == "f": #attack
    if bot1Ready:
        bot1.meleeAtk()
        turnPass()
  elif a == "g": #steal
    if bot1Ready:
        bot1.steal(bot1.getFrontTarget())
        turnPass()
  elif a == "q": 
    print("NotImplementedAtAll")
  elif a == "t":
    print("not implemented")
  elif a == "v":
    bot1.talk()
  elif a == " ":
      bot1.activateTarget()






    # To pass to getKeyTyped in order to block inputs 
    # (e.g., during animations or delays)

def blockKeys(a):
    None





          
# Currently only sets up the lootTable

def initialSetup():
    for item in weaponStatsList:
        lootTable[item] = weaponStatsList[item]
    for item in helmStatsList:
        lootTable[item] = helmStatsList[item]
    for item in chestStatsList:
        lootTable[item] = chestStatsList[item]
    for item in legsStatsList:
        lootTable[item] = legsStatsList[item]
    for item in feetStatsList:
        lootTable[item] = feetStatsList[item]





        
  





        ####################
        #                  #
        #      CLASSES     #
        #                  #
        ####################


class Area():
    def __init__(self, mapSprite, mapObject, spawnLocation):
        self.beingList = []
        self.objectList = []
        self.gibList = []
        self.animatedSpriteList = []
        self.lightSources = []
        self.mapSprite = mapSprite
        self.mapObject = mapObject
        self.spawnCoords = spawnLocation

# universal coordinates object 

class Coords():
  def __init__(self, x, y):
    self.x = x
    self.y = y


class Tile():
  def __init__(self, isTraversable, isPassable, isTough, desc):
    self.desc = desc
    #self.tileImg = tile
    #can a being walk over
    self.isTraversable = isTraversable
    #can a projectile go over
    self.isPassable = isPassable
    #ai gets 2 turns if player is on this tile
    self.isTough = isTough
    self.beings = {} #array of beings in that tile

  def getTraversable(self):
    return self.isTraversable

  def addBeing(self, being):
    self.beings.append(being)

  def getDesc(self):
    return self.desc


class Map():
    def __init__(self, tileMap, back):
        self.map = back
        self.tileMap = {} #change to make map
        #beings will probably be a dictionary with coords as the key and value is the being at the spot
        self.beings = {} #master holder for all of the beings
        #self.Map = makeEmptyPicture(backWidth, backHeight) #704 is chosen because its divisible by 32
        self.updateMap(tileMap)
        #for key, value in self.tileMap.iteritems():
            #printNow(key)

    def placeTex(self, tex, spot):
        self.tileMap.update({spot: tex})


    def placeStruct(self, struct, spot):
        startx = (spot * BITS) % backWidth
        starty = ((spot * BITS) / backWidth) * bits
        structWidth = getWidth(struct) / bits
        structHeight = getHeight(struct) / bits
        for structx in range(0, structWidth):
            for structy in range(0, structHeight):
                curr = spotToCoord(spot)
                newSpot = tileCoordToSpot(Coords(curr.x + structx, curr.y + structy))
                self.tileMap.update({newSpot: blank}) #replace water with a blank tile


    def updateMap(self, tiles):
        for spot in range(0, len(tiles)):
            if   tiles[spot] == "g": self.placeTex(grass, spot)
            elif tiles[spot] == "s": self.placeTex(stone, spot)
            elif tiles[spot] == "l": self.placeTex(lavaRock, spot)
            elif tiles[spot] == "d": self.placeTex(dirt, spot)
            elif tiles[spot] == "w": self.placeTex(water, spot)
            elif tiles[spot] == "L": self.placeTex(lava, spot)
            elif tiles[spot] == "f": self.placeTex(fence, spot)
            elif tiles[spot] == ".": self.placeTex(blank, spot)
            elif tiles[spot] == ",": self.placeTex(blank, spot)
            elif tiles[spot] == "o": self.placeTex(door, spot)
            elif tiles[spot] == "h": self.placeStruct(house, spot)
            elif tiles[spot] == "t": self.placeStruct(tree1, spot)

    def isTraversable(self, spot):
        printNow(spot)
        if spot < 0 or spot > len(self.tileMap) - 1: return false
        printNow(self.tileMap[spot].getTraversable())
        printNow(self.tileMap[spot].getDesc())
        return self.tileMap[spot].getTraversable()







# class for placeable objects (torches, trees, blocks, tc.)

class Doodad():
    def __init__(self, filepaths, x, y, layer = 3):
        self.destructible = false
        self.sprites = filepaths
        self.coords = Coords(x, y)
        self.layer = layer
        self.spriteList = filepaths
        self.sprite = Sprite(filepaths[0], self, layer)
        self.sprite.spawnSprite()
        self.isAnimating = false
        self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], x, y, self.layer)
        objectList.append(self)


# special animated doodad that emits light within 3 tiles. if is burnable, attacking
# with an onFire weapon will turnOn the light source

class LightSource(Doodad):
    def __init__(self, filepaths, x, y, burnable = false, layer = 3):
        Doodad.__init__(self, filepaths, x, y, layer)
        self.isOn = false
        self.type = "light"
        self.isBurnable = burnable
        lightSources.append(self)

    def activate(self):
        if self.isOn == true:
            self.turnOff()
        else:
            self.turnOn()

    def turnOn(self):
        if self.isOn == false:
            self.isOn = true            
            self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], self.coords.x, self.coords.y, self.layer)
            self.animatedSprite.animate()
            for being in currentBeingList:
                distanceX = abs(being.coords.x - light.coords.x)
                distanceY = abs(being.coords.y - light.coords.y)
                if distanceX <= bits*3 and distanceY <= range:
                    being.lightenDarken()
            #self.sprite.removeSprite()
    def turnOff(self):
        if self.isOn == true:
            self.isOn = false
            animatedSpriteList.remove(self.animatedSprite.spriteList[0])
            animatedSpriteList.remove(self.animatedSprite.spriteList[1])
            self.sprite.removeSprite()
            self.sprite.spawnSprite()
            for being in currentBeingList:
                distanceX = abs(being.coords.x - light.coords.x)
                distanceY = abs(being.coords.y - light.coords.y)
                if distanceX <= bits*3 and distanceY <= range:
                    being.lightenDarken()

    






# Class for merchant items and "buy/sell" transaction

class ItemForSale():
    def __init__(self, price, item):
        self.price = price
        self.item = item

    def buy(self, buyer, seller):
        buyer.inventoryAdd(self.item)
        buyer.changeWallet(self.price * - 1)
        seller.changeWallet(self.price)
        seller.inventoryRemove(self)
        del self
        


class Lootbag():
    def __init__(self, itemList, coords):
        self.contents = itemList
        self.coords = coords
        self.spriteList = [Sprite(path + r"EffectSprites/lootBag.gif", self),
                           Sprite(path + r"EffectSprites/lootBag2.gif", self)]
        self.sprite = self.spriteList[0]
        self.type = "lootbag"
        
        self.spawnSprite()
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))






    def spawnSprite(self):
        display.place(self.sprite, self.coords.x, self.coords.y, 1)
    def removeSprite(self):
        display.remove(self.sprite)



    def threadAnimate(self, x):
        while self in objectList:
            time.sleep(.5)
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in objectList:
            self.removeSprite()
            del self


        

# Class used when an ownerless sprite is needed

class RawSprite():
    def __init__(self, filename, x, y, layer = 4):
        self.coords = Coords(x, y)
        self.sprite = Sprite(filename, self, layer)
    def spawnSprite(self):
        self.sprite.spawnSprite()
    def spawnSpriteFront(self):
        self.sprite.spawnSpriteFront()
    def spawnSpriteBack(self):
        self.sprite.spawnSpriteBack()
    def removeSprite(self):
        self.sprite.removeSprite()

# general class for sprites. 
# to display on the main screen.
# parameters: 
#   filename    - filename in string format
#   parental      - object that owns this instance. must have it's own coords
#   layer       - screen layer of sprite, 0 closest to front

class Sprite(gui.Icon):

  def __init__(self, filename, parental, layer = 4):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM- LEGACY, NOT SURE OF NECESSITY
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, NOT SURE OF NECESSITY
      self.position = (0,0)              # assume placement at a Display's origin- LEGACY, NOT SURE OF NECESSITY
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, NOT SURE OF NECESSITY
      self.layer = layer
      self.parental = parental

      printNow(filename)
      self.icon = gui.ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality)- LEGACY, NOT SURE OF NECESSITY
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self):
        display.place(self, self.parental.coords.x, self.parental.coords.y, self.layer)
 
      # adds the sprite to the display in the foreground (closest to the user)

  def spawnSpriteFront(self):
      self.layer = 3
      self.spawnSprite()

      
      # adds the sprite to the display in the background (closest to the map, just in front of it)
      # order number of 3 spawns behind the background

  def spawnSpriteBack(self):
      self.layer = 5
      self.spawnSprite()

      # removes the sprite from the display
        
  def removeSprite(self):
        display.remove(self)











                     
  # inherits from Sprite. Separated to give   See sprite for function exacts. 
  # ownership to sub-sprites (e.g., weapon)

class BeingSprite(Sprite):
  def __init__(self, filename, parental, layer = 4):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM - LEGACY, UNUSED FOR NOW
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, UNUSED FOR NOW
      self.position = (0,0)              # assume placement at a Display's origin - LEGACY, UNUSED FOR NOW
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, UNUSED FOR NOW
      self.icon = gui.ImageIO.read(File(filename))
      self.parental = parental
      self.layer = layer
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality) - LEGACY, UNUSED FOR NOW
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self):
        display.place(self, self.parental.coords.x, self.parental.coords.y, self.layer)





        
      # removes the sprite

  def removeSprite(self):
        display.remove(self)




        
      # not a huge fan of the weaponOut flag, but it works for now.
      # without the check in putAwayWeap, JES complains  

  def displayWeapon(self, sprite, coords):
    display.add(sprite, coords.x, coords.y)





       
      # hides the weapon. may be unnecessary if we get
      # animations figured out

  def hideWeapon(self):
      display.remove(self.weap)





           
      #moves sprite to location given

  def moveTo(self, x, y):
      self.parental.coords.x = x
      self.parental.coords.y = y
      display.add(self, x, y)











          
    # Class for weapon objects. weapName must correspond to a weapon
    # in the weaponList. Contains stats and sprites.
    #
    #
    #
    #spritePaths should be array of order [up, down, left, right]


class Weapon():
    def __init__(self, weapName):
        self.name = weapName
        if self.name != None:
          self.originalSprites = weaponStatsList[self.name][1]
          self.coords = Coords(0, 0)
          self.sprites = self.originalSprites
          self.burningSprites = weaponStatsList[self.name][3]
          self.sprite = Sprite(self.sprites[3], self)
          self.power = weaponStatsList[self.name][0]
          self.isBurnable = weaponStatsList[self.name][2]
          self.onFire = false
        self.displayed = false

    def burn(self):
        x = None
        self.onFire = true
        self.sprites = self.burningSprites
        thread.start_new_thread(self.threadFireCountdown, (x, ))

    def threadFireCountdown(self, x):
        start = counter.turn
        finish = start + 15
        while counter.turn < finish:
            None
        self.onFire = false
        self.sprites = self.originalSprites
    





        # Displays the weapon's "up/down/left/right" sprite at the coords.
        # For use with being's "self.forwardCoords.x/y" 
        
    def displayUp(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[0], self)
            display.add(self.sprite, x, y)
            self.displayed = true
                        
    def displayDown(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[1], self)
            display.add(self.sprite, x, y)
            self.displayed = true
           
    def displayLeft(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[2], self)
            display.add(self.sprite, x, y)
            self.displayed = true
            
            
    def displayRight(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[3], self)
            display.add(self.sprite, x, y)
            self.displayed = true
          






        # removes the weapon from the display

    def hide(self):
        display.remove(self.sprite)
        self.displayed = false










        

    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the currentBeingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location

class Being():
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        self.name = name
        self.level = 0
        self.hp = 10
        self.maxHp = 10
        self.xp = 0
        self.atk = 5
        self.df = 5
        self.lootValue = self.maxHp + self.atk + self.df
        self.xpValue = self.lootValue/2
        self.hostile = false
        self.inv = []
        self.coords = Coords(xSpawn, ySpawn)
        self.forwardCoords = Coords(self.coords.x + bits, self.coords.y)
        self.unchangedSpritePaths = spritePaths
        self.spritePaths = spritePaths
        self.sprite = BeingSprite(self.spritePaths[1], self)
        self.weapon = Weapon(weapName)
        self.wallet = 0
        self.facing = directionList["down"]
        self.isMoving = false
        self.talkingLines = ["Hello!",
                             "Yes?",
                             "Can I Help you?"]
        self.bloodySprites = []
        self.lightSprites = []
        self.darkSprites = []
        self.inv.append(self.weapon)
        if itemList != None:
            self.inv += itemList
        currentBeingList.append(self)



        # use this moveTo when moving beings around

    def moveTo(self, x, y):
        self.sprite.moveTo(x, y)
        self.coords.x = x
        self.coords.y = y

    def activateTarget(self):
      self.getFrontTarget().activate()


        # Updates wallet by amount

    def changeWallet(self, amount):
        self.wallet += amount
        if self.wallet <= 0:
            self.wallet == 0
            




            
        # Adds item to inventory list

    def inventoryAdd(self, item):
        self.inv.append(item)


    def inventoryRemove(self, item):
        self.inv.Remove(item)



        # returns the Being's level

    def getLevel(self):
        return self.level






        # level-up logic. Semi-randomly increases max HP, Atk, df
        
    def levelUp(self):
        self.xp = 0
        self.level += 1
        self.changeMaxHP(random.randint(0, 8))
        self.changeAtk(random.randint(0, 4))
        self.changeDf(random.randint(0, 4))
        self.hp = self.maxHp

    



        # returns the Being's name

    def getName(self):
        return self.name
    




        
        # returns the Being's current hp

    def getCurrentHP(self):
        return int(self.hp)





        
        # returns the Being's max hp

    def getMaxHP(self):
        return int(self.maxHp)
    




        
        # returns the Being's current xp

    def getXp(self):
        return int(self.xp)
    




           
        # returns the Being's ATK

    def getAtk(self):
        return int(self.atk)
    




           
        # returns the Being's DF

    def getDf(self):
        return int(self.df)





             
        # increases xp by the amount given.
        # negative amounts will reduce xp
        # contains built in "barrier" formula
        # for levelling up

    def changeXp(self, amount):
        for i in range(1, amount):
            self.xp +=1
            if self.xp>=(self.level**1.2)*1.5:
                self.levelUp()
    

                               


                
        # changes ATK by the amount given

    def changeAtk(self, amount):
        self.atk += amount
    

               


        
        # changes DF by the amount given


    def changeDf(self, amount):
        self.df += amount


               


        
        # changes max HP by the amount given

    def changeMaxHP(self, amount):
        self.maxHp += amount


               



        # changes current HP by amount given.
        # negative values reduce.
        # if hp falls below 0, calls dead()
        
    def changeHp(self, amount):
        self.hp = int(self.hp + amount)
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        elif self.hp <= 0:
            self.dead()
        else:
            self.bloodify()






# Basic enemy AI. Enemy moves in a random direction and attacks if 
# the player is directly in front.

    def simpleHostileAI(self):
        distanceX = self.coords.x - bot1.coords.x
        distanceY = self.coords.y - bot1.coords.y
        closeProximity = BITS * 3
        if self.forwardCoords.x == bot1.coords.x and self.forwardCoords.y == bot1.coords.y:
            self.meleeAtk()
        elif self.coords.x-BITS == bot1.coords.x and self.coords.y == bot1.coords.y:
            self.faceLeft()
            self.meleeAtk()
        elif self.coords.x+BITS == bot1.coords.x and self.coords.y == bot1.coords.y:
            self.faceRight()
            self.meleeAtk()
        elif self.coords.x == bot1.coords.x and self.coords.y+BITS == bot1.coords.y:
            self.faceDown()
            self.meleeAtk()
        elif self.coords.x == bot1.coords.x and self.coords.y-BITS == bot1.coords.y:
            self.faceUp()
            self.meleeAtk()
        elif abs(self.coords.x - bot1.coords.x) < BITS and abs(self.coords.y - bot1.coords.y) < bits:
            self.moveRandom()
        elif abs(self.coords.x - bot1.coords.x) <= closeProximity and abs(self.coords.y - bot1.coords.y) <= closeProximity:
            self.moveTowardsPlayer(distanceX, distanceY)
        else:
            self.moveRandom()






        # Moves towards bot1. Distances should be passed in form self.x - bot1.x, same for y

    def moveTowardsPlayer(self, distanceX, distanceY):
        if abs(distanceX) > abs(distanceY):
            if distanceX < 0:
                self.moveRight()
            else:
                self.moveLeft()
        else:
            if distanceY < 0:
                self.moveDown()
            else:
                self.moveUp()


# Moves a being in a random direction

    def moveRandom(self):
        randNum = random.randint(0, 3)
        if randNum == 0:
            self.moveUp()
        elif randNum == 1:
            self.moveDown()
        elif randNum == 2:
            self.moveLeft()
        else:
            self.moveRight()






                                  
        # returns a random item from the inv list

    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]
            






        # drops all contents of the inv list in a lootbag object

    def dropLoot(self):
        loot = Lootbag(self.inv, self.coords)
        objectList.append(loot)






        # Actions to be taken on hp <= 0

    def dead(self):
        
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        currentBeingList.remove(self)
        del self
        dead = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
        music.Play(dead)

        # Handles lighting of sprites. If a valid light object is within the range
        # currently set to BITS * 3, a new set of sprites will be created and applied
        # to simulate lighting.
        # Starts a new thread.

    def lightenDarken(self):
        bright = self.lightWithinRange(BITS * 3)
        if self.spritePaths != self.lightSprites and bright:
            self.lightenPixels()
        elif self.spritePaths == self.lightSprites and not bright:
            self.resumePixels()
            deletePath = path + "RobotSprites"
            deleteKey = self.name + str(currentBeingList.index(self)) + "lightSprite"
            x = None
            thread.start_new_thread(self.threadDeleteLightSprites, (x,))




        # Helper for lightenDarken(). Separated to allow for early returns. Determins if
        # a valid light source is within the range passed

    def lightWithinRange(self, range):
        for light in lightSources:
            distanceX = abs(self.coords.x - light.coords.x)
            distanceY = abs(self.coords.y - light.coords.y)
            if distanceX <= range and distanceY <= range and light.isOn:
                return true  
        return false


    def threadDeleteLightSprites(self, x):
        for sprite in self.lightSprites:
            os.remove(sprite)
        self.lightSprites = []

    def resumePixels(self):
        self.spritePaths = self.darkSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[self.facing], self)
        self.sprite.spawnSprite()


    def lightenPixels(self):
        self.darkSprites = self.spritePaths
        spriteNum = 0
        for sprites in range(0, len(self.spritePaths)):
            pic = makePicture(self.spritePaths[sprites])
            for x in range(0, getWidth(pic)-1):
                for y in range(0, getHeight(pic)-1):
                    p = getPixel(pic, x, y)
                    color = getColor(p)
                    if color != makeColor(0, 0, 0):
                        setColor(p, makeColor(getRed(p)*1.5, getGreen(p)*1.5, getBlue(p)*1.5))
            newPicPath = path + "RobotSprites/" + self.name + str(currentBeingList.index(self)) + "lightSprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.lightSprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.lightSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.lightSprites[self.facing], self)
        self.sprite.spawnSprite()
        

    def bloodify(self):
        spriteNum = 0
        
        self.bloodySprites = []
        for sprites in range(0, len(self.spritePaths)):
            pic = makePicture(self.spritePaths[sprites])
            for x in range(0, getWidth(pic)-1):
                for y in range(0, getHeight(pic)-1):
                    p = getPixel(pic, x, y)
                    if getColor(p) != makeColor(0, 0, 0):
                        if random.randint(0, 100) > (self.hp*100)/self.maxHp:
                            setColor(p, makeColor(114, 87, 7))
            newPicPath = path + "RobotSprites/" + self.name + str(currentBeingList.index(self)) + "bloodySprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.bloodySprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.bloodySprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.bloodySprites[self.facing], self)
        self.sprite.spawnSprite()
  




        # For use with actions that can target more than one target (e.g., attacks)

    def getFrontTargetList(self):
        bigList = currentBeingList + objectList
        targetList = []
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                targetList.append(target)
        return targetList
        






        #for use with actions that can only target one target (e.g., talking)

    def getFrontTarget(self):
        bigList = currentBeingList + objectList
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                return target

            


            
        #needs to be reworked for better decomp
        #
        # activates the melee attack action.
        # displays the weapon at the being's forward coord
        # and activates a damage calculation if any being is there
        # Friendly fire is enabled. Attacking a friendly turns them hostile
        # if the target is killed, exp is calculated.  If the player is killed,
        # the player loses all levels/items and respawns as a new instance of the
        # User class.

    def meleeAtk(self):
        self.displayWeapon()
        x = 1
        thread.start_new_thread(threadRemoveSprite, (.2, self.weapon.sprite))
        self.weapon.displayed = false
        for target in self.getFrontTargetList():
            if isinstance(target, LightSource):
              if target.isBurnable and target.isOn and self.weapon.isBurnable:
                self.weapon.burn()
              elif target.isBurnable and not target.isOn and self.weapon.onFire:
                target.turnOn()
            elif isinstance(target, Being) or isinstance(target, Enemy):    
              damage = self.atk
              if target != bot1:
                target.hostile = true
              if damage <= 0:
                damage = 1
              target.changeHp(damage*(-1))
              target.displayDamage()
              if target.hp <= 0:
                self.changeXp(target.xpValue)

                    
            



                    
        # Display's the "damage splash" sprite at
        # the given location. Uses multithreading.

    def displayDamage(self):
        damage = Sprite(path + r"EffectSprites/damage.gif", self)
        display.add(damage, self.coords.x, self.coords.y)
        thread.start_new_thread(threadRemoveSprite, (.25, damage))

        




        # For use with meleeAtk and thread.start_new_thread().
        # may be removed and have functionality replaced by 
        # more general function

    def threadHideWeapon(self, x):
            time.sleep(.2)
            self.weapon.hide()






        # displays the being's weapon at the being's forward coords
        # note that the weapon sprite is not despawned

    def displayWeapon(self):
        if self.facing == directionList["up"]:
            self.weapon.displayUp(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == directionList["down"]:
            self.weapon.displayDown(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == directionList["left"]:
            self.weapon.displayLeft(self.forwardCoords.x, self.forwardCoords.y)
        else:  #right
            self.weapon.displayRight(self.forwardCoords.x, self.forwardCoords.y)


    
    def pickUpLoot(self, coords):
        for item in objectList:
            if item.type == "lootbag" and item.coords.x == coords.x and item.coords.y == coords.y:
                self.inv += item.contents
                item.removeSprite()
                objectList.remove(item)
                del item



                    # MOVEMENT CLUSTER                                                    
        # Moves the being up/down/left/right one unit in two steps.
        # the first step is instant/halfstep, the second
        # is through a delayed call to thread moveDirection
        # in order to give the illusion of animation.
        # faceDirection is called first 
        # threadMoveDirection is not meant to be called directly.
        # pickUpLoot() is called in the threadMovefunctions
        # 
        # may be streamlined by using a single moveForward function
        # that interacts with direction facing

    

 
    def moveUp(self):
        self.faceUp()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y >= 0 and currentMap.isTraversable(targetSpot):
            self.coords.y -= bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[0], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveUp, (x,))
            if self.facing == directionList["up"]: 
              self.forwardCoords.y = self.coords.y - BITS - bits/2
              self.forwardCoords.x = self.coords.x
              move = music(path+"Audio/footstep.wav")
              music.volume(move, .08)
              music.Play(move)


        else:
            self.isMoving = false
            move = music(path+"Audio/footstep.wav")
            music.Stop(move)
                           
    def threadMoveUp(self, x):
        time.sleep(.15)
        self.coords.y -= bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[0], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        

    def moveDown(self):
        self.faceDown()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y < backHeight and currentMap.isTraversable(targetSpot):
            self.coords.y += bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[1], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveDown, (x,))
            self.sprite.moveTo(self.coords.x, self.coords.y)
            if self.facing == directionList["down"]:
              self.forwardCoords.y = self.coords.y + BITS + bits/2
              self.forwardCoords.x = self.coords.x
              move = music(path+"Audio/footstep.wav")
              music.volume(move, .08)
              music.Play(move)
        else:
            self.isMoving = false
            move = music(path+"Audio/footstep.wav")
            music.Stop(move)
                   
    def threadMoveDown(self, x):
        time.sleep(.15)
        self.coords.y += bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[1], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()


    def moveLeft(self):
        self.faceLeft()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x >= 0 and currentMap.isTraversable(targetSpot):
            self.coords.x -= bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[4], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveLeft, (x,))
            if self.facing == directionList["left"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x - BITS - bits/2 
              move = music(path+"Audio/footstep.wav")
              music.volume(move, .08)
              music.Play(move)
        else:
            self.isMoving = false
            move = music(path+"Audio/footstep.wav")
            music.Stop(move)
            
    def threadMoveLeft(self, x):
        time.sleep(.15)
        self.coords.x -= bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[2], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()

    def moveRight(self):
        self.faceRight()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x < backWidth and currentMap.isTraversable(targetSpot):
            self.coords.x += bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[5], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveRight, (x,))
            if self.facing == directionList["right"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x + bits+ bits/2
              move = music(path+"Audio/footstep.wav")
              music.volume(move, .08)
              music.Play(move)
        else:
            self.isMoving = false
            move = music(path+"Audio/footstep.wav")
            music.Stop(move)


    def threadMoveRight(self, x):
        time.sleep(.1)
        self.coords.x += bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[3], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()


        # changes the being's sprite to one facing the corresponding
        # direction. If a weapon is displayed, it is first hidden.
        # adjusts forwardCoords accordingly

    def faceUp(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["up"]:
          self.facing = directionList["up"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[0], self)
          self.sprite.spawnSprite()
          self.forwardCoords.y = self.coords.y - bits
          self.forwardCoords.x = self.coords.x
                           
    def faceDown(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["down"]:
          self.facing = directionList["down"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[1], self)
          self.sprite.spawnSprite()
          self.forwardCoords.y = self.coords.y + bits
          self.forwardCoords.x = self.coords.x
                   
    def faceLeft(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["left"]:
          self.facing = directionList["left"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[2], self)
          self.sprite.spawnSprite()
          self.forwardCoords.x = self.coords.x - bits
          self.forwardCoords.y = self.coords.y
                   
    def faceRight(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["right"]:
          self.facing = directionList["right"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[3], self)
          self.sprite.spawnSprite()
          self.forwardCoords.x = self.coords.x + bits
          self.forwardCoords.y = self.coords.y







class Friendly(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [Sprite(path + r"RobotSprites/friendlyBigGib1.gif", self),
                              Sprite(path + r"RobotSprites/friendlyBigGib2.gif", self),
                              Sprite(path + r"RobotSprites/friendlyHead.gif", self),
                              ]

    def gibSpawn(self, gibSprite, x, y):
        gibList.append(gibSprite)
        display.add(gibSprite, x, y)

    def giblets(self):
        x = random.randint(self.coords.x - bits, self.coords.x + BITS)
        y = random.randint(self.coords.y - bits, self.coords.y + BITS)
        if isTraversable(x, y):
          animatedGib = AnimatedGiblets(path + r"RobotSprites/friendlyBigGib1.gif", path + r"RobotSprites/friendlyBigGib2.gif", x, y)
          animatedGib.animate()
        possibilities = random.randint(0, 3)
        if possibilities == 3:
          for i in range(0, random.randint(0, len(self.gibSpriteList))):
            x = random.randint(self.coords.x - bits, self.coords.x + BITS)
            y = random.randint(self.coords.y - bits, self.coords.y + BITS)
            if isTraversable(x, y):
              self.gibSpawn(self.gibSpriteList[3], x, y)

        # Actions to be taken on hp <= 0

    def dead(self):
        self.giblets()
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        currentBeingList.remove(self)
        del self
        dead = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
        music.Play(dead)
        

class ShopKeeper(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [Sprite(path + r"RobotSprites/shopKeeperGib1.gif", self),
                              Sprite(path + r"RobotSprites/shopKeeperGib2.gif", self)
                              ]








    def giblets(self):
        x = random.randint(self.coords.x - bits, self.coords.x + BITS)
        y = random.randint(self.coords.y - bits, self.coords.y + BITS)
        if isTraversable(x, y):
          animatedGib = AnimatedGiblets(path + r"RobotSprites/shopKeeperGib1.gif", path + r"RobotSprites/shopKeeperGib2.gif", x, y)
          animatedGib.animate()



    def dead(self):
        #play animation
        #delete coordinate data from grid
        self.giblets()
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        currentBeingList.remove(self)
        del self
        dead = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
        music.Play(dead)
        music.Stop(dead)







    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the currentBeingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   species:        - Being's species as a string
    #   level:          - Being's starting level

class Enemy(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, species, level):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        self.species = species 
        for val in range(0, level):
            self.levelUp()
        self.gibSpriteList = [Sprite(path + r"RobotSprites/enemyArmGib.gif", self),
                              Sprite(path + r"RobotSprites/enemyLegGib.gif", self),
                              Sprite(path + r"RobotSprites/enemyLegGib2.gif", self),
                              Sprite(path + r"RobotSprites/enemyBodyGib.gif", self),
                              Sprite(path + r"RobotSprites/enemyHeadGib.gif", self),
                              ]
        self.hostile = true
        





        
        # in progress loot-dropping function

    def dropLoot(self):
        items = []
        items.append(self.randomInvItem())
        loot = Lootbag(items, self.coords)
        objectList.append(loot)





    def gibSpawn(self, gibSprite, x, y):
        gibList.append(gibSprite)
        display.add(gibSprite, x, y)



    def giblets(self):
        gibIndex = 0
        for i in range(0, random.randint(0, len(self.gibSpriteList))):
            x = random.randint(self.coords.x - bits, self.coords.x + BITS)
            y = random.randint(self.coords.y - bits, self.coords.y + BITS)
            if isTraversable(x, y):
                self.gibSpawn(self.gibSpriteList[gibIndex], x, y)
                print(gibIndex)
                gibIndex += 1



        # in progress hp == 0 action

    def dead(self):
        #play animation
        #delete coordinate data from grid
        self.giblets()
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
          os.remove(files)
        currentBeingList.remove(self)
        del self
        dead= music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
        music.Play(dead)
        music.Stop(dead)




               
        # returns a random item from the inv list

    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]
            



        






        
        # Class for armor/equipment, in development

class Armor():
    def __init__(self, name):
        self.armorType = "FIX THIS CLASS"






# used for sprite animation, flickering between two sprites at random
# used for twitching/sparking/flames


class AnimatedGiblets():
    def __init__(self, filename1, filename2, x, y):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, self),
                           Sprite(filename2, self)]
        self.sprite = self.spriteList[0]
        gibList.append(self.spriteList[0])
        gibList.append(self.spriteList[1])




        #activates animation

    def animate(self):
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))






        # sprite addition and removal to and from display

    def spawnSprite(self):
        display.place(self.sprite, self.coords.x, self.coords.y, 5)
    def removeSprite(self):
        display.remove(self.sprite)


    def threadAnimate(self, container):
        while self.spriteList[0] in gibList or self.spriteList[1] in gibList:
            time.sleep(random.randint(0, 2)/10.0)
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in animatedSpriteList:
            self.removeSprite()
            del self
                     
            











# used for sprite animation, flickering between two sprites at random
# used for twitching/sparking/flames


class StationaryAnimatedSprite():
    def __init__(self, filename1, filename2, x, y, layer = 3):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, self, layer),
                           Sprite(filename2, self, layer)]
        self.sprite = self.spriteList[0]
        animatedSpriteList.append(self)
        self.coords = Coords(x, y)
        self.sprite.layer = layer




    def animate(self):
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))

    def spawnSprite(self):
        self.sprite.spawnSprite()
    def removeSprite(self):
        display.remove(self.sprite)


    def threadAnimate(self, container):
        while self in animatedSpriteList:
            time.sleep(random.randint(0, 2)/10.0)
            placeHolderSprite = self.spriteList[0]
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in animatedSpriteList:
            self.removeSprite()
            del self










    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the currentBeingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   species:        - Being's species as a string
    #   level:          - Being's starting level

class User(Being):
    def __init__(self, name, weapName, spritePaths, currentArea):
        Being.__init__(self, name, weapName, spritePaths, currentArea.spawnCoords.x, currentArea.spawnCoords.y)
        self.name = name
        self.helm = "Hair"
        self.chest = "BDaySuit"
        self.legs = "Shame"
        self.boots = "Toes"
        self.gloves = "Digits"
        self.area = currentArea

        self.sprite.spawnSprite()





    def giblets():
        None


               # EQUIPMENT CLUSTER
        # The following 6 functions handle equipping items
        # to  specific parts of the body.  Atk and Df stats
        # are adjusted accordingly.  The equipped item must
        # correlate to one of the itemLists

    def setWeapon(self, weapon):
        if self.weapon != "Stick":
            inventoryAdd(self.weapon)
        self.atk -= weaponStatsList[self.weapon]
        self.weapon = weapon
        self.atk += weaponStatsList[self.weapon]
               

    def setHelm(self, helm):
        if self.helm != "Hair":
            inventoryAdd(self.helm)
        self.df -= helmStatsList(self.helm)
        self.helm = helm
        self.df += helmStatsList(self.helm)


    def setChest(self, chest):
        if self.chest != "BDaySuit":
            inventoryAdd(self.chest)
        self.df -= chestStatsList(self.chest)
        self.chest = chest
        self.df += chestStatsList(self.chest)
               

    def setLegs(self, legs):
        if self.legs != "Shame":
            inventoryAdd(self.legs)
        self.df -= legsStatsList(self.legs)
        self.legs = legs
        self.df += legsStatsList(self.legs)
                 
        
    def setBoots(self, boots):
        if self.boots != "Toes":
            inventoryAdd(self.boots)
        self.df -= bootsStatsList(self.boots)
        self.boots = boots
        self.df += bootsStatsList(self.boots)
        

    def setGloves(self, gloves):
        if self.gloves != "Digits":
            inventoryAdd(self.gloves)
        self.df -= glovesStatsList(self.gloves)
        self.gloves = gloves
        self.df += glovesStatsList(self.gloves)
    




                     
        # equips a given item by calling one of the 
        # equipment "set" functions
        # item should be passed as it's key as it appears
        # in the item lists

    def equip(self, item):
        if indexName == weaponStatsList:
            if item in weaponStatsList:
                self.setWeapon(item)
        elif indexName == helmStatsList:
            if item in helmStatsList:
                self.setHelm(item)
        elif indexName == legsStatsList:
            if item in legsStatsList:
                self.setLegs(item)
        elif indexName == chestStatsList:
            if item in chestStatsList:
                self.setChest(item)
        elif indexName == glovesStatsList:
            if item in glovesStatsList:
                self.setGloves(item)
        elif indexName == bootsStatsList:
            if item in bootsStatsList:
                self.setBoots(item)
         





            # action - attempts to steal an item from a target
            # Being.  If the attempt fails, the Being turns hostile

    def steal(self, target):
        possibilities = len(target.inv)
        if possibilities>0:
            if random.randint(0, 10)%10 == 0:
                item = target.randomInvItem()
                target.inv.remove(item)
                self.inv.append(item)
                label = gui.Label("You stole "  + item.name)
                showLabel(label)
            else:
                label = gui.Label("You messed up now!")
                showLabel(label)
                target.hostile = true
            delayRemoveObject(label, 2)

    def talk(self):
        target = self.getFrontTarget()
        speech = gui.Label(target.talkingLines[random.randint(0, len(target.talkingLines)-1)])
        showLabel(speech)
        delayRemoveObject(speech, 2)

    def dead(self):
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        currentBeingList.remove(self)
        self.__init__("bot1", "Stick", userSpritePaths, self.area)
        weapon_sound = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
        music.Play(weapon_sound)



class music:
  
    def __init__(self, music_file):
      self.sound = makeSound(music_file)

    def Play(self):
      play(self.sound)
    
    
    def Stop(self):
      stopPlaying(self.sound)
     
         
    def volume(self, n):
      for sample in getSamples(self.sound):
        value = getSampleValue(sample)
        setSampleValue(sample, value*n)
 
         
    def repeat(self):
      while true:
        play(self.sound)
        stopPlaying(self.sound)
        time.sleep(20)
      return
      

            ######################
            #                    #
            #    PSEUDO-MAIN     #
            #                    #
            ######################



#initailize background image
backWidth = BITS * WIDTHTILES
backHeight = BITS * HEIGHTTILES

tilesPath = path + "Tiles/LPC/tiles/"
#Old, probably dont need textureMap anymore
textureMap = makePicture(path + "Tiles/hyptosis_tile-art-batch-1.png")

#initailize textures
#  Tile(isTraversable, isPassable, isTough, desc)
#add Dirt
dirt = Tile(true, true, false, "dirt")
#add Grass
grass = Tile(true, true, false, "grass")
#add Stone
stone = Tile(true, true, false, "stone")
#add lavaRock
lavaRock = Tile(true, true, false, "lavaRock")
#add Water
water = Tile(false, true, false, "water")
#add Lava
lava = Tile(false, true, false, "lava")
#add Fence
fence = Tile(false, true, false, "fence")
#add Door tile
door = Tile(true, false, false, "door")
#add Blank
blank = Tile(false, false, false, "Filler for structure class")

#structures
structPath = path + "Tiles/LPC/structures/"
house = makePicture(structPath + "house.png")
tree1 = makePicture(structPath + "tree1.png")

#get width and height
texWidth = getWidth(textureMap)
texHeight = getHeight(textureMap)


paths = ["d", "s", "h", ".", "o"]
#create empty grass field will clean up later
home  = "fffffffffffffddddfffffffffffffff"
home += "fh......ggt,,ddddgh......ggggggf"
home += "f.......gg,,,ddddg.......dgggggf"
home += "f.......gg,,,ddddg.......ddggggf"
home += "f..o....gggggddddg..o....ddggggf"
home += "f..o....gggggddddg..o....ddggggf"
home += "fgsssssssddddddddddddddddddggggf"
home += "fgsssssssddddddddddddddddddggddd"
home += "fgggsssssggggddddddddddddddddddd"
home += "fgggddssgggggddddddddddddddddddf"
home += "fgggdddggggwwwwddddddh......gggf"
home += "fgggdddgggwwwwwwddddd.......gggf"
home += "fgggdddwwwwwwwwwwwwdd.......gggf"
home += "fgggdddwwwwwwwwwwwwdd..o....t,,f"
home += "fgdddddwwwwwwwwwwwddd..o....,,,f"
home += "fgdddddddwwwwwwwdddddddddddd,,,f"
home += "fggddddddgggggggddddddddddddgdgf"
home += "ffffffffffffffffffffffffffffffff"
town = makePicture(path + "newBack.png")
townMap = Map(home, town)
townSpawn = Coords(13*bits, 1*BITS)
currentMap = townMap

field  = "ffffffffffffffffffffffffffffffff"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggwwwwwwwgggf"
field += "fggggggggggggggggggggwwwwwwwwwgf"
field += "fggggggggggggggggggggwwwwwwwwwgf"
field += "fgggggggggggggggggggggggggwwwwgf"
field += "fggggggggggggggggggggggggwwwwwgf"
field += "ggggggggggggggggggggggggwwwwwwgf"
field += "ggggggggggggggggggggggggwwwwwggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fffffffffffffggggfffffffffffffff"
fieldImg = makePicture(path + "fieldMap.png")
fieldSpawn = Coords(1*bits, 8*BITS)
fieldMap = Map(field, fieldImg)

dungeon  = "ffffffffffffffffffffffffffffffff"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllLLLLllllllllllllllllllf"
dungeon += "fllllllllLLLLLLLLllllllllllllllf"
dungeon += "fllllllllLLLLLLLLLLLlllllllllllf"
dungeon += "lllllllllLLLLLLLLLLLlllllllllllf"
dungeon += "lllllllllLLLLLLLLLLLlllllllllllf"
dungeon += "flllllllllllLLLLLLLLlllllllllllf"
dungeon += "flllllllllllLLLLlllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fffffffffffffllllfffffffffffffff"
dungeonImg = makePicture(path + "dungeonMap.png")
dungeonMap = Map(dungeon, dungeonImg)
dungeonSpawn = Coords(15*bits, 16*BITS)

layer0 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 0)
layer1 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 1)
layer2 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 2)
layer3 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 3)
layer4 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 4)
layer5 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 5)
layer6 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 6)
loading = RawSprite(path + "Fullscreens/LogoOmega.png", 0, 0, 0)

display = gui.Display("Robot Saga", backWidth, backHeight)


setUpLayers()


TOWNAREA = Area(None, townMap, townSpawn)
townSprite = RawSprite(path + "newBack.png", 0, 0, 6)
TOWNAREA.mapSprite = townSprite
FIELDAREA = Area(None, fieldMap, fieldSpawn)
fieldSprite = RawSprite(path + "fieldMap.png", 0, 0, 6)
FIELDAREA.mapSprite = fieldSprite
DUNGEONAREA = Area(None, dungeonMap, dungeonSpawn)
dungeonSprite = RawSprite(path + "dungeonMap.png", 0, 0, 6)
DUNGEONAREA.mapSprite = dungeonSprite

currentArea = TOWNAREA
currentBg = TOWNAREA.mapSprite
currentBg.spawnSprite()
currentBeingList = TOWNAREA.beingList
objectList = TOWNAREA.objectList
gibList = TOWNAREA.gibList
animatedSpriteList = TOWNAREA.animatedSpriteList
lightSources = TOWNAREA.lightSources
#loadIntro()  - Intro credits for production build. see loadIntro() definition for details



# Currently acts as the "controller" to read inputs
text = gui.TextField("", 1) 

# text.onKeyType(function) sets the function to be called on character entry.  Default is keyAction()
# setting "function" to a different function will alter controls. Make sure to pass a function
# that takes exactly one parameter.  onKeyType will pass the character of the typed key as an argument,
# so for example:
# 
# def randomFunction(key) 
#   if key == "h":
#       doSomething
# 
# text.onKeyType(randomFunction) 
#
# would activate doSomething if "h" was pressed.
text.onKeyType(keyAction) 


display.add(text)

#display.drawImage(path + "newBack.png", 0, 0)
bot1Spawn = Coords(13*bits, 1*BITS)
bot1 = User("bot1", "Stick", userSpritePaths, TOWNAREA)
bot1.area = currentArea
shopKeeper = ShopKeeper("shopKeep", "Stick", shopKeeperSpritePaths, 3*bits, 6*BITS)
light = LightSource(bigTorchSpritePaths, 416, 288, 1)
light2 = LightSource(bigTorchSpritePaths, 384, 288, 1)
shopKeeper.sprite.spawnSprite()
friendlyOrange = Friendly("orange", "Stick", friendlyOrangeSpritePaths, 8*bits, 10*BITS)
friendlyGreen = Friendly("green", "Stick", friendlyGreenSpritePaths, 10*bits, 10*BITS)
friendlyOrange.sprite.spawnSprite()
friendlyGreen.sprite.spawnSprite()

#background music
#background_music1 = music(path+"Audio/Still-of-Night_Looping.wav")
#music.repeat(background_music1)
#music.Stop(background_music1)
testCoords = Coords(0, 0)
currentBeingList.append(friendlyOrange)
