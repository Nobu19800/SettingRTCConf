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


class ManagerWidget(MTabWidget):
    
    def __init__(self, mgrc, language="Python",  parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("manager")
        self.language = language
        #self.addLangButton = QtGui.QPushButton(u"サポートする言語の追加")
        #self.WidList["manager.supported_languages"]["Layout"].addWidget(self.addLangButton)
        #self.addLangButton.clicked.connect(self.addLangSlot)
        #self.delLangButton = QtGui.QPushButton(u"サポートする言語の削除")
        #self.WidList["manager.supported_languages"]["Layout"].addWidget(self.delLangButton)
        #self.delLangButton.clicked.connect(self.delLangSlot)
        self.createCompButton = QtGui.QPushButton(u"RTC起動")
        self.WidList["manager.components.precreate"]["Layout"].addWidget(self.createCompButton)
        self.createCompButton.clicked.connect(self.createCompSlot)
        self.delCompButton = QtGui.QPushButton(u"RTC終了")
        self.WidList["manager.components.precreate"]["Layout"].addWidget(self.delCompButton)
        self.delCompButton.clicked.connect(self.delCompSlot)
        self.delModuleButton = QtGui.QPushButton(u"モジュール削除")
        self.WidList["manager.modules.preload"]["Layout"].addWidget(self.delModuleButton)
        self.delModuleButton.clicked.connect(self.delModuleSlot)
        self.delPathButton = QtGui.QPushButton(u"パス削除")
        self.WidList["manager.modules.load_path"]["Layout"].addWidget(self.delPathButton)
        self.delPathButton.clicked.connect(self.delPathSlot)

        self.loadRTCButton = QtGui.QPushButton(u"RTコンポーネントをファイルから読み込み")
        self.subLayouts[-1].addWidget(self.loadRTCButton)
        self.loadRTCButton.clicked.connect(self.loadRTCSlot)

        self.addTextBox("filenameBox.sub", u"RTコンポーネント名", [""] , "")
        self.loadFileRTCButton = QtGui.QPushButton(u"RTコンポーネント読み込み")
        self.WidList["filenameBox.sub"]["Layout"].addWidget(self.loadFileRTCButton)
        self.loadFileRTCButton.clicked.connect(self.loadFileRTCSlot)

        

    def loadFileRTCSlot(self):
        wid = self.WidList["filenameBox.sub"]["Widget"]
        s = str(wid.text().toLocal8Bit())
        if s == "":
            return
        self.loadRTC(s)

    def addLangSlot(self):
        wid = self.WidList["manager.supported_languages"]["Widget"]
        
        if wid.findText(wid.currentText()) == -1:
            s = str(wid.currentText().toLocal8Bit())
            if s != "":
                wid.addItem(s)
        

    def delLangSlot(self):
        wid = self.WidList["manager.supported_languages"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    def createCompSlot(self):
        wid = self.WidList["manager.components.precreate"]["Widget"]
        s = str(wid.currentText().toLocal8Bit())
        
        comp = self.mgrc.mgr.createComponent(s)
        if not comp:
            self.mesBox(u"RTCの起動に失敗しました")
            return
        wid.addItem(wid.currentText())

        self.mgrc.addComp(s, comp)

    def delCompSlot(self):
        wid = self.WidList["manager.components.precreate"]["Widget"]
        self.mgrc.deleteComp(str(wid.currentText().toLocal8Bit()))
        wid.removeItem(wid.findText(wid.currentText()))

        

    def delModuleSlot(self):
        wid = self.WidList["manager.modules.preload"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    def delPathSlot(self):
        wid = self.WidList["manager.modules.load_path"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    def loadRTC(self, fileName):
        fname = os.path.basename(fileName)
        name, ext = os.path.splitext(fname)

	tmp_dname = os.path.dirname(fileName)
        dname = [tmp_dname]


        if self.mgrc.createComp(name,dname) == False:
            self.mesBox(u"モジュールの読み込みに失敗しました")
            return

        if tmp_dname == "/usr/local/components/lib":
            dname = [tmp_dname]

        wid = self.WidList["manager.components.precreate"]["Widget"]
        wid.addItem(name)

        wid = self.WidList["manager.modules.preload"]["Widget"]
        if wid.findText(fname) == -1:
            wid.addItem(fname)

        wid = self.WidList["manager.modules.load_path"]["Widget"]

        if dname[0] == "":
            dname[0] = "./" + dname[0]
        if wid.findText(dname[0]) == -1:
            
            wid.addItem(dname[0])

    def loadRTCSlot(self):
        pyFilePath = "Python File (*.py);;"
        cppFilePath = "Dynamic Link Library (*.dll *.so);;"
        allFilePath = "All Files (*)"
        if self.language == "Python":
            filepath = pyFilePath + cppFilePath + allFilePath
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","",filepath)
        else:
            filepath = cppFilePath + pyFilePath + allFilePath
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","",filepath)

        if fileName.isEmpty():
            return
        ba = str(fileName.toLocal8Bit())

        self.loadRTC(ba)
