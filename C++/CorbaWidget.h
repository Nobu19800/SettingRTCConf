#ifndef CorbaWidget_H
#define CorbaWidget_H

#include <QWidget>
#include "MTabWidget.h"

class CorbaWidget : public MTabWidget {
	Q_OBJECT
private:

public:
	CorbaWidget(ManagerControl *mgrc, QWidget *parent);
protected:

public slots:
	void addEndpointsSlot();
	void delEndpointsSlot();

};

#endif
