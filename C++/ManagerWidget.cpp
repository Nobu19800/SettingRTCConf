#include "ManagerWidget.h"




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

ManagerWidget::ManagerWidget(ManagerControl *mgrc, QWidget *parent) : MTabWidget(mgrc, parent)
{
	setGUI("manager");

	QPushButton *addLangButton = new QPushButton(tc->toUnicode("サポートする言語の追加"));
	getWidgetFromName("manager.supported_languages")->m_layout->addWidget(addLangButton);
	connect(addLangButton, SIGNAL(clicked()), this, SLOT(addLangSlot()));

	QPushButton *delLangButton = new QPushButton(tc->toUnicode("サポートする言語の削除"));
	getWidgetFromName("manager.supported_languages")->m_layout->addWidget(delLangButton);
	connect(delLangButton, SIGNAL(clicked()), this, SLOT(delLangSlot()));

	QPushButton *createCompButton = new QPushButton(tc->toUnicode("RTC起動"));
	getWidgetFromName("manager.components.precreate")->m_layout->addWidget(createCompButton);
	connect(createCompButton, SIGNAL(clicked()), this, SLOT(createCompSlot()));

	QPushButton *delCompButton = new QPushButton(tc->toUnicode("RTC終了"));
	getWidgetFromName("manager.components.precreate")->m_layout->addWidget(delCompButton);
	connect(delCompButton, SIGNAL(clicked()), this, SLOT(delCompSlot()));

	QPushButton *delModuleButton = new QPushButton(tc->toUnicode("モジュール削除"));
	getWidgetFromName("manager.modules.preload")->m_layout->addWidget(delModuleButton);
	connect(delModuleButton, SIGNAL(clicked()), this, SLOT(delModuleSlot()));

	QPushButton *delPathButton = new QPushButton(tc->toUnicode("パス削除"));
	getWidgetFromName("manager.modules.load_path")->m_layout->addWidget(delPathButton);
	connect(delPathButton, SIGNAL(clicked()), this, SLOT(delPathSlot()));

	QPushButton *loadRTCButton = new QPushButton(tc->toUnicode("RTコンポーネントをファイルから読み込み"));
	subLayouts[subLayouts.size()-1]->addWidget(loadRTCButton);
	connect(loadRTCButton, SIGNAL(clicked()), this, SLOT(loadRTCSlot()));


}

void ManagerWidget::addLangSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.supported_languages")->m_widget);

	if(wid)
	{
		if(wid->findText(wid->currentText()) == -1)
		{
			std::string s = wid->currentText().toLocal8Bit();
			if(s != "")
			{
				wid->addItem(wid->currentText());
			}
		}
	}
}

void ManagerWidget::delLangSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.supported_languages")->m_widget);
	if(wid)
		wid->removeItem(wid->findText(wid->currentText()));
}

void ManagerWidget::createCompSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.components.precreate")->m_widget);
	if(wid)
	{
		std::string s = wid->currentText().toLocal8Bit();
		RTC::RtcBase *comp = m_mgrc->mgr->createComponent(s.c_str());
		if(!comp)
		{
				mesBox("RTCの起動に失敗しました");
				return;
		}
		wid->addItem(wid->currentText());
		m_mgrc->addComp(s, comp);
	}
}

void ManagerWidget::delCompSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.components.precreate")->m_widget);
	if(wid)
	{
		std::string s = wid->currentText().toLocal8Bit();
	
		m_mgrc->deleteComp(s);
		wid->removeItem(wid->findText(wid->currentText()));
	}
}

void ManagerWidget::delModuleSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.modules.preload")->m_widget);
	if(wid)
		wid->removeItem(wid->findText(wid->currentText()));
}

void ManagerWidget::delPathSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.modules.load_path")->m_widget);
	if(wid)
		wid->removeItem(wid->findText(wid->currentText()));

}

void ManagerWidget::loadRTCSlot()
{
	QString fileName = QFileDialog::getOpenFileName(this,
							tc->toUnicode("開く"), "",
							tr("Dynamic Link Library (*.dll);;Dynamic Link Library (*.so);;All Files (*)"));
	if (fileName.isEmpty())
        return;

	
	std::string ba = fileName.toLocal8Bit();
	
	//char* path = const_cast<char*>(ba.c_str());
	
	PathList p = PathList(ba);

	
	
	/*std::cout << ba << std::endl;
	std::cout << fname << std::endl;
	std::cout << name << std::endl;
	std::cout << cxt << std::endl;
	std::cout << dname << std::endl;*/

	if(m_mgrc->createComp(p.name, p.dname) == false)
	{
		mesBox("モジュールの読み込みに失敗しました");
		return;
	}

	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.components.precreate")->m_widget);
	if(wid)
		wid->addItem(tc->toUnicode(p.name.c_str()));


	wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.modules.preload")->m_widget);
	if(wid)
	{
		if(wid->findText(tc->toUnicode(p.fname.c_str())) == -1)
		{
			wid->addItem(tc->toUnicode(p.fname.c_str()));
		}
	}


	wid = dynamic_cast<QComboBox *>(getWidgetFromName("manager.modules.load_path")->m_widget);
	
	if(wid)
	{
		if(p.dname == "")
			p.dname = "./" + p.dname;
		if(wid->findText(tc->toUnicode(p.dname.c_str())) == -1)
		{
		
		
			wid->addItem(tc->toUnicode(p.dname.c_str()));
		}

	}
}

