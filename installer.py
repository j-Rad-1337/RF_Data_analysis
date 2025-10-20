#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QBrush

import subprocess
import os
import sys
import time
import re

this_file_directory = os.path.dirname(os.path.realpath(__file__))
fissure_directory = os.path.abspath(os.path.join(this_file_directory, os.pardir))

form_class = uic.loadUiType(fissure_directory + "/UI/install.ui")[0]
form_class2 = uic.loadUiType(fissure_directory + "/UI/install2.ui")[0]

# Program Format: ('name','command',checked/default, parent_category)

larger_categories = [
    'Minimum Install',
    'Remote Sensor Node',
    'Hardware',
    'Out-of-Tree Modules',
    'Compile Flow Graphs',
    '433 MHz','802.11',
    'Aircraft',
    'AIS',
    'Audio',
    'Bluetooth',
    'Data',
    'Development',
    'Filters',
    'GPS',
    'GSM',
    'Ham Radio',
    'HD Radio',
    'LTE',
    'M17',
    'Mapping',
    'POCSAG',
    'Radiosonde',
    'RFID',
    'Satellite',
    'SDR',
    'SSH',
    'Trunked Radio',
    'V2V',
    'Video',
    'Z-Wave'
]


########################################################################


class InstallDialog2(QtWidgets.QDialog, form_class2):
    def __init__(self,programs):
        """ Software Selection Dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        
        # Prevent Resizing/Maximizing
        self.setFixedSize(920, 650)     

        # Hide Progress Bar
        self.progressBar1.hide()   
        self.label2_current_item.hide()
        
        # Set Style Sheet
        color1 = "#F4F4F4"
        color2 = "#FBFBFB"
        color3 = "#17365D"
        color4 = "#000000"
        color5 = "#FFFFFF"
        color6 = "#FEFEFE"
        color7 = "#EFEFEF"
        color8 = "#FEFEFE"
        color9 = "#EFEFEF"
        color10 = "#FEFEFE"
        color11 = "#F8F8F8"
        color12 = "#000000"
        color13 = "#C0C0C0"        
        get_css_text = str(open('/' + os.path.dirname(os.path.realpath(__file__)).strip('/Installer') + "/UI/Style_Sheets/light.css","r").read())
        get_css_text = re.sub(r'@color1\b',color1,get_css_text)
        get_css_text = re.sub(r'@color2\b',color2,get_css_text)
        get_css_text = re.sub(r'@color3\b',color3,get_css_text)
        get_css_text = re.sub(r'@color4\b',color4,get_css_text)
        get_css_text = re.sub(r'@color5\b',color5,get_css_text)
        get_css_text = re.sub(r'@color6\b',color6,get_css_text)
        get_css_text = re.sub(r'@color7\b',color7,get_css_text)
        get_css_text = re.sub(r'@color8\b',color8,get_css_text)
        get_css_text = re.sub(r'@color9\b',color9,get_css_text)
        get_css_text = re.sub(r'@color10\b',color10,get_css_text)
        get_css_text = re.sub(r'@color11\b',color11,get_css_text)
        get_css_text = re.sub(r'@color12\b',color12,get_css_text)
        get_css_text = re.sub(r'@color13\b',color13,get_css_text)
        get_css_text = re.sub(r'@unchecked_enabled\b','light-unchecked.png',get_css_text)
        get_css_text = re.sub(r'@checked_enabled\b','light-checked.png',get_css_text)
        get_css_text = re.sub(r'@checked_disabled\b','light-checked-disabled.png',get_css_text)
        get_css_text = re.sub(r'@unchecked_disabled\b','light-unchecked-disabled.png',get_css_text)
        get_css_text = re.sub(r'@down_arrow_enabled\b','light-down-arrow.png',get_css_text)
        get_css_text = re.sub(r'@down_arrow_disabled\b','light-down-arrow-disabled.png',get_css_text)
        get_css_text = re.sub(r'@radio_unchecked_enabled\b','light-radio.png',get_css_text)
        get_css_text = re.sub(r'@radio_checked_enabled\b','light-radio-checked.png',get_css_text)
        get_css_text = get_css_text.replace("@icon_path",'/' + os.path.dirname(os.path.realpath(__file__)).strip('/Installer') + "/docs/Icons")
        get_css_text = get_css_text.replace('@menu_hover_padding','0px')
        self.setStyleSheet(get_css_text)
        
        # Do SIGNAL/Slots Connections
        self._connectSlots()  
        
        # Create Categories
        for c in larger_categories:
            parent = QtWidgets.QTreeWidgetItem(self.treeWidget_software)
            parent.setText(0,c)
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Checked)
        
        # Load Checkboxes in Table
        self.programs = programs
        for row in range(0,len(programs)):
            # Subcategories
            if programs[row][3] != None:
                parent_name = programs[row][3]
                
                # Iterate the Tree
                iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
                while iterator.value():
                    item = iterator.value()
                    if item.text(0) == parent_name:
                        child = QtWidgets.QTreeWidgetItem(item)
                        child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                        child.setText(0, programs[row][0])
                        if programs[row][2] == True:
                            child.setCheckState(0, QtCore.Qt.Checked)
                        else:
                            child.setCheckState(0, QtCore.Qt.Unchecked)
                        break
                    iterator+=1      
            
            # No Category
            else:            
                parent = QtWidgets.QTreeWidgetItem(self.treeWidget_software)
                parent.setText(0,programs[row][0])
                parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                if programs[row][2] == True:
                    parent.setCheckState(0, QtCore.Qt.Checked)
                else:
                    parent.setCheckState(0, QtCore.Qt.Unchecked)

        # Remove Empty Categories
        root = self.treeWidget_software.invisibleRootItem()
        for i in range(root.childCount() - 1, -1, -1):  # Iterate in reverse order
            parent = root.child(i)
            if parent.childCount() == 0:
                root.removeChild(parent)

            
    def _connectSlots(self):
        """ Contains the connect functions for all the signals and slots
        """   
        # Push Buttons
        self.pushButton_ok.clicked.connect(self._slotOK_Clicked)
        self.pushButton_cancel.clicked.connect(self._slotCancelClicked)
        self.pushButton_deselect.clicked.connect(self._slotDeselectClicked)
        self.pushButton_rankings.clicked.connect(self._slotRankingsClicked)
        self.pushButton_needs_help.clicked.connect(self._slotNeedsHelpClicked)
        self.pushButton_expand_all.clicked.connect(self._slotExpandAllClicked)
        self.pushButton_collapse_all.clicked.connect(self._slotCollapseAllClicked)
        self.pushButton_import.clicked.connect(self._slotImportClicked)
        self.pushButton_export.clicked.connect(self._slotExportClicked)
        self.pushButton_full.clicked.connect(self._slotFullClicked)
        self.pushButton_sensor_node.clicked.connect(self._slotSensorNodeClicked)       
        self.pushButton_hiprfisr.clicked.connect(self._slotHiprfisrClicked)
        self.pushButton_dashboard.clicked.connect(self._slotDashboardClicked)
        
        # Tables
        self.treeWidget_software.clicked.connect(self._slotTableItemClicked)


    def _slotOK_Clicked(self):
        """ Install the software.
        """      
        # Find Number of Checked Items and Store Names (prevents checking after starting the install)
        get_checked_items = 0
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        self.checked_items = []
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == 2:    
                # Ignore Categories
                if item.text(0) not in larger_categories:       
                    get_checked_items = get_checked_items + 1
                    self.checked_items.append(item.text(0))     
            iterator+=1   
            
        # Reset the Colors
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item.setForeground(0,QtGui.QColor('Black'))
            iterator+=1   
            
        # Show Progress Bar
        self.progressBar1.show() 
        self.label2_current_item.show()      
        self.progressBar1.setMaximum(get_checked_items+1)
        QtWidgets.QApplication.processEvents()
        self.pushButton_ok.setEnabled(False)

        # Clear the Output File
        with open(this_file_directory + "/disk_usage.txt", "w") as file:
            file.write("")

        # Iterate the Checked Items
        self.checked_index = 0
        for n in range(0,len(self.checked_items)):            
            # Find the Install Code
            for p in range(0,len(self.programs)):
                if self.checked_items[n] == self.programs[p][0]:
                    self.loop = True

                    # Calculate Disk Usage - Before
                    statvfs_before = os.statvfs('/')
                    total_before = statvfs_before.f_frsize * statvfs_before.f_blocks
                    free_before = statvfs_before.f_frsize * statvfs_before.f_bfree
                    used_before = total_before - free_before
                    
                    # Update the Label
                    self.label2_current_item.setText(str(self.checked_items[n]))
            
                    # Split Install Commands and Verifier Commands
                    install_command = self.programs[p][1].split("########## Verify ##########")
                    
                    # Verify Code Found
                    if len(install_command) == 2:
                        self.verify_code = install_command[1]
                    else:
                        self.verify_code = ""
                        
                    self.loadthread = MyThread(install_command[0], self)                        
                    self.loadthread.finished.connect(self.on_finished)
                    self.loadthread.start()
                                      
                    self.progressBar1.setValue(self.checked_index+1)
                    self.checked_index = self.checked_index + 1
                    
                    while self.loop == True:
                        QtWidgets.QApplication.processEvents()
                        time.sleep(0.1)

                    # Calculate Disk Usage - After
                    statvfs_after = os.statvfs('/')
                    total_after = statvfs_after.f_frsize * statvfs_after.f_blocks
                    free_after = statvfs_after.f_frsize * statvfs_after.f_bfree
                    used_after = total_after - free_after

                    # Write to File
                    used = used_after - used_before
                    used_gb = used / (1024 ** 3)
                    used_mb = used / (1024 ** 2)
                    used_kb = used / 1024
                    if int(used_gb) > 0:
                        text_output = str(self.checked_items[n]).split('(')[0].strip() + f" ({used_gb:.2f} GB)"
                    elif int(used_mb) > 0:
                        text_output = str(self.checked_items[n]).split('(')[0].strip() + f" ({used_mb:.2f} MB)"
                    else:
                        text_output = str(self.checked_items[n]).split('(')[0].strip() + f" ({used_kb:.2f} kB)"
                    with open(this_file_directory + "/disk_usage.txt", "a") as file:
                        file.write(text_output + "\n")

        # Finished
        self.progressBar1.setValue(self.checked_index+1)
        print("\nInstall Complete")
        time.sleep(2)
        self.progressBar1.hide()
        self.label2_current_item.hide() 
        self.pushButton_ok.setEnabled(True)
        #self.accept()

        
    @QtCore.pyqtSlot()
    def on_finished(self):
        """ Proceed to the next program.
        """
        # Verify
        if len(self.verify_code) > 0:
            iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
            while iterator.value():
                item = iterator.value()
                if item.text(0) == self.checked_items[self.checked_index-1]:
                    # Verify Success
                    try:
                        p1 = subprocess.check_call(self.verify_code, shell=True)
                        print("VERIFY SUCCESS")
                        item.setForeground(0,QtGui.QColor('Green'))
                        
                    # Verify Failure
                    except:
                        print("VERIFY FAILURE")
                        item.setForeground(0,QtGui.QColor('Red'))
                    break
                iterator+=1  
            
        
        self.loop = False
        

    def _slotCancelClicked(self):
        """ Close everything.
        """
        self.close()
        

    def _slotTableItemClicked(self, item):
        """ Update text edit box with command text when table row is clicked.
        """
        # Clicked Item
        try:
            current_item = self.treeWidget_software.currentItem().text(0)  # Deselect All and checking a box causes an error
        except:
            return  

        # Search Programs
        for p in range(0,len(self.programs)):
            if current_item == self.programs[p][0]:
                self.plainTextEdit_commands.setPlainText(self.programs[p][1])
                break
        

    def _slotDeselectClicked(self):
        """ Unchecks all the checkboxes.
        """
        # Iterate the Tree
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            iterator+=1  
                       

    def _slotRankingsClicked(self):
        """ Opens a window with the programs sorted by size.
        """
        # Extract the Sizes
        sizes = []        
        for p in range(0,len(self.programs)):
            if '(' in self.programs[p][0] and ')' in self.programs[p][0]:
                get_size = self.programs[p][0].split(' (')[-1].replace(')','')
                if get_size.endswith(" GB"):
                    get_size = int(float(get_size[:-3]) * 1024 * 1024 * 1024)
                elif get_size.endswith(" MB"):
                    get_size = int(float(get_size[:-3]) * 1024 * 1024)
                elif get_size.endswith(" kB") or get_size.endswith(" KB"):
                    get_size = int(float(get_size[:-3]) * 1024)
                else:
                    get_size = 0
                sizes.append(get_size)
            else:
                sizes.append(0)
                
        indices = [i[0] for i in sorted(enumerate(sizes), key=lambda x:x[1], reverse=True)]
            
        msg_text = "Top 30:\n"
        count = 0
        for n in indices:
            msg_text = msg_text + "\t" + self.programs[n][0] + "\n"
            count = count + 1
            if count == 30:
                break
            
        msg_text = msg_text + "\n\nTotal (Estimate):\n\t " + str(round(sum(sizes)/(1024*1024*1024),1)) + " GB"
            
        # Create the Message Box
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(msg_text)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        ret = msgBox.exec_()

    
    def _slotNeedsHelpClicked(self):
        """ Opens a window with a list of installer items that are not checked by default.
        """
        # Get Unchecked Items
        unchecked_items = []        
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()            
            for p in range(0,len(self.programs)):
                if item.text(0) == self.programs[p][0]:
                    if self.programs[p][2] == False:
                        unchecked_items.append(item.text(0))
                    break
            iterator+=1  
        
        # Build the Message
        msg_text = "These programs need help with installation. \nPlease suggest fixes on GitHub or Discord.\n\n"
        for n in unchecked_items:
            msg_text = msg_text + "\t" + n + "\n"
            
        # Create the Message Box
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(msg_text)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        ret = msgBox.exec_()
        

    def _slotExpandAllClicked(self):
        """ Expands the tree widget.
        """
        # Expand
        self.treeWidget_software.expandAll()
        

    def _slotCollapseAllClicked(self):
        """ Collapses the tree widget.
        """
        # Collapse
        self.treeWidget_software.collapseAll()
        

    def _slotImportClicked(self):
        """ Imports a yaml file for checking installer items.
        """
        # Open the File
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open YAML File', this_file_directory, filter='YAML (*.yaml)')
        lines = []
        if len(path[0]) > 0:
            with open(path[0], 'r') as file:
                lines = file.readlines()
        else:
            return

        # Convert to List
        checked_items = []
        for line in lines:
            if line.strip().startswith('-'):
                checked_items.append(line.strip().lstrip('- ').strip())

        # Uncheck all Items
        self._slotDeselectClicked()

        # Iterate the Tree
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()            
            for p in range(0,len(checked_items)):
                if item.text(0).split('(')[0].strip() == checked_items[p]:
                    item.setCheckState(0, QtCore.Qt.Checked)
                    break
            iterator+=1  


    def _slotExportClicked(self):
        """ Saves checked items to a yaml file to be imported.
        """
        # Get Checked Items
        checked_items = []        
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == 2:    
                # Ignore Categories
                if item.text(0) not in larger_categories:       
                    checked_items.append(item.text(0).split('(')[0].strip())
            iterator+=1   

        # Save List to YAML
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save YAML File', this_file_directory, filter='YAML (*.yaml)')
        if len(path[0]) > 0:
            if path[0].endswith(".yaml") == False:
                path[0] = path[0] + ".yaml"
            with open(path[0], 'w') as file:
                file.write("checked_items:\n")
                for item in checked_items:
                    file.write(f"  - {item}\n")


    def _slotFullClicked(self):
        """ Checks the default checkboxes.
        """
        # Iterate the Tree
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()            
            for p in range(0,len(self.programs)):
                if item.text(0) == self.programs[p][0]:
                    if self.programs[p][2] == True:
                        item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        item.setCheckState(0, QtCore.Qt.Unchecked)
                    break           
            iterator+=1  

  
    def _slotSensorNodeClicked(self):
        """ Checks minimum required items to install on a remote FISSURE tactical node.
        """
        from Modes.sensornode import required_items

        # Step 1: Uncheck all items
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            iterator += 1

        # Step 2: Check only items in the required list
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item_name = item.text(0).split('(')[0].strip()  # ignore sizes like " (3.4 MB)"
            if item_name in required_items:
                item.setCheckState(0, QtCore.Qt.Checked)
            iterator += 1


    def _slotHiprfisrClicked(self):
        """ Checks minimum required items to install the FISSURE HIPRFISR/central hub.
        """
        from Modes.hiprfisr import required_items

        # Step 1: Uncheck all items
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            iterator += 1

        # Step 2: Check only items in the required list
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item_name = item.text(0).split('(')[0].strip()  # ignore sizes like " (3.4 MB)"
            if item_name in required_items:
                item.setCheckState(0, QtCore.Qt.Checked)
            iterator += 1


    def _slotDashboardClicked(self):
        """ Checks minimum required items to install the FISSURE Dashboard.
        """
        from Modes.dashboard import required_items

        # Step 1: Uncheck all items
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            iterator += 1

        # Step 2: Check only items in the required list
        iterator = QtWidgets.QTreeWidgetItemIterator(self.treeWidget_software)
        while iterator.value():
            item = iterator.value()
            item_name = item.text(0).split('(')[0].strip()  # ignore sizes like " (3.4 MB)"
            if item_name in required_items:
                item.setCheckState(0, QtCore.Qt.Checked)
            iterator += 1

        
class MyThread(QtCore.QThread):
    def __init__(self, n, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.n = n


    def run(self):
        try:
            #print(self.n)
            p1 = subprocess.Popen(self.n, shell=True)
            p1.wait()
        except:
            print("FAILURE") 


class InstallDialog1(QtWidgets.QDialog, form_class):
    def __init__(self):
        """ Operating System Dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        
        # Prevent Resizing/Maximizing
        self.setFixedSize(320, 435)
        
        # Set Style Sheet
        color1 = "#F4F4F4"
        color2 = "#FBFBFB"
        color3 = "#17365D"
        color4 = "#000000"
        color5 = "#FFFFFF"
        color6 = "#FEFEFE"
        color7 = "#EFEFEF"
        color8 = "#FEFEFE"
        color9 = "#EFEFEF"
        color10 = "#FEFEFE"
        color11 = "#F8F8F8"
        color12 = "#000000"
        color13 = "#C0C0C0"        
        get_css_text = str(open('/' + os.path.dirname(os.path.realpath(__file__)).strip('/Installer') + "/UI/Style_Sheets/light.css","r").read())
        get_css_text = re.sub(r'@color1\b',color1,get_css_text)
        get_css_text = re.sub(r'@color2\b',color2,get_css_text)
        get_css_text = re.sub(r'@color3\b',color3,get_css_text)
        get_css_text = re.sub(r'@color4\b',color4,get_css_text)
        get_css_text = re.sub(r'@color5\b',color5,get_css_text)
        get_css_text = re.sub(r'@color6\b',color6,get_css_text)
        get_css_text = re.sub(r'@color7\b',color7,get_css_text)
        get_css_text = re.sub(r'@color8\b',color8,get_css_text)
        get_css_text = re.sub(r'@color9\b',color9,get_css_text)
        get_css_text = re.sub(r'@color10\b',color10,get_css_text)
        get_css_text = re.sub(r'@color11\b',color11,get_css_text)
        get_css_text = re.sub(r'@color12\b',color12,get_css_text)
        get_css_text = re.sub(r'@color13\b',color13,get_css_text)
        get_css_text = re.sub(r'@unchecked_enabled\b','light-unchecked.png',get_css_text)
        get_css_text = re.sub(r'@checked_enabled\b','light-checked.png',get_css_text)
        get_css_text = re.sub(r'@checked_disabled\b','light-checked-disabled.png',get_css_text)
        get_css_text = re.sub(r'@unchecked_disabled\b','light-unchecked-disabled.png',get_css_text)
        get_css_text = re.sub(r'@down_arrow_enabled\b','light-down-arrow.png',get_css_text)
        get_css_text = re.sub(r'@down_arrow_disabled\b','light-down-arrow-disabled.png',get_css_text)
        get_css_text = re.sub(r'@radio_unchecked_enabled\b','light-radio.png',get_css_text)
        get_css_text = re.sub(r'@radio_checked_enabled\b','light-radio-checked.png',get_css_text)
        get_css_text = get_css_text.replace("@icon_path",'/' + os.path.dirname(os.path.realpath(__file__)).strip('/Installer') + "/docs/Icons")
        get_css_text = get_css_text.replace('@menu_hover_padding','0px')
        self.setStyleSheet(get_css_text)  
        
        # Do SIGNAL/Slots Connections
        self._connectSlots()  
        
        # Detect Operating System
        process = subprocess.Popen('lsb_release -d', shell=True, stdout=subprocess.PIPE, encoding='utf8')
        stdout = process.communicate()[0]
       
        # Detect x86_64 or ARM
        process2 = subprocess.Popen('lscpu', shell=True, stdout=subprocess.PIPE, encoding='utf8')
        stdout2 = process2.communicate()[0]        

        # Select Radio Button
        if "Ubuntu 20.04" in stdout:
            self.radioButton_ubuntu20_04.setChecked(True)
        elif "Parrot" in stdout:
            self.radioButton_parrot_os_6_1.setChecked(True)
        elif "DragonOS" in stdout:
            self.radioButton_dragonos_noble.setChecked(True)
        elif "KDE neon" in stdout:
            if "5.25" in stdout:
                self.radioButton_kde_neon_5_25.setChecked(True)
        elif "Ubuntu 22.04" in stdout:
              self.radioButton_ubuntu22_04.setChecked(True)            
        elif "Kali" in stdout:
            self.radioButton_kali.setChecked(True)
        elif "BackBox" in stdout:  # Check this again
            self.radioButton_backbox_linux_8.setChecked(True)            
        elif "bookworm" in stdout or "pixie" in stdout:
            self.radioButton_raspberry_pi_os.setChecked(True)
        elif "Ubuntu 24.04" in stdout:
            self.radioButton_ubuntu24_04.setChecked(True) 
        elif "Arch Linux" in stdout:
            self.radioButton_arch_linux.setChecked(True) 

        self.get_os = ""
        

    def _connectSlots(self):
        """ Contains the connect functions for all the signals and slots
        """   
        # Push Buttons
        self.pushButton_ok.clicked.connect(self._slotOK_Clicked)
        self.pushButton_cancel.clicked.connect(self._slotCancelClicked)
        

    def _slotOK_Clicked(self):
        """ Return to open the second install dialog.
        """        
        # Select Software for Operating System
        if self.radioButton_ubuntu20_04.isChecked():
            self.get_os = "Ubuntu 20.04"         
        elif self.radioButton_parrot_os_6_1.isChecked():
            self.get_os = "Parrot OS 6.1"            
        elif self.radioButton_kde_neon_5_25.isChecked():
            self.get_os = "KDE neon 5.25"
        elif self.radioButton_ubuntu22_04.isChecked():
            self.get_os = "Ubuntu 22.04"
        elif self.radioButton_dragonos_noble.isChecked():
            self.get_os = "DragonOS Noble"
        elif self.radioButton_kali.isChecked():
            self.get_os = "Kali 2024.3"
        elif self.radioButton_backbox_linux_8.isChecked():
            self.get_os = "BackBox Linux 8"
        elif self.radioButton_raspberry_pi_os.isChecked():
            self.get_os = "Raspberry Pi OS"
        elif self.radioButton_ubuntu24_04.isChecked():
            self.get_os = "Ubuntu 24.04"
        elif self.radioButton_arch_linux.isChecked():
            self.get_os = "Arch Linux"
            
        self.accept()
        

    def _slotCancelClicked(self):
        """ Close everything.
        """
        self.close()



