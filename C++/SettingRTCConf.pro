TEMPLATE = vcapp
TARGET = SettingRTCConf
QT += widgets
QT += testlib

HEADERS	    =   MTabWidget.h \
		ManagerWidget.h \
		CorbaWidget.h \
		ConfigWidget.h \
		NamingWidget.h \
		LoggerWidget.h \
		TimerWidget.h \
		LoggerWidget.h \
		ExecCxtWidget.h \
		MainWindow.h \
		ManagerControl.h
SOURCES	    =   MTabWidget.cpp \
		ManagerWidget.cpp \
		CorbaWidget.cpp \
		ConfigWidget.cpp \
		NamingWidget.cpp \
		LoggerWidget.cpp \
		TimerWidget.cpp \
		LoggerWidget.cpp \
		ExecCxtWidget.cpp \
		MainWindow.cpp \
		ManagerControl.cpp \
		main.cpp
build_all:!build_pass {
    CONFIG -= build_all
    CONFIG += release
}

# install
sources.files = $$SOURCES $$HEADERS $$RESOURCES $$FORMS diagramscene.pro images
INSTALLS += target sources
