from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser

from modes.live import runLive
from modes.instant import runInstant
from modes.offline import runOffline

import os
import config
import os, sys
from kivy.resources import resource_add_path


class Test(MDApp):    
    workingFolder = ""
    instantImagePath = ""
    
    
    def runLive(self, alg) :
        runLive(alg)

    def runInstant(self, args) :
        if((args[0] != "") & (args[1] != "") & (args[2] != "")):
            #print("Calling run instant")
            runInstant(self, args)
    
    def runOffline(self, args):
        if((args[0] != "") & (args[1] != "")):
            runOffline(self, args)

    def setWorkingFolder(self) :
        try: 
            workingFolder = filechooser.choose_dir(title="Choose the output directory...")[0]
            self.root.ids.InstantID.outputFolder = workingFolder
            #print(instantImagePath + "\\test\\another\\directory\\")
        except:
            pass

    def chooseImage(self) :
        try: 
            instantImagePath = filechooser.open_file(title="Pick an image file...", filters = [("*.png","*.jpg")])[0]
            self.root.ids.my_image.source = instantImagePath # Try clause since if they click on a directory or any non-image, it won't error out
            self.root.ids.InstantID.selectedImage = instantImagePath
            #print(instantImagePath + "\\test\\another\\directory\\")
        except:
            pass
    
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
        self.root.ids.instantOuputJSONFilePath.text = "Output Data Folder: " + self.root.ids.InstantID.outputFolder + config.instantDataLocation
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
        if hasattr(sys, '_MEIPASS'):
            return Builder.load_file(sys._MEIPASS + '\\new_kiv.kv')
        
        return Builder.load_file('new_kiv.kv')
if __name__ == "__main__":
    # these lines should be added
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    ###
    Test().run()



