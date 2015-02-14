#include <stdio.h>
#include <QApplication>

#include "MainWindow.h"

int main(int argc,char *argv[])
{
	QApplication *app = new QApplication(argc, argv);
	MainWindow *mw = new MainWindow();
	mw->show();
	app->exec();

	return 0;
}