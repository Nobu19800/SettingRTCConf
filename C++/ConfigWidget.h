#ifndef ConfigWidget_H
#define ConfigWidget_H

#include <QWidget>
#include "MTabWidget.h"

class ConfigWidget : public MTabWidget {
	Q_OBJECT
private:

public:
	ConfigWidget(ManagerControl *mgrc, QWidget *parent);
protected:

public slots:

};

#endif
