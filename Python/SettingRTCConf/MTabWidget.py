#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file .py
#   @brief 



import thread


import optparse
import sys,os,platform
import re
import time
import random
import commands
import math
import imp



import RTC
import OpenRTM_aist

from OpenRTM_aist import CorbaNaming
from OpenRTM_aist import RTObject
from OpenRTM_aist import CorbaConsumer
from omniORB import CORBA
import CosNaming

from PyQt4 import QtCore, QtGui

from ManagerControl import ManagerControl


class MTabWidget(QtGui.QWidget):
    def __init__(self, mgrc, parent=None):
        super(MTabWidget, self).__init__(parent)
        self.mgrc = mgrc
        self.mainLayout = QtGui.QHBoxLayout()

        self.setLayout(self.mainLayout)

        self.WidList = {}
        self.widNum = 0

        self.subLayouts = [QtGui.QVBoxLayout()]
        self.mainLayout.addLayout(self.subLayouts[-1])

    def apendWidget(self, wid, name, label):
        widget = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        Lb = QtGui.QLabel(label)
        
        
        layout.addWidget(Lb)
        layout.addWidget(wid)

        self.widNum += 1
        if self.widNum%7 == 0:
            self.subLayouts.append(QtGui.QVBoxLayout())
            self.mainLayout.addLayout(self.subLayouts[-1])
            
        self.subLayouts[-1].addWidget(widget)

        self.subLayouts[-1].addStretch()

        self.WidList[name] = {"Widget":wid,"Layout":layout}

        return self.WidList[name]
        

    def addCombox(self, name, label, value, ls, default):
        wid = QtGui.QComboBox()
        for l in ls:
            if l != "":
                wid.addItem(l)

        if name == "manager.modules.load_path" or name == "manager.modules.preload" or name == "manager.components.precreate" or name == "corba.endpoints":
            for l in value:
                if l != "":
                    wid.addItem(l)

        
        if len(value) != 0:
            if value[0] != "":
                wid.setCurrentIndex(wid.findText(value[0]))
            else:
                wid.setCurrentIndex(wid.findText(default))
        else:
            wid.setCurrentIndex(wid.findText(default))

        wl = self.apendWidget(wid, name, label)
        wl["Type"] = ManagerControl.Combox
        
        return wl

        

    def addTextCombox(self, name, label, value, ls, default):
        wl = self.addCombox(name, label, value, ls, default)
        wl["Widget"].setLineEdit(QtGui.QLineEdit())
        if len(value) == 0:
            wl["Widget"].lineEdit().setText(default)
        elif value[0] == "":
            wl["Widget"].lineEdit().setText(default)
        else:
            wl["Widget"].lineEdit().setText(value[0])

        
        wl["Type"] = ManagerControl.TextCombox
        
        return wl
        

    def addSpinBox(self, name, label, value, default):
        wid = QtGui.QSpinBox()
        if len(value) == 0:
            wid.setValue(int(default))
        elif value[0] == "":
            wid.setValue(int(default))
        else:
            wid.setValue(int(value[0]))

        wl = self.apendWidget(wid, name, label)
        wl["Type"] = ManagerControl.SpinBox
        
        return wl

        

    def addDoubleSpinBox(self, name, label, value, default):
        wid = QtGui.QDoubleSpinBox()
        if len(value) == 0:
            wid.setValue(float(default))
        elif value[0] == "":
            wid.setValue(float(default))
        else:
            wid.setValue(float(value[0]))

        wl = self.apendWidget(wid, name, label)
        wl["Type"] = ManagerControl.DoubleSpinBox
        
        return wl



    def addTextBox(self, name, label, value, default):
        wid = QtGui.QLineEdit()
        if len(value) == 0:
            wid.setText(default)
        elif value[0] == "":
            wid.setText(default)
        else:
            wid.setText(value[0])

        wl = self.apendWidget(wid, name, label)
        wl["Type"] = ManagerControl.TextBox
        
        return wl


    def setGUI(self, tabName):
        for j in self.mgrc.confList:
            name = j["name"].split(".")[0]
            if name == tabName:
                if j["type"] == ManagerControl.Combox:
                    self.addCombox(j["name"],j["label"],j["value"],j["list"],j["default"])
                elif j["type"] == ManagerControl.TextCombox:
                    self.addTextCombox(j["name"],j["label"],j["value"],j["list"],j["default"])
                elif j["type"] == ManagerControl.SpinBox:
                    self.addSpinBox(j["name"],j["label"],j["value"],j["default"])
                elif j["type"] == ManagerControl.DoubleSpinBox:
                    self.addDoubleSpinBox(j["name"],j["label"],j["value"],j["default"])
                elif j["type"] == ManagerControl.TextBox:
                    self.addTextBox(j["name"],j["label"],j["value"],j["default"])

        
    def mesBox(self, mes):
        msgbox = QtGui.QMessageBox( self )
        msgbox.setText( mes )
        msgbox.setModal( True )
        ret = msgbox.exec_()
