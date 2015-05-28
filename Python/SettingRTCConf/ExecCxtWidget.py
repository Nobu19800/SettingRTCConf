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

from MTabWidget import MTabWidget
from ManagerControl import ManagerControl


class ExecCxtWidget(MTabWidget):
    
    def __init__(self, mgrc, mgrWidget, language="Python", parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("exec_cxt")
        self.language = language

        self.loadECButton = QtGui.QPushButton(u"実行コンテキストをファイルから読み込み")
        self.subLayouts[-1].addWidget(self.loadECButton)
        self.loadECButton.clicked.connect(self.loadECSlot)


        self.addTextBox("filenameBox.sub", u"実行コンテキスト名", [""] , "")
        self.loadFileECButton = QtGui.QPushButton(u"実行コンテキスト読み込み")
        self.WidList["filenameBox.sub"]["Layout"].addWidget(self.loadFileECButton)
        self.loadFileECButton.clicked.connect(self.loadFileECSlot)

        

        self.setOrderFileButton = QtGui.QPushButton(u"実行順序設定をファイルから読み込み")
        self.WidList["exec_cxt.periodic.filename"]["Layout"].addWidget(self.setOrderFileButton)
        self.setOrderFileButton.clicked.connect(self.setOrderFSlot)

        

        
        

        self.mgrWidget = mgrWidget

    

    def loadEC(self, fileName):
        
        
        fname = os.path.basename(fileName)
        name, ext = os.path.splitext(fname)
        dname = [os.path.dirname(fileName)]

        self.mgrc.createEC(dname)
        
        wid = self.mgrWidget.WidList["manager.modules.preload"]["Widget"]
        if wid.findText(fname) == -1:
            wid.addItem(fname)

        wid = self.mgrWidget.WidList["manager.modules.load_path"]["Widget"]

        if dname[0] == "":
            dname[0] = "./" + dname[0]
        if wid.findText(dname[0]) == -1:
            wid.addItem(dname[0])

        wid = self.WidList["exec_cxt.periodic.type"]["Widget"]
        if wid.findText(name) == -1:
            wid.addItem(name)
            wid.lineEdit().setText(name)

    def loadFileECSlot(self):
        wid = self.WidList["filenameBox.sub"]["Widget"]
        s = str(wid.text().toLocal8Bit())
        if s == "":
            return
        self.loadEC(s)

    def loadECSlot(self):
        pyFilePath = "Python File (*.py);;"
        cppFilePath = "Dynamic Link Library (*.dll *.so);;"
        allFilePath = "All Files (*)"
        if self.language == "Python":
            filepath = pyFilePath + cppFilePath + allFilePath
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","",filepath)
        else:
            filepath = cppFilePath + pyFilePath + allFilePath
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","",filepath)

        #fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Python File (*.py);;Dynamic Link Library (*.dll *.so);;All Files (*)")

        if fileName.isEmpty():
            return

        ba = str(fileName.toLocal8Bit())

        self.loadEC(ba)

        

        

    def setOrderFSlot(self):
        pyFilePath = "Python File (*.py);;"
        cppFilePath = "Lua FIle (*.lua);;"
        confFilePath = "Config FIle (*.conf);;"
        allFilePath = "All Files (*)"
        if self.language == "Python":
            filepath = pyFilePath + confFilePath + cppFilePath + allFilePath
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","",filepath)
        else:
            filepath = cppFilePath + confFilePath + pyFilePath + allFilePath
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","",filepath)
        
        if fileName.isEmpty():
            return

        ba = str(fileName.toLocal8Bit())

        dname = [ba]
        self.mgrc.createEC(dname)
        fname = dname[0]
        #fname = os.path.relpath(ba)

        wid = self.WidList["exec_cxt.periodic.filename"]["Widget"]
        wid.setText(fname)
