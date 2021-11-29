from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

from modes.live import runLive
from modes.instant import runInstant
from modes.offline import runOffline

class Test(MDApp):
    offlineRuntimeResult = StringProperty("0")
    offlineFacesDetectedResult = StringProperty("0")
    instantImagePath = ""
    
    def runLive(self, alg) :
        runLive(alg)

    def runInstant(self, args) :
        runInstant(args)
    
    def runOffline(self, args):
        runOffline(self, args)
    
    def select_image(self, file) :
        try: 
            # self.instantImagePath = file[0]
            self.root.ids.my_image.source = file[0] # Try clause since if they click on a directory or any non-image, it won't error out
        except:
            pass
    
    def UpdateOfflineRuntimeResult(self, number):
        try:
            self.root.ids.offlineRunTime.text = "Run Time: " + str(number) + "ms"
        except:
            pass
    
    def UpdateOfflineFacesDetectedResult(self, number):
        try:
            self.root.ids.offlineFaceCounted.text = "Faces Detected: " + str(number)
        except:
            pass
    
    def UpdateOfflineAvgRuntimeResult(self, number):
        try:
            self.root.ids.offlineAvgRunTime.text = "Avg. Run Time: " + str(number) + "ms"
        except:
            pass
    
    def UpdateOfflineAvgFacesDetectedResult(self, number):
        try:
            self.root.ids.offlineAvgFaceCounted.text = "Avg. Faces Detected: " + str(number)
        except:
            pass
    
    def build(self):
        self.icon = "logo.png"
        self.title = "Faceify"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        return Builder.load_file('new_kiv.kv')
            


Test().run()


