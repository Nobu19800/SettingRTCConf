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


import SettingRTCConf


        
##
# @brief 
def main():
    #mgrc = ManagerControl("")
    
    
    app = QtGui.QApplication([""])
    mainWin = SettingRTCConf.MainWindow()
    mainWin.show()
    app.exec_()
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    
    
    
    
    

    
    
    
if __name__ == "__main__":
    main()
