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
    
    def __init__(self, mgrc, mgrWidget, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("exec_cxt")

        self.loadECButton = QtGui.QPushButton(u"実行コンテキスト読み込み")
        self.subLayouts[-1].addWidget(self.loadECButton)
        self.loadECButton.clicked.connect(self.loadECSlot)

        self.setOrderFileButton = QtGui.QPushButton(u"実行順序設定ファイルの読み込み")
        self.WidList["exec_cxt.periodic.filename"]["Layout"].addWidget(self.setOrderFileButton)
        self.setOrderFileButton.clicked.connect(self.setOrderFSlot)

        self.mgrWidget = mgrWidget

    def loadECSlot(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Python File (*.py);;All Files (*)")

	if fileName.isEmpty():
            return
        ba = str(fileName.toLocal8Bit())
        fname = os.path.basename(ba)
        name, ext = os.path.splitext(fname)
        dname = os.path.dirname(os.path.relpath(ba))
        

        

        wid = self.mgrWidget.WidList["manager.modules.preload"]["Widget"]
        if wid.findText(fname) == -1:
            wid.addItem(fname)

        wid = self.mgrWidget.WidList["manager.modules.load_path"]["Widget"]

        if dname == "":
            dname = "./" + dname
        if wid.findText(dname) == -1:
            wid.addItem(dname)

        wid = self.WidList["exec_cxt.periodic.type"]["Widget"]
        if wid.findText(name) == -1:
            wid.addItem(name)
            wid.lineEdit().setText(name)

    def setOrderFSlot(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Python File (*.py);;Configuration File (*.conf);;All Files (*)")
        if fileName.isEmpty():
            return

        ba = str(fileName.toLocal8Bit())
        fname = os.path.relpath(ba)

        wid = self.WidList["exec_cxt.periodic.filename"]["Widget"]
        wid.setText(fname)
