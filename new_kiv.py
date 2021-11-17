from kivymd.app import MDApp
from kivy.lang import Builder

from modes.live import runLive
from modes.instant import runInstant





class Test(MDApp):
    
    instantImagePath = ""
    
    def runLive(self, alg) :
        runLive(alg)

    def runInstant(self, args) :
        runInstant(args)
    
    def select_image(self, file) :
        self.instantImagePath = file[0]

    def build(self):
        self.title = "Face Detection Algorithms"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        return Builder.load_file('new_kiv.kv')
            


Test().run()


