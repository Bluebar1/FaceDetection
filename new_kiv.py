from kivymd.app import MDApp
from kivy.lang import Builder


from modes.live import runLive
from modes.instant import runInstant
from modes.offline import runOffline

import os
import config

class Test(MDApp):    
    instantImagePath = ""
    
    def runLive(self, alg) :
        runLive(alg)

    def runInstant(self, args) :
        if((args[0] != "") & (args[1] != "")):
            runInstant(self, args)
    
    def runOffline(self, args):
        if((args[0] != "") & (args[1] != "")):
            runOffline(self, args)
    
    def select_image(self, file) :
        try: 
            # self.instantImagePath = file[0]
            self.root.ids.my_image.source = file[0] # Try clause since if they click on a directory or any non-image, it won't error out
            self.root.ids.InstantID.selectedImage = file[0]
        except:
            pass
    
    def updateInstantResults(self, runTime, facesDetected, resultPicture):
        self.root.ids.instantRunTime.text = "Run Time: " + str(runTime) + "ms"
        self.root.ids.instantFaceCounted.text = "Faces Detected: " + str(facesDetected)
        self.root.ids.instantOuputJSONFilePath.text = "Output Data Folder: " + os.path.dirname(os.path.abspath(config.instantDataLocation))
        self.root.ids.my_image.source = resultPicture
        self.root.ids.my_image.reload()
        
    def updateOfflineProgress(self, scanProgress, currentFileName):
        self.root.ids.offlineModeCurrentProgress.value = scanProgress
        self.root.ids.offlineModeCurrentFile.text = currentFileName
    
    def updateOfflineResults(self, runTime, avgRunTime, facesDetected, avgFacesDetected):
        self.root.ids.offlineRunTime.text = "Run Time: " + str(runTime) + "ms"
        self.root.ids.offlineAvgRunTime.text = "Avg. Run Time: " + str(avgRunTime) + "ms"
        self.root.ids.offlineFaceCounted.text = "Faces Detected: " + str(facesDetected)
        self.root.ids.offlineAvgFaceCounted.text = "Avg. Faces Detected: " + str(avgFacesDetected)
        self.root.ids.saved_folder_path.outputLatexFilePath = os.path.dirname(os.path.abspath(config.offlineLatexLocation))
    
    def build(self):
        self.icon = "logo.png"
        self.title = "Faceify"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        return Builder.load_file('new_kiv.kv')

Test().run()


