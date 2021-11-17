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
        try: 
            # self.instantImagePath = file[0]
            self.root.ids.my_image.source = file[0] # Try clause since if they click on a directory or any non-image, it won't error out
        except:
            pass

    def build(self):
        self.title = "Face Detection Algorithms"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        return Builder.load_file('new_kiv.kv')
            


Test().run()


