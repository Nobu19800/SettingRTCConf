#include "MTabWidget.h"

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

PWidget::PWidget(std::string name, QWidget *widget, QVBoxLayout *layout)
{
	
	m_name = name;
	m_widget = widget;
	m_layout = layout;
}

MTabWidget::MTabWidget(ManagerControl *mgrc, QWidget *parent) : QWidget(parent)
{
	tc = QTextCodec::codecForLocale();
	m_mgrc = mgrc;

	mainLayout = new QHBoxLayout();
	setLayout(mainLayout);

	subLayouts.push_back(new QVBoxLayout());
	mainLayout->addLayout(subLayouts[subLayouts.size()-1]);
}

PWidget* MTabWidget::getWidgetFromName(std::string name)
{
	for(int i=0;i < WidList.size();i++)
	{
		if(WidList[i]->m_name == name)
		{
			return WidList[i];
		}
	}
	return NULL;
}

PWidget* MTabWidget::apendWidget(QWidget *wid, std::string name, std::string label)
{
	QWidget *widget = new QWidget();
	QVBoxLayout *layout = new QVBoxLayout();
	widget->setLayout(layout);
	QLabel *Lb = new QLabel(tc->toUnicode(label.c_str()));

	layout->addWidget(Lb);
	layout->addWidget(wid);
	PWidget *pw = new PWidget(name, wid, layout);
	WidList.push_back(pw);
	if(WidList.size()%7 == 0)
	{
		subLayouts.push_back(new QVBoxLayout());
		mainLayout->addLayout(subLayouts[subLayouts.size()-1]);
	}

	subLayouts[subLayouts.size()-1]->addWidget(widget);
	subLayouts[subLayouts.size()-1]->addStretch();

	return pw;

}

PWidget* MTabWidget::addCombox(std::string name, std::string label, std::vector<std::string> value, std::vector<std::string> ls, std::string def)
{
	QComboBox *wid = new QComboBox();

	for(int i=0;i < ls.size();i++)
	{
		if(ls[i] != "")
		{
			wid->addItem(tc->toUnicode(ls[i].c_str()));
		}
	}

	if(name == "manager.modules.load_path" || name == "manager.modules.preload" || name == "manager.components.precreate" || name == "corba.endpoints")
	{
		for(int i=0;i < value.size();i++)
		{
			if(value[i] != "")
			{
				wid->addItem(tc->toUnicode(value[i].c_str()));
			}
		}
	}

	if(value.size() != 0)
	{
		if(value[0] != "")
		{
			wid->setCurrentIndex(wid->findText(tc->toUnicode(value[0].c_str())));
		}
		else
		{
			wid->setCurrentIndex(wid->findText(tc->toUnicode(def.c_str())));
		}
	}
	else
	{
		wid->setCurrentIndex(wid->findText(tc->toUnicode(def.c_str())));
	}

	PWidget *wl = apendWidget(wid, name, label);
	wl->m_type = Combox;

	return wl;
}

PWidget* MTabWidget::addTextCombox(std::string name, std::string label, std::vector<std::string> value, std::vector<std::string> ls, std::string def)
{
	PWidget *wl = addCombox(name, label, value, ls, def);
	QComboBox *wid = dynamic_cast<QComboBox *>(wl->m_widget);
	if(wid)
	{
		wid->setLineEdit(new QLineEdit());
		if(value.size() == 0)
		{
			wid->lineEdit()->setText(tc->toUnicode(def.c_str()));
		}
		else if(value[0] == "")
		{
			wid->lineEdit()->setText(tc->toUnicode(def.c_str()));
		}
		else
		{
			wid->lineEdit()->setText(tc->toUnicode(value[0].c_str()));
		}

	}
	else
	{
		return NULL;
	}

	wl->m_type = TextCombox;

	return wl;
	
}

PWidget* MTabWidget::addSpinBox(std::string name, std::string label, std::vector<std::string> value, std::string def)
{
	QSpinBox *wid = new QSpinBox();

	int val;
	coil::stringTo<int>(val, def.c_str());

	if(value.size() == 0)
	{
		
		wid->setValue(val);
	}
	else if(value[0] == "")
	{
		wid->setValue(val);
	}
	else
	{
		coil::stringTo<int>(val, value[0].c_str());
		wid->setValue(val);
	}

	PWidget *wl = apendWidget(wid, name, label);
	wl->m_type = SpinBox;

	return wl;

}

PWidget* MTabWidget::addDoubleSpinBox(std::string name, std::string label, std::vector<std::string> value, std::string def)
{
	QDoubleSpinBox *wid = new QDoubleSpinBox();

	double val;
	coil::stringTo<double>(val, def.c_str());

	if(value.size() == 0)
	{
		
		wid->setValue(val);
	}
	else if(value[0] == "")
	{
		wid->setValue(val);
	}
	else
	{
		coil::stringTo<double>(val, value[0].c_str());
		wid->setValue(val);
	}

	PWidget *wl = apendWidget(wid, name, label);
	wl->m_type = SpinBox;

	return wl;
}

PWidget* MTabWidget::addTextBox(std::string name, std::string label, std::vector<std::string> value, std::string def)
{
	QLineEdit *wid = new QLineEdit();

	if(value.size() == 0)
	{
		
		wid->setText(tc->toUnicode(def.c_str()));
	}
	else if(value[0] == "")
	{
		wid->setText(tc->toUnicode(def.c_str()));
	}
	else
	{
		wid->setText(tc->toUnicode(value[0].c_str()));
	}

	PWidget *wl = apendWidget(wid, name, label);
	wl->m_type = TextBox;

	return wl;

}

void MTabWidget::setGUI(std::string tabName)
{
	for(int i=0;i < m_mgrc->confList.size();i++)
	{
		std::string name = coil::split(m_mgrc->confList[i].m_name,".")[0];

		if(name == tabName)
		{
			if(m_mgrc->confList[i].m_type == Combox)
			{
				addCombox(m_mgrc->confList[i].m_name,m_mgrc->confList[i].m_label,m_mgrc->confList[i].m_value,m_mgrc->confList[i].m_list,m_mgrc->confList[i].m_def);
			}
			else if(m_mgrc->confList[i].m_type == TextCombox)
			{
				addTextCombox(m_mgrc->confList[i].m_name,m_mgrc->confList[i].m_label,m_mgrc->confList[i].m_value,m_mgrc->confList[i].m_list,m_mgrc->confList[i].m_def);
			}
			else if(m_mgrc->confList[i].m_type == SpinBox)
			{
				addSpinBox(m_mgrc->confList[i].m_name,m_mgrc->confList[i].m_label,m_mgrc->confList[i].m_value,m_mgrc->confList[i].m_def);
			}
			else if(m_mgrc->confList[i].m_type == DoubleSpinBox)
			{
				addDoubleSpinBox(m_mgrc->confList[i].m_name,m_mgrc->confList[i].m_label,m_mgrc->confList[i].m_value,m_mgrc->confList[i].m_def);
			}
			else if(m_mgrc->confList[i].m_type == TextBox)
			{
				addTextBox(m_mgrc->confList[i].m_name,m_mgrc->confList[i].m_label,m_mgrc->confList[i].m_value,m_mgrc->confList[i].m_def);
			}
		}
	}
}

void MTabWidget::mesBox(std::string mes)
{
	QMessageBox msgBox(this);
	msgBox.setText(tc->toUnicode(mes.c_str()));
	msgBox.exec();
}