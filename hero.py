from math import pi, sin, cos #! нужно импортировать для управления мышью
from panda3d.core import WindowProperties #! нужно импортировать для управления мышью
from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionRay, CollisionHandlerQueue #! нужно импортировать для управления мышью
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

#!Градусы в радианы
def degToRad(degrees):
    return degrees * (pi / 180.0)

class Hero:
    def __init__(self,pos,land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel("smiley")
        self.restartSound = loader.loadMusic('build.wav')
        self.hero.setColor(1,0.5,0)
        self.hero.setScale(0.5)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        render.setShaderAuto()
        self.cameraBind()
        self.accept_events()

        self.captureMouse() #! добавляем метод для управления мышью
        self.setupCamera() #! добавляем метод для управления мышью

        taskMgr.add(self.update, 'update') #! добавляем менеджер задач и передаём ему метод update как обрабтчик

    def update(self, task): #! обработчик для менеджера задач
        dt = globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed

        camera.setPos(
            camera.getX() + x_movement,
            camera.getY() + y_movement,
            camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = base.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            self.cameraSwingFactor = 10

            currentH = base.camera.getH()
            currentP = base.camera.getP()

            base.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

        return task.cont
        
    def cameraBind(self):

        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        #base.disableMouse()
        base.camera.setH(80)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,3)
        self.cameraOn = True

    def cameraUp(self):
        
        position = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-position[0],-position[1],-position[2] - 3)
        base.camera.reparentTo(render)
        #base.enableMouse()
        self.cameraOn = False

    def accept_events(self):
        base.accept('escape', self.releaseMouse)
        base.accept('w', self.updateKeyMap, ['forward', True])
        base.accept('w-up', self.updateKeyMap, ['forward', False])
        base.accept('a', self.updateKeyMap, ['left', True])
        base.accept('a-up', self.updateKeyMap, ['left', False])
        base.accept('s', self.updateKeyMap, ['backward', True])
        base.accept('s-up', self.updateKeyMap, ['backward', False])
        base.accept('d', self.updateKeyMap, ['right', True])
        base.accept('d-up', self.updateKeyMap, ['right', False])
        base.accept('space', self.updateKeyMap, ['up', True])
        base.accept('space-up', self.updateKeyMap, ['up', False])
        base.accept('lshift', self.updateKeyMap, ['down', True])
        base.accept('lshift-up', self.updateKeyMap, ['down', False])

        base.accept("c",self.changeView)

        base.accept("r",self.seeUp)
        base.accept("f",self.seeDown)

        base.accept("x" + "-repeat",self.turn_right)
        base.accept("z" + "-repeat",self.turn_left)

        base.accept("x",self.turn_right)
        base.accept("z",self.turn_left)

        base.accept("w" + "-repeat",self.forward)
        base.accept("a" + "-repeat",self.left)
        base.accept("s" + "-repeat",self.back)
        base.accept("d" + "-repeat",self.right)

        base.accept("w",self.forward)
        base.accept("a",self.left)
        base.accept("s",self.back)
        base.accept("d",self.right)

        base.accept("f" + "-repeat",self.seeDown)
        base.accept("r" + "-repeat",self.seeUp)

        '''base.accept("space",self.up)
        base.accept("space" + "-repeat",self.up)
        base.accept("shift",self.down)
        base.accept("shift" + "-repeat",self.down)'''

        base.accept("g",self.changeMode)
        base.accept("v",self.destroy)
        base.accept("b",self.build)
        base.accept("l",self.land.loadMap)
        base.accept("k",self.land.saveMap)
        base.accept("j",self.land.changeBlocks)
        base.accept("h",self.land.changeBackground)
        base.accept("y",self.land.changeModel)

        
    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)
    def just_move(self,angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    def try_move(self,angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0],pos[1],pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def move_to(self,angle):
        if self.mode:
            self.just_move(angle)
        elif self.mode == False:
            self.try_move(angle)

    def check_dir(self,angle):
        if angle >= 0 and angle <= 20:
            return 0,-1
        elif angle >= 0 and angle <= 65:
            return 1,-1
        elif angle >= 0 and angle <= 110:
            return 1,0
        elif angle >= 0 and angle <= 155:
            return 1,1
        elif angle >= 0 and angle <= 200:
            return 0,1
        elif angle >= 0 and angle <= 245:
            return -1,1
        elif angle >= 0 and angle <= 290:
            return -1,0
        elif angle >= 0 and angle <= 335:
            return -1,-1
        else:
            return 0,-1
    def look_at(self,angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())

        dx,dy = self.check_dir(angle)
        return from_x + dx, from_y + dy,from_z
    
    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)
    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        i = 0
        while i < 10:
            i += 1
            self.hero.setZ(self.hero.getZ() + 1)
        
    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)

    def seeDown(self):
        if self.hero.getP() % 360 < 90 or self.hero.getP() % 360 < 1 :
            self.hero.setP((self.hero.getP() + 5) % 360)
            print(self.hero.getP())

    def seeUp(self):
        if self.hero.getP() % 360 >= 0:
            self.hero.setP((self.hero.getP() - 5 ) % 360)
            

    def changeMode(self):
        if self.mode:
            self.mode = False
        elif self.mode == False:
            self.mode = True
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.restartSound.setVolume(1)
            self.restartSound.play()
            self.land.addBlock(pos)
        else:
            self.restartSound.setVolume(1)
            self.restartSound.play()
            self.land.buildBlock(pos)
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.restartSound = loader.loadMusic('destroy.wav')
            self.restartSound.setVolume(1)
            self.restartSound.play()
            self.land.delBlock(pos)
        else:
            self.restartSound = loader.loadMusic('destroy.wav')
            self.restartSound.setVolume(1)
            self.restartSound.play()
            self.land.delBlockFrom(pos)
    def captureMouse(self):
        self.cameraSwingActivated = True

        md = base.win.getPointer(0)
        self.lastMouseX = md.getX()
        self.lastMouseY = md.getY()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(properties)
        
    def releaseMouse(self):
        self.cameraSwingActivated = False

        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        base.win.requestProperties(properties)
    
    def setupCamera(self):
        base.disableMouse()
        base.camera.setPos(0, 0, 3)
        base.camLens.setFov(180)

        crosshairs = OnscreenImage(
            image = 'crosshairs.png',
            pos = (0, 0, 0),
            scale = 0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(base.camNode, (0, 0))
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = base.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value
