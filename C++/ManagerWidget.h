#ifndef ManagerWidget_H
#define ManagerWidget_H

#include <QWidget>
#include "MTabWidget.h"



class ManagerWidget : public MTabWidget {
	Q_OBJECT
private:

public:
	ManagerWidget(ManagerControl *mgrc, QWidget *parent);
protected:

public slots:
	void addLangSlot();
	void delLangSlot();
	void createCompSlot();
	void delCompSlot();
	void delModuleSlot();
	void delPathSlot();
	void loadRTCSlot();


};

#endif
