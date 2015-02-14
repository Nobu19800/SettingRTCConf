#include "CorbaWidget.h"

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

CorbaWidget::CorbaWidget(ManagerControl *mgrc, QWidget *parent) : MTabWidget(mgrc, parent)
{
	setGUI("corba");

	QPushButton *addEndpointsButton = new QPushButton(tc->toUnicode("エンドポイント追加"));
	getWidgetFromName("corba.endpoints")->m_layout->addWidget(addEndpointsButton);
	connect(addEndpointsButton, SIGNAL(clicked()), this, SLOT(addEndpointsSlot()));

	QPushButton *delEndpointsButton = new QPushButton(tc->toUnicode("エンドポイント削除"));
	getWidgetFromName("corba.endpoints")->m_layout->addWidget(delEndpointsButton);
	connect(delEndpointsButton, SIGNAL(clicked()), this, SLOT(delEndpointsSlot()));
	
}


void CorbaWidget::addEndpointsSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("corba.endpoints")->m_widget);

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

void CorbaWidget::delEndpointsSlot()
{
	QComboBox *wid = dynamic_cast<QComboBox *>(getWidgetFromName("corba.endpoints")->m_widget);
	if(wid)
		wid->removeItem(wid->findText(wid->currentText()));
}