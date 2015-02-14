#ifndef MTabWidget_H
#define MTabWidget_H

#include <vector>
#include <QWidget>
#include <QLayout>
#include "ManagerControl.h"

class PWidget
{
public:
	PWidget(std::string name, QWidget *widget, QVBoxLayout *layout);
	std::string m_name;
	QWidget *m_widget;
	QVBoxLayout *m_layout;
	UIList m_type;
};

class MTabWidget : public QWidget {
	Q_OBJECT


public:
	MTabWidget(ManagerControl *mgrc, QWidget *parent);
	QHBoxLayout *mainLayout;
	std::vector<PWidget*> WidList;
	std::vector<QVBoxLayout*> subLayouts;
	PWidget* getWidgetFromName(std::string name);
	void mesBox(std::string mes);
	void setGUI(std::string tabName);
	QTextCodec* tc;
	ManagerControl *m_mgrc;
protected:

public slots:

private:
	
	

	PWidget* apendWidget(QWidget *wid, std::string name, std::string label);
	PWidget* addCombox(std::string name, std::string label, std::vector<std::string> value, std::vector<std::string> ls, std::string def);
	PWidget* addTextCombox(std::string name, std::string label, std::vector<std::string> value, std::vector<std::string> ls, std::string def);
	PWidget* addSpinBox(std::string name, std::string label, std::vector<std::string> value, std::string def);
	PWidget* addDoubleSpinBox(std::string name, std::string label, std::vector<std::string> value, std::string def);
	PWidget* addTextBox(std::string name, std::string label, std::vector<std::string> value, std::string def);
	


	
};

#endif
