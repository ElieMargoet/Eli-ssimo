import nuke
import os
import sys
import math
import re
from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui


class mytool(QtWidgets.QWidget):
    def __init__(self):
        #define and load UI
        super(mytool,self).__init__()
        scriptpath = "C:/Users/Elie/.nuke/Elissimo.ui"
        self.ui = QtUiTools.QUiLoader().load(scriptpath, parentWidget=self)

        #fit UI in QBoxLayout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

        #Set window to stay on top of nuke and set its title
        label = self.setWindowTitle('Eli-ssimo') 

        self.ui.btn_publish.clicked.connect(self.getFileName)

        self.file = None
        self.first_frame = None
        self.last_frame = None
        self.artist_value = self.ui.lineE_artist.text()
        self.name_value = self.ui.lineE_name.text()

        global nodes_to_keep

        nodes_to_keep = nuke.allNodes()


    def getFileName(self):

        selectedNode = nuke.selectedNode()

        if selectedNode.Class() == 'Read':
            self.file = selectedNode["file"].value()
            self.first_frame = selectedNode["first"].value()
            self.last_frame = selectedNode["last"].value()
            self.createOverlayScript()
            
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le node selectionne n'est pas un read")

    def createOverlayScript(self):

        scriptpath = 'D:\\interface python\\PirateOverlay.nknc'

        nuke.nodePaste(scriptpath)

        version_value = self.ui.spinB_version.value()

        read_node = nuke.toNode("read_exr")
        artist = nuke.toNode("artist")
        name = nuke.toNode("shot_name")
        version = nuke.toNode("version")
        write = nuke.toNode("Write_mov")

        if read_node:
            read_node["file"].setValue(self.file)
            read_node["first"].setValue(self.first_frame)
            read_node["last"].setValue(self.last_frame)
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le node read_exr de PirateOverlay a ete supprime")

        if artist:
            artist["message"].setValue(self.artist_value)
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le node artist de PirateOverlay a ete supprime")

        if name:
            name["message"].setValue(f"shot {self.name_value}")
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le node name de PirateOverlay a ete supprime")

        if version:
            print(version_value)
            version["message"].setValue(f"v{str(version_value)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le node version de PirateOverlay a ete supprime")

        if write:
            start_frame = read_node["first"].value()
            end_frame = read_node["last"].value()

            write["file"].setValue(f"I:/COMP/PUBLISH/shot_{self.name_value}_v{(str(version_value))}.mov")
            nuke.execute(write, start_frame, end_frame)
            

            output_mov_path = write["file"].value()

            # Sauvegarder le chemin du fichier .mov dans un fichier texte
            with open("D:\\interface python\\output_path.txt", "w") as f:
                f.write(output_mov_path)

            self.cleanUpNode()

            self.call_publish_script()
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le node Write_mov de PirateOverlay a ete supprime")

    def cleanUpNode(self):

        read_node = nuke.toNode("read_exr")
        artist = nuke.toNode("artist")
        name = nuke.toNode("shot_name")
        version = nuke.toNode("version")
        pirates = nuke.toNode("Pirates")
        framerange = nuke.toNode("framerange")
        write = nuke.toNode("Write_mov")

        ##### all the merges
        merge1 = nuke.toNode("merge_current_frame")

        #### reformat
        reformat1 = nuke.toNode("reformat_mov")
        reformat2 = nuke.toNode("reformat_pre_mov")

        nuke.delete(read_node)
        nuke.delete(artist)
        nuke.delete(name)
        nuke.delete(version)
        nuke.delete(pirates)
        nuke.delete(framerange)
        nuke.delete(write)
        nuke.delete(merge1)
        nuke.delete(reformat1)
        nuke.delete(reformat2)

    def call_publish_script(self):
        os.system("D:\\interface python\\import_discord.py")
      
#define global window, try to close it if already open. Then show  window
def open_mytool_Elissimo():
    global win
    try:
        win.close()
    except:
        pass
    win = mytool()
    win.show()
