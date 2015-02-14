#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file SettingRTCConf.py
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


class MTabWidget(QtGui.QWidget):
    UpdateSizeSignal = QtCore.pyqtSignal()
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

        
        
        

        

class ManagerWidget(MTabWidget):
    
    def __init__(self, mgrc, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("manager")
        self.addLangButton = QtGui.QPushButton(u"サポートする言語の追加")
        self.WidList["manager.supported_languages"]["Layout"].addWidget(self.addLangButton)
        self.addLangButton.clicked.connect(self.addLangSlot)
        self.delLangButton = QtGui.QPushButton(u"サポートする言語の削除")
        self.WidList["manager.supported_languages"]["Layout"].addWidget(self.delLangButton)
        self.delLangButton.clicked.connect(self.delLangSlot)
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

    def loadRTCSlot(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Python File (*.py);;All Files (*)")

	if fileName.isEmpty():
            return
        ba = str(fileName.toLocal8Bit())
        fname = os.path.basename(ba)
        name, ext = os.path.splitext(fname)
        dname = os.path.dirname(os.path.relpath(ba))
        if self.mgrc.createComp(name,[dname]) == False:
            self.mesBox(u"モジュールの読み込みに失敗しました")
            return

        wid = self.WidList["manager.components.precreate"]["Widget"]
        wid.addItem(name)

        wid = self.WidList["manager.modules.preload"]["Widget"]
        if wid.findText(fname) == -1:
            wid.addItem(fname)

        wid = self.WidList["manager.modules.load_path"]["Widget"]

        if dname == "":
            dname = "./" + dname
        if wid.findText(dname) == -1:
            
            wid.addItem(dname)

    

    
        

class CorbaWidget(MTabWidget):
    
    def __init__(self, mgrc, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("corba")

        self.addEndpointsButton = QtGui.QPushButton(u"エンドポイント追加")
        self.WidList["corba.endpoints"]["Layout"].addWidget(self.addEndpointsButton)
        self.addEndpointsButton.clicked.connect(self.addEndpointsSlot)

        self.delEndpointsButton = QtGui.QPushButton(u"エンドポイント削除")
        self.WidList["corba.endpoints"]["Layout"].addWidget(self.delEndpointsButton)
        self.delEndpointsButton.clicked.connect(self.delEndpointsSlot)

    def addEndpointsSlot(self):
        wid = self.WidList["corba.endpoints"]["Widget"]
        
        if wid.findText(wid.currentText()) == -1:
            s = str(wid.currentText().toLocal8Bit())
            if s != "":
                wid.addItem(s)
        

    def delEndpointsSlot(self):
        wid = self.WidList["corba.endpoints"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))
        

class ConfigWidget(MTabWidget):
    
    def __init__(self, mgrc, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("config")

class NamingWidget(MTabWidget):
    
    def __init__(self, mgrc, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("naming")

class LoggerWidget(MTabWidget):
    
    def __init__(self, mgrc, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("logger")

class TimerWidget(MTabWidget):
    
    def __init__(self, mgrc, parent=None):
        MTabWidget.__init__(self, mgrc, parent)
        self.setGUI("timer")

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

        

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        

        self.tab_widget = QtGui.QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.createAction()
	self.createMenus()

	#self.mgrc = ManagerControl("")
	self.mgrc = None
	

	#self.mgrc.CreateComp("MyFirstComponent",[".\\MyFirstComponent"])
        #self.mgrc.CreateComp("MyFirstComponent",[".\\MyFirstComponent"])
        
    ##
    #アクションの作成の関数
    ##
    def createAction(self):

	self.newAct = QtGui.QAction("&New...",self)
	self.newAct.setShortcuts(QtGui.QKeySequence.New)
        self.newAct.triggered.connect(self.newFile)
        


	self.openAct = QtGui.QAction("&Open...",self)
        self.openAct.setShortcuts(QtGui.QKeySequence.Open)
        self.openAct.triggered.connect(self.open)


        self.saveAct = QtGui.QAction("&Save",self)
        self.saveAct.setShortcuts(QtGui.QKeySequence.Save)
        self.saveAct.triggered.connect(self.save)

    ##
    #メニューの作成の関数
    ##
    def createMenus(self):

	self.fileMenu = self.menuBar().addMenu("&File")
	self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)


    def createTabs(self):
        self.Tabs = []
        self.ManagerTab = ManagerWidget(self.mgrc)
        self.tab_widget.addTab(self.ManagerTab, u"マネージャ")
        self.Tabs.append(self.ManagerTab)
        self.CorbaTab = CorbaWidget(self.mgrc)
	self.tab_widget.addTab(self.CorbaTab, u"CORBA")
	self.Tabs.append(self.CorbaTab)
	self.ConfigTab = ConfigWidget(self.mgrc)
	self.tab_widget.addTab(self.ConfigTab, u"一般的")
	self.Tabs.append(self.ConfigTab)
	self.NamingTab = NamingWidget(self.mgrc)
	self.tab_widget.addTab(self.NamingTab, u"ネームサービス")
	self.Tabs.append(self.NamingTab)
	self.LoggerTab = LoggerWidget(self.mgrc)
	self.tab_widget.addTab(self.LoggerTab, u"ロガー")
	self.Tabs.append(self.LoggerTab)
	self.TimerTab = TimerWidget(self.mgrc)
	self.tab_widget.addTab(self.TimerTab, u"タイマ")
	self.Tabs.append(self.TimerTab)
	self.ExecCxtTab = ExecCxtWidget(self.mgrc, self.ManagerTab)
	self.tab_widget.addTab(self.ExecCxtTab, u"実行コンテキスト")
	self.Tabs.append(self.ExecCxtTab)
	

    ##
    #ファイル読み込みスロット
    ##
    def open(self):
        if self.mgrc == None:
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Config File (*.conf);;All Files (*)")
            if fileName.isEmpty():
                return
            ba = str(fileName.toLocal8Bit())
            #ba = ba.replace("/","\\")
            self.mgrc = ManagerControl(ba)
            self.createTabs()

            

            
        else:
            self.mesBox(u"既にコンフィギュレーションファイルは開いています")

    ##
    #ファイル保存のスロット
    ##
    def save(self):

	fileName = QtGui.QFileDialog.getSaveFileName(self,u"保存", "","Config File (*.conf);;All Files (*)")
	if fileName.isEmpty():
            return False

	ba = str(fileName.toLocal8Bit())

	f = open(ba, "w")

        for t in self.Tabs:
            for k,j in t.WidList.items():
                s = k + ": "
                v = ""
                if j["Type"] == ManagerControl.TextBox:
                    v += str(j["Widget"].text().toLocal8Bit())
                elif j["Type"] == ManagerControl.TextCombox or j["Type"] == ManagerControl.Combox:
                    
                    
                    if k == "manager.modules.load_path" or k == "manager.modules.preload" or k == "manager.components.precreate" or k == "corba.endpoints":
                        for c in range(0, j["Widget"].count()):
                            v += str(j["Widget"].itemText(c).toLocal8Bit())
                            if c < j["Widget"].count()-1:
                                v += ","
                    else:
                        v += str(j["Widget"].currentText().toLocal8Bit())
                elif j["Type"] == ManagerControl.SpinBox or j["Type"] == ManagerControl.DoubleSpinBox:
                    v += str(j["Widget"].value())
                if v != "":
                    s += v + "\n"
                    f.write(s)



        fname = os.path.basename(ba)
        name, ext = os.path.splitext(fname)
        dname = os.path.dirname(os.path.relpath(ba))

        for c in self.mgrc.mgr.getComponents():
            s = "Category." + c.get_sdo_id() + ".config_file: " + c.get_sdo_id() + ".conf\n"
            f.write(s)
            if dname == "":
                path = ".\\"+c.get_sdo_id() + ".conf"
            else:
                path = dname+"\\"+c.get_sdo_id() + ".conf"
            f2 = open(path, "w")

            
            cstes = c.get_configuration().get_active_configuration_set()
            s = "configuration.active_config: " + cstes.id + "\n"
            f2.write(s)
            
            for l in c.get_configuration().get_configuration_sets():
                for d in l.configuration_data:
                    s = "conf." + l.id + "." + d.name + ": " + d.value.value() + "\n"
                    f2.write(s)

            oEC = c.get_owned_contexts()[0]
            rate = oEC.get_rate()
            s = "exec_cxt.periodic.rate: " + str(rate) + "\n"
            f2.write(s)

            #s = "exec_cxt.periodic.type: " + "" + "\n"
            f2.close()
                
            



	f.close()

	

	

    ##
    #初期化のスロット
    ##
    def newFile(self):
        if self.mgrc == None:
            self.mgrc = ManagerControl("")
            self.createTabs()

            
            """for c in self.mgrc.mgr.getComponents():
                print c.get_sdo_id()
                for l in c.get_configuration().get_configuration_sets():
                    print l.id
                    print l.description
                    #prop = OpenRTM_aist.SDOPackage.NVList
                    #OpenRTM_aist.toProperties(prop,l.configuration_data)
                    #print prop
                    for d in l.configuration_data:
                        print d.name
                        print d.value.value()"""
                
        else:
            self.mesBox(u"既にコンフィギュレーションファイルは開いています")


        

    def mesBox(self, mes):
        msgbox = QtGui.QMessageBox( self )
        msgbox.setText( mes )
        msgbox.setModal( True )
        ret = msgbox.exec_()
	
        

class ManagerControl:
    TextBox = 1
    Combox = 2
    TextCombox = 3
    SpinBox = 4
    DoubleSpinBox = 5
    def __init__(self, conf_filepath):
        self.conf_filepath = conf_filepath
        if conf_filepath == "":
            self.mgr = OpenRTM_aist.Manager.init(sys.argv)
        else:
            self.mgr = OpenRTM_aist.Manager.init([os.path.abspath(__file__), '-f', conf_filepath])

        self.mgr.activateManager()
        self.mgr.runManager(True)
        
        
        self.compList = {}

        
        self.SetParam()
        

        
        
    def SetParam(self):

        self.confNameList = [{"default":"localhost","type":ManagerControl.TextBox,"list":[],"name":"corba.nameservers","label":u"RTC等を登録するネームサーバ"},
                             {"default":"%h.host_cxt/%n.mgr","type":ManagerControl.TextBox,"list":[],"name":"naming.formats","label":u"RTCをネームサーバに登録する際のフォーマット"},
                             {"default":"NORMAL","type":ManagerControl.Combox,"list":["SILENT","ERROR","WARN","NORMAL","INFO","DEBUG","TRACE","VERBOSE","PARANOID"],"name":"logger.log_level","label":u"ログレベル"},
                              {"default":"1000","type":ManagerControl.SpinBox,"list":[],"name":"exec_cxt.periodic.rate","label":u"実行コンテキストの周期"},
                               {"default":"NO","type":ManagerControl.Combox,"list":["YES","NO"],"name":"manager.is_master","label":u"マスターマネージャにするかどうか？"},
                              {"default":"","type":ManagerControl.Combox,"list":[],"name":"manager.modules.load_path","label":u"モジュール探索パス"},
                             {"default":"","type":ManagerControl.Combox,"list":[],"name":"manager.modules.preload","label":u"あらかじめロードしておくモジュール"},
                              {"default":"","type":ManagerControl.Combox,"list":[],"name":"manager.components.precreate","label":u"スタート時に起動するコンポーネント名"},
                             {"default":"1.0","type":ManagerControl.TextBox,"list":[],"name":"config.version","label":u"バージョン"},
                              {"default":"manager","type":ManagerControl.TextBox,"list":[],"name":"manager.name","label":u"managerの名前"},
                              {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"manager.corba_servant","label":u"マネージャのCORBAサーバントを起動するか"},
                             {"default":"localhost:2810","type":ManagerControl.TextBox,"list":[],"name":"corba.master_manager","label":u"マスターマネージャのアドレスとポート番号"},
                             {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"manager.shutdown_on_nortcs","label":u"RTCが一つもなくなった場合にプロセスを終了させるかどうか(RTCの削除で判定)"},
                              {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"manager.shutdown_auto","label":u"RTCが一つもなくなった場合にプロセスを終了させるかどうか(時間で判定)"},
                             {"default":"","type":ManagerControl.TextCombox,"list":["C++","Python","Java"],"name":"manager.supported_languages","label":u"サポートする言語"},
                              {"default":"py","type":ManagerControl.TextBox,"list":[],"name":"manager.modules.Python.suffixes","label":u"RTCモジュールの拡張子"},
                             {"default":"rtcd_python","type":ManagerControl.TextBox,"list":[],"name":"manager.modules.Python.manager_cmd","label":u"マネージャプログラム名"},
                              {"default":"rtcprof_python","type":ManagerControl.TextBox,"list":[],"name":"manager.modules.Python.profile_cmd","label":u"プロファイル取得コマンド名"},
                             {"default":"","type":ManagerControl.TextBox,"list":[],"name":"corba.args","label":u"CORBAに与える引数"},
                              {"default":"","type":ManagerControl.TextBox,"list":[],"name":"corba.endpoint","label":u"エンドポイント"},
                             {"default":"","type":ManagerControl.TextCombox,"list":[],"name":"corba.endpoints","label":u"エンドポイント(複数)"},
                              {"default":"","type":ManagerControl.TextBox,"list":[],"name":"corba.nameservice.replace_endpoint","label":u"エンドポイントの置き換え"},
                             {"default":"corba","type":ManagerControl.Combox,"list":["corba"],"name":"naming.type","label":u"ネームサービスのタイプ"},
                              {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"naming.update.enable","label":u"RTC生成後ネームサーバーの起動をした場合に登録できるか"},
                             {"default":"10.0","type":ManagerControl.DoubleSpinBox,"list":[],"name":"naming.update.interval","label":u"ネームサーバの確認および再登録を行う周期"},
                              {"default":"NO","type":ManagerControl.Combox,"list":["YES","NO"],"name":"naming.update.rebind","label":u"すでに名前と参照が登録されているネームサーバ上で名前が削除されるなどした場合に再度登録を行う"},
                             {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"manager.modules.abs_path_allowed","label":u"モジュールを絶対パスで指定するか"},
                              {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"logger.enable","label":u"ロガーの有効化・無効化"},
                             #{"default":"./rtc%p.log","type":ManagerControl.TextBox,"list":[],"name":"logger.file_name","label":u"ログファイル名"},
                              {"default":"%b %d %H:%M:%S","type":ManagerControl.TextBox,"list":[],"name":"logger.date_format","label":u"ログに記載する日付・時刻のフォーマット"},
                             {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"timer.enable","label":u"タイマ機能の有効/無効"},
                              {"default":"0.1","type":ManagerControl.DoubleSpinBox,"list":[],"name":"timer.tick","label":u"タイマの精度"},
                             {"default":"PeriodicExecutionContext","type":ManagerControl.TextCombox,"list":["PeriodicExecutionContext","ExtTrigExecutionContext","OpenHRPExecutionContext","ArtExecutionContext","RTPreemptEC"],"name":"exec_cxt.periodic.type","label":u"実行コンテキストのタイプ"},
                            {"default":"YES","type":ManagerControl.Combox,"list":["YES","NO"],"name":"exec_cxt.periodic.gui","label":u"MultipleOrderedEC使用時にGUIを表示するか"},
                            {"default":"","type":ManagerControl.TextBox,"list":[],"name":"exec_cxt.periodic.filename","label":u"MultipleOrderedEC使用時に実行順序を設定してあるファイル名"}
                             ]
        self.confList = []

        
        self.prop = OpenRTM_aist.Manager.instance().getConfig()
        

        for n in self.confNameList:
            p = self.getParam(n["name"])
            self.confList.append({"default":n["default"],"type":n["type"],"list":n["list"],"name":n["name"],"label":n["label"],"value":p.split(",")})
            
        
        
        
        
        

    def getParam(self, name):
        param = self.getProperty(self.prop, name, "")
        p = [param]
        OpenRTM_aist.StringUtil.eraseBlank(p)
        return p[0]

    
        

    
        

    ##
    #rtc.confの設定を取得する関数
    ##
    def getProperty(self, prop, key, value):
        
        if  prop.findNode(key) != None:
            
            value = prop.getProperty(key)
        return value
    

    def getFunc(self, filename, filepath):
        try:
            sys.path.append(filepath[0])
            (file, pathname, description) = imp.find_module(filename, filepath)
            mod = imp.load_module(filename, file, pathname, description)
            func = getattr(mod,filename+"Init",None)

            return func
        except:
            return None
        
        


    def deleteComp(self, name):
        
        if self.compList.has_key(name):
            if len(self.compList[name]["compList"]) != 0:
                self.compList[name]["compList"][-1].exit()
                del self.compList[name]["compList"][-1]
            #if len(self.compList[name]["compList"]) == 0:
            #    del self.compList[name]

    def addComp(self, name, comp):
        
        if self.compList.has_key(name):
            self.compList[name]["compList"].append(comp)
                
        
    def createComp(self, filename, filepath):
        
            
        
        

        

        preLoadComp = None
        if self.compList.has_key(filename):
            func = self.compList[filename]["func"]
            preLoadComp = self.compList[filename]
            
        
                
                

        if preLoadComp == None:    
            func = self.getFunc(filename, filepath)
            if func == None:
                return False
            func(self.mgr)
            
        if func:
            
            self.comp = self.mgr.createComponent(filename)
            if not self.comp:
                return False
            if preLoadComp:
                preLoadComp["compList"].append(self.comp)
            else:
                self.compList[filename] = {"filename":filename,"filepath":filepath,"func":func,"compList":[self.comp]}
        else:
            return False

        return True
        
##
# @brief 
def main():
    #mgrc = ManagerControl("")
    
    
    app = QtGui.QApplication([""])
    mainWin = MainWindow()
    mainWin.show()
    app.exec_()
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    
    
    
    
    

    
    
    
if __name__ == "__main__":
    main()
