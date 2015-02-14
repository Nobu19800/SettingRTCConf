#include "ExecCxtWidget.h"

//#include <coil/File.h>

#include <QAction>
#include <QLayout>
#include <QMenu>
#include <QMenuBar>
#include <QStatusBar>
#include <QTextEdit>
#include <QFile>
#include <QDataStream>
#include <QFileDialog>
#include <QMessageBox>
#include <QSignalMapper>
#include <QApplication>
#include <QPainter>
#include <QMouseEvent>
#include <QLineEdit>
#include <QComboBox>
#include <QLabel>
#include <QPushButton>
#include <qdebug.h>
#include <QtWidgets>

ExecCxtWidget::ExecCxtWidget(ManagerControl *mgrc, ManagerWidget *mgrWidget, QWidget *parent) : MTabWidget(mgrc, parent)
{

	m_mgrWidget = mgrWidget;
	setGUI("exec_cxt");

	QPushButton *loadECButton = new QPushButton(tc->toUnicode("実行コンテキスト読み込み"));
	subLayouts[subLayouts.size()-1]->addWidget(loadECButton);
	connect(loadECButton, SIGNAL(clicked()), this, SLOT(loadECSlot()));

	QPushButton *setOrderFileButton = new QPushButton(tc->toUnicode("実行順序設定ファイルの読み込み"));
	getWidgetFromName("exec_cxt.periodic.filename")->m_layout->addWidget(setOrderFileButton);
	connect(setOrderFileButton, SIGNAL(clicked()), this, SLOT(setOrderFSlot()));
}

void ExecCxtWidget::loadECSlot()
{
	QString fileName = QFileDialog::getOpenFileName(this,
							tc->toUnicode("開く"), "",
							tr("Dynamic Link Library (*.dll);;Dynamic Link Library (*.so);;All Files (*)"));
	if (fileName.isEmpty())
        return;

	
	std::string ba = fileName.toLocal8Bit();
	
	PathList p = PathList(ba);


	

	QComboBox *wid = dynamic_cast<QComboBox *>(m_mgrWidget->getWidgetFromName("manager.modules.preload")->m_widget);
	if(wid)
	{
		if(wid->findText(tc->toUnicode(p.fname.c_str())) == -1)
		{
			wid->addItem(tc->toUnicode(p.fname.c_str()));
		}
	}
	wid = dynamic_cast<QComboBox *>(m_mgrWidget->getWidgetFromName("manager.modules.load_path")->m_widget);
	
	if(wid)
	{
		if(p.dname == "")
			p.dname = "./" + p.dname;
		if(wid->findText(tc->toUnicode(p.dname.c_str())) == -1)
		{
		
		
			wid->addItem(tc->toUnicode(p.dname.c_str()));
		}
	}

	wid = dynamic_cast<QComboBox *>(getWidgetFromName("exec_cxt.periodic.type")->m_widget);
	
	if(wid)
	{
		if(wid->findText(tc->toUnicode(p.name.c_str())) == -1)
		{
			wid->addItem(tc->toUnicode(p.name.c_str()));
		}
		wid->lineEdit()->setText(tc->toUnicode(p.name.c_str()));
	}
}

void ExecCxtWidget::setOrderFSlot()
{
	QString fileName = QFileDialog::getOpenFileName(this,
							tc->toUnicode("開く"), "",
							tr("Lua File (*.lua);;Configuration File (*.conf);;All Files (*)"));
	if (fileName.isEmpty())
        return;

	QString refileName = QDir().relativeFilePath(fileName);
	std::string ba = refileName.toLocal8Bit();
	QLineEdit *wid = dynamic_cast<QLineEdit *>(getWidgetFromName("exec_cxt.periodic.filename")->m_widget);
	
	wid->setText(tc->toUnicode(ba.c_str()));
}