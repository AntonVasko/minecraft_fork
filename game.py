from math import pi, sin, cos #! для вычислений, в том числе и для работы с мышью

#from panda3d.core import loadPrcFileData
from panda3d.core import loadPrcFile
from direct.tkpanels.Inspector import inspect
from direct.showbase.ShowBase import ShowBase
import mapmanager
import hero as hr

'''loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")
'''

loadPrcFile('settings.prc')

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        
        self.land = mapmanager.MapManager()
        try:
            self.land.loadLand("land.txt")
        except Exception as e:
            print("Произошла ошибка при загрузке карты " + str(e))
        self.hero = hr.Hero((1,1,2),self.land)   
       
        self.restartSound = base.loader.loadSfx('music.mp3') #! замена loadMusic на loadSfx
        self.restartSound.setLoop(True) #! играть постоянно
        #self.restartSound.play()

        #taskMgr.add(self.hero.update, 'update')

        base.camLens.setFov(80)
        
    
    

game = Game()
game.run()