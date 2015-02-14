#ifndef LoggerWidget_H
#define LoggerWidget_H

#include <QWidget>
#include "MTabWidget.h"

class LoggerWidget : public MTabWidget {
	Q_OBJECT
private:

public:
	LoggerWidget(ManagerControl *mgrc, QWidget *parent);
protected:

public slots:

};

#endif
