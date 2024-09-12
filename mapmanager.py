import pickle
from panda3d.core import DirectionalLight, AmbientLight


i = 0
sky_color = 0
class MapManager():
    list_blocks = ["grass-block.glb", 'dirt-block.glb', 'sand-block.glb', 'stone-block.glb']
    def __init__(self):
        self.model = self.list_blocks[0]
        self.texture = "block.png"
        self.colors = [(0.2,0.2,0.35,1),
                        (0.5,0.3,0.0,1),
                        (0.2,0.2,0.3,1),
                        (0.5,0.5,0.2,1),
                        (0.0,0.6,0.0,1)]
        self.startNew()
        self.setupLights()
        #self.addBlock((0,10,0))
    def startNew(self):
        self.land = render.attachNewNode("Land")
    def addBlock(self,position):
        self.block = loader.loadModel(self.model)
        #self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(position[2])
        #self.block.setColor(self.color)
        self.block.setTag("at",str(position))
        self.block.reparentTo(self.land)

    def loadLand(self,path):
        self.clear()
        with open(path) as file:
            y = 0
            for string in file:
                x = 0
                new_string = string.split()
                for z in new_string:
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x,y,z0))
                    x += 1
                y += 1
    def clear(self):
        self.land.removeNode()
        self.startNew()

    def getColor(self,z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]
        
    def isEmpty(self,pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
        
    def findBlocks(self,pos):
        return self.land.findAllMatches("=at=" + str(pos))
    
    def findHighestEmpty(self,pos):
        x,y,z = pos
        z = 1
        while not self.isEmpty((x,y,z)):
            z += 1
        return (x,y,z)
    
    def delBlock(self,position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def buildBlock(self,pos):
        x,y,z = pos
        new = self.findHighestEmpty((x,y,z))
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlockFrom(self,position):
        x,y,z = self.findHighestEmpty(position)
        pos = x,y,z, - 1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def saveMap(self):
        print("Сохранил")
        blocks = self.land.getChildren()
        with open("map.dat","wb") as file:
            pickle.dump(len(blocks),file)
            for block in blocks:
                x,y,z = block.getPos()
                x,y,z = int(x),int(y),int(z)
                xyz = (x,y,z)
                pickle.dump(xyz,file)

    def loadMap(self):
        print("Загрузил")
        self.clear()
        with open("map.dat","rb") as file:
            amount = pickle.load(file)
            for i in range(amount):
                coords = pickle.load(file)
                self.addBlock(coords)

    def changeBlocks(self):
        global i
        #todo blocks = ["block.png","brick.png","stone.png","wood.png"]
        if i < len(self.list_blocks) - 1:
            print("Поменял текстуру")
            i += 1
            print(i)
            self.model = self.list_blocks[i]
        elif i >= len(self.list_blocks) - 1:
            i = 0
            self.model = self.list_blocks[0]

    def changeModel(self, position):
        blocks = ["block.png","brick.png","stone.png","wood.png"]
        global i
        if i < len(blocks) - 1:
            print("Поменял текстуру")
            i += 1
            print(i)
            self.texture = blocks[i]
        elif i >= len(blocks) - 1:
            i = 0
            self.texture = blocks[0]
        self.block = loader.loadModel(self.texture)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(position[2])
        self.block.setColor(self.color)
        self.block.setTag("at",str(position))
        self.block.reparentTo(self.land)

    def changeBackground(self):
        global sky_color
        if sky_color == 0:
            base.setBackgroundColor(0.2, 0.4, 1)
            sky_color += 1
        elif sky_color == 1:
            base.setBackgroundColor(0.8, 0.8, 0.8)
            sky_color = 0

    def setupLights(self):
        mainLight = DirectionalLight('main light')
        mainLightNodePath = render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(60, -60, 0)
        render.setLight(mainLightNodePath)

        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNodePath)
    


    