def main(argv):
    """ The start of everything.
    """   
    import os
    import sys
    import subprocess
    from PyQt5 import QtWidgets

    # --- HEADLESS MODE (Non-interactive install) ---
    if "--headless" in argv:
        os_arg = os.getenv("FISSURE_OS")
        mode_arg = os.getenv("FISSURE_MODE")

        if not os_arg or not mode_arg:
            print("Error: FISSURE_OS and FISSURE_MODE environment variables not set.")
            sys.exit(1)

        print(f"[*] Running headless install: OS={os_arg}, Mode={mode_arg}")

        # --- Select OS Program List ---
        if "Ubuntu 24.04" in os_arg:
            from OS.ubuntu24_04 import programs_ubuntu24_04 as programs
        elif "Ubuntu 22.04" in os_arg:
            from OS.ubuntu22_04 import programs_ubuntu22_04 as programs
        elif "DragonOS" in os_arg:
            from OS.dragonOS_noble import programs_dragonOS_noble as programs
        elif "Parrot" in os_arg:
            from OS.parrot_os import programs_parrot_os_6_1 as programs
        elif "Kali" in os_arg:
            from OS.kali23_1 import programs_kali as programs
        elif "BackBox" in os_arg:
            from OS.backbox import programs_backbox_linux_8 as programs
        elif "Raspberry Pi OS" in os_arg:
            from OS.raspberry_pi_os import programs_raspberry_pi_os as programs
        else:
            print(f"Unsupported OS: {os_arg}")
            sys.exit(1)

        # --- Select Install Mode ---
        mode_arg = mode_arg.lower()
        selected_programs = []

        if mode_arg == "full":
            selected_programs = [p for p in programs if p[2] is True]

        elif mode_arg == "base":
            print("Base install not supported yet. Exiting.")
            sys.exit(1)
            from Modes.base import required_items
            selected_programs = [p for p in programs if p[0].split('(')[0].strip() in required_items]

        elif mode_arg == "hiprfisr":
            print("HIPRFISR install not supported yet. Exiting.")
            sys.exit(1)
            from Modes.hiprfisr import required_items
            selected_programs = [p for p in programs if p[0].split('(')[0].strip() in required_items]

        elif mode_arg == "dashboard":
            print("Dashboard install not supported yet. Exiting.")
            sys.exit(1)
            from Modes.dashboard import required_items
            selected_programs = [p for p in programs if p[0].split('(')[0].strip() in required_items]

        elif mode_arg in ("sensor", "sensornode"):
            from Modes.sensornode import required_items         
            selected_programs = [p for p in programs if p[0].split('(')[0].strip() in required_items]

        elif mode_arg == "custom":
            from Modes.custom import required_items
            selected_programs = [p for p in programs if p[0].split('(')[0].strip() in required_items]

        else:
            print(f"Unknown mode: {mode_arg}")
            sys.exit(1)

        # --- Run Installs Sequentially ---
        print(f"[*] Installing {len(selected_programs)} program(s)...")
        for name, command, _, _ in selected_programs:
            print(f"[INSTALL] {name}")
            result = subprocess.run(command, shell=True)
            if result.returncode != 0:
                print(f"[ERROR] {name} installation failed (code {result.returncode})")
            else:
                print(f"[OK] {name} installed successfully")

        print("[*] Headless installation complete.")
        sys.exit(0)


    # --- GUI MODE (Interactive install) ---
    app = QtWidgets.QApplication(argv) 

    # Operating System Dialog
    install_dlg1 = InstallDialog1()
    install_dlg1.show() 
    
    # OK Clicked
    if install_dlg1.exec_() == QtWidgets.QDialog.Accepted:
        if install_dlg1.get_os == "Ubuntu 20.04":
            from OS.ubuntu20_04 import programs_ubuntu20_04
            install_dlg2 = InstallDialog2(programs_ubuntu20_04)
        elif install_dlg1.get_os == "Parrot OS 6.1":
            from OS.parrot_os import programs_parrot_os_6_1
            install_dlg2 = InstallDialog2(programs_parrot_os_6_1)
        elif install_dlg1.get_os == "KDE neon 5.25":
            from OS.ubuntu20_04 import programs_ubuntu20_04
            install_dlg2 = InstallDialog2(programs_ubuntu20_04)
        elif install_dlg1.get_os == "Ubuntu 22.04":
            from OS.ubuntu22_04 import programs_ubuntu22_04
            install_dlg2 = InstallDialog2(programs_ubuntu22_04)
        elif install_dlg1.get_os == "DragonOS Noble":
            from OS.dragonOS_noble import programs_dragonOS_noble
            install_dlg2 = InstallDialog2(programs_dragonOS_noble)
        elif "Kali" in install_dlg1.get_os:
            from OS.kali23_1 import programs_kali
            install_dlg2 = InstallDialog2(programs_kali)
        elif install_dlg1.get_os == "BackBox Linux 8":
            from OS.backbox import programs_backbox_linux_8
            install_dlg2 = InstallDialog2(programs_backbox_linux_8)
        elif install_dlg1.get_os == "Raspberry Pi OS":
            from OS.raspberry_pi_os import programs_raspberry_pi_os
            install_dlg2 = InstallDialog2(programs_raspberry_pi_os)
        elif install_dlg1.get_os == "Ubuntu 22.04 ARM":
            from OS.ubuntu24_04 import programs_ubuntu24_04
            install_dlg2 = InstallDialog2(programs_ubuntu24_04)
        elif install_dlg1.get_os == "Ubuntu 24.04":
            from OS.ubuntu24_04 import programs_ubuntu24_04
            install_dlg2 = InstallDialog2(programs_ubuntu24_04)
        elif "Arch Linux" in install_dlg1.get_os:
            return

        install_dlg2.show() 

        # Install Clicked
        if install_dlg2.exec_() == QtWidgets.QDialog.Accepted:
            pass
            # print("Install Complete")

    sys.exit()


if __name__ == "__main__":
    main(sys.argv)
