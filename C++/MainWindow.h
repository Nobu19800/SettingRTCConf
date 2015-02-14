#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTextEdit>
#include <QtWidgets>

#include "ManagerControl.h"
#include "ConfigWidget.h"
#include "CorbaWidget.h"
#include "ExecCxtWidget.h"
#include "LoggerWidget.h"
#include "NamingWidget.h"
#include "TimerWidget.h"


class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
	MainWindow();

signals:
	
public slots:
	void open();
	void save();
	void newFile();

private:
	void createAction();
	void createMenus();
	void createTabs();
	void mesBox(std::string mes);

	ManagerControl *mgrc;
	QAction *newAct;
	QAction *openAct;
	QAction *saveAct;

	std::vector<MTabWidget*> Tabs;
	QTabWidget *tab_widget;
	QMenu *fileMenu;

	QTextCodec* tc;
	
	
	

private:

};

#endif