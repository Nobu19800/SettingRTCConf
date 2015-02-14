#ifndef ExecCxtWidget_H
#define ExecCxtWidget_H

#include <QWidget>
#include "MTabWidget.h"
#include "ManagerWidget.h"

class ExecCxtWidget : public MTabWidget {
	Q_OBJECT

public:
	ExecCxtWidget(ManagerControl *mgrc, ManagerWidget *mgrWidget, QWidget *parent);
protected:

public slots:
	void loadECSlot();
	void setOrderFSlot();

private:
	ManagerWidget *m_mgrWidget;
};

#endif
