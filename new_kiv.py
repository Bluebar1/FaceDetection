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
from PIL import Image


class Test(MDApp):    
    workingFolder = os.path.expanduser('~/Documents') + "\\Faceify"
    os.makedirs(workingFolder, exist_ok=True)
    instantImagePath = ""
    offlineFolder = ""

    def openLeTeXFolder(self) :
        os.makedirs(self.workingFolder + '\\results', exist_ok=True)

        path = os.path.realpath(self.workingFolder + '\\results')
        os.startfile(path)

    def openOfflineOutputFolder(self) :
        os.makedirs(self.workingFolder + config.offlineOutputPath, exist_ok=True)

        path = os.path.realpath(self.workingFolder + config.offlineOutputPath)
        os.startfile(path)
    
    def setOfflineFolder(self) :
        try: 
            self.offlineFolder = filechooser.choose_dir(title="Choose the source folder...")[0]
            self.root.ids.folder_path_label.text = "Chosen Folder: " + self.offlineFolder
            #print(instantImagePath + "\\test\\another\\directory\\")
        except:
            pass

    def runLive(self, alg) :
        runLive(alg,self.workingFolder)

    def runInstant(self, args) :
        if((args[0] != "") & (args[1] != "")):
            #print("Calling run instant")
            runInstant(self, [args[0], args[1], self.workingFolder])
    
    def runOffline(self, args):
        if((args[0] != "") & (args[1] != "") & (self.offlineFolder != "")):
            runOffline(self, [args[0], self.offlineFolder, args[1], args[2], self.workingFolder])

    def chooseImage(self) :
        try: 
            instantImagePath = filechooser.open_file(title="Pick an image file...", filters = [("Images", '*.png','*.jpg')])[0]
            self.root.ids.my_image.source = instantImagePath # Try clause since if they click on a directory or any non-image, it won't error out
            self.root.ids.InstantID.selectedImage = instantImagePath
            self.root.ids.instant_file_location_label.text = "Image Location: " + instantImagePath
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
        self.root.ids.instantOuputJSONFilePath.text = "Output Data Folder: " + self.workingFolder + config.instantDataLocation
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
        self.root.ids.saved_folder_path.outputLatexFilePath = self.workingFolder + config.offlineLatexLocation
    
    def build(self):
        self.icon = "logo.png"
        self.title = "Faceify"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        if hasattr(sys, '_MEIPASS'): # if it's in EXE form
            return Builder.load_file(sys._MEIPASS + '\\new_kiv.kv')
        
        return Builder.load_file('new_kiv.kv') # if you're just using python new_kiv.ky
if __name__ == "__main__":
    # these lines should be added
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    ###
    Test().run()



