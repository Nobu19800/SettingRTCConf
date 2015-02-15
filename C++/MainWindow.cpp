
#include <QLabel>
#include <QtWidgets>
#include <rtm/CorbaNaming.h>
#include <rtm/CorbaConsumer.h>

#include "MainWindow.h"


MainWindow::MainWindow()
{
	tc = QTextCodec::codecForLocale();

	tab_widget = new QTabWidget(this);
	setCentralWidget(tab_widget);

	createAction();
	createMenus();

	mgrc = NULL;
	//mgrc = new ManagerControl("");
	//createTabs();

}

void MainWindow::open()
{
	

	if(mgrc == NULL)
	{
		QString fileName = QFileDialog::getOpenFileName(this,
								tc->toUnicode("開く"), "",
								tr("Config File (*.conf);;All Files (*)"));
		if (fileName.isEmpty())
			return;

		std::string ba = fileName.toLocal8Bit();
		mgrc = new ManagerControl(ba);
		createTabs();
	}
	else
	{
		mesBox("既にコンフィギュレーションファイルは開いています");
	}
}

void MainWindow::save()
{
	QString fileName = QFileDialog::getSaveFileName(this,
							tc->toUnicode("保存"), "",
							tr("Config File (*.conf);;All Files (*)"));
	if (fileName.isEmpty())
        return;

	std::string ba = fileName.toLocal8Bit();
	std::ofstream ofs( ba );

	for(int i=0;i < Tabs.size();i++)
	{
		for(int j=0;j < Tabs[i]->WidList.size();j++)
		{
			std::string s = Tabs[i]->WidList[j]->m_name;
			s += ": ";
			std::string v = "";
			if(Tabs[i]->WidList[j]->m_type == TextBox)
			{
				QLineEdit *c = dynamic_cast<QLineEdit *>(Tabs[i]->WidList[j]->m_widget);
				if(c)
				{
					v += c->text().toLocal8Bit();
				}
			}
			else if(Tabs[i]->WidList[j]->m_type == TextCombox || Tabs[i]->WidList[j]->m_type == Combox)
			{
				QComboBox *c = dynamic_cast<QComboBox *>(Tabs[i]->WidList[j]->m_widget);
				if(c)
				{
					if(Tabs[i]->WidList[j]->m_name == "manager.modules.load_path" || Tabs[i]->WidList[j]->m_name == "manager.modules.preload" || Tabs[i]->WidList[j]->m_name == "manager.components.precreate" || Tabs[i]->WidList[j]->m_name == "corba.endpoints")
					{
					
						for(int k = 0;k < c->count();k++)
						{
							v += c->itemText(k).toLocal8Bit();
							if(k < c->count()-1)
							{
								v += ",";
							}
						}
					}
					else
					{
						v += c->currentText().toLocal8Bit();
					}
				}
				
			}
			else if(Tabs[i]->WidList[j]->m_type == SpinBox || Tabs[i]->WidList[j]->m_type == DoubleSpinBox)
			{
				QSpinBox *c = dynamic_cast<QSpinBox *>(Tabs[i]->WidList[j]->m_widget);
				if(c)
				{
					v += coil::otos<int>(c->value());
				}
				else
				{
					QDoubleSpinBox *cd = dynamic_cast<QDoubleSpinBox *>(Tabs[i]->WidList[j]->m_widget);
					if(cd)
					{
						v += coil::otos<double>(cd->value());
					}
				}
			}

			if(v != "")
			{
				s += v;
				ofs << s << std::endl;
			}
			
		}
	}

	PathList p = PathList(ba);

	std::string tpt = p.dname;
	tpt += "/";
	tpt += p.name;
	tpt += ".bat";
	std::ofstream pf( tpt );

	pf << "cd " << p.inv_rdir << std::endl;
	pf << "rtcd -f " << p.dname << "/" << p.name << "." << p.cxt << std::endl;
	pf.close();

	std::vector<RTC::RtcBase*> bl = mgrc->mgr->getComponents();
	for(int i=0;i < bl.size();i++)
	{
		

		std::string path;

		if(p.dname == "")
		{
			path = "./";
			path += bl[i]->get_sdo_id();
			path += ".conf";
		}
		else
		{
			path = p.dname;
			path += "/";
			path += bl[i]->get_sdo_id();
			path += ".conf";
		}

		std::ofstream ofs2( path );


		std::string s = bl[i]->getCategory();
		s += ".";
		s += bl[i]->get_sdo_id();
		s += ".config_file: ";
		s += path;


		ofs << s << std::endl;



		SDOPackage::ConfigurationSet* cstes = bl[i]->get_configuration()->get_active_configuration_set();
		s = "configuration.active_config: ";
		s += cstes->id;
		
		ofs2 << s << std::endl;

		SDOPackage::ConfigurationSetList* cl = bl[i]->get_configuration()->get_configuration_sets();
		
		//SDOPackage::Configuration_ptr cl = bl[i]->get_configuration();
		//cl->get_configuration_sets;
		//RTC::Properties properties;
		
		//std::vector<std::string> nl = properties.propertyNames();

		for(int j=0;j < cl->length();j++)
		{
			//std::cout << cl->length() << std::endl;
			//RTC::CorbaConsumer<SDOPackage::ConfigurationSet> cs;
			//SDOPackage::ConfigurationSetList_var clist;
			//cs.setObject(clist[j]);

			
			SDOPackage::ConfigurationSet l = cl->get_buffer()[j];
			//SDOPackage::NVList d = l.configuration_data;
			RTC::Properties properties;
			NVUtil::copyToProperties(properties, l.configuration_data);
			std::vector<std::string> kl = properties.propertyNames();
			for(int k=0;k < kl.size();k++)
			{
				
				s = "conf.";
				s += l.id;
				s += ".";
				s += kl[k];
				s += ": ";
				s += properties.getProperty(kl[k]);

				ofs2 << s << std::endl;
				//std::cout << properties.getProperty(kl[k]) << std::endl;
			}
			//properties[0].c_str();
			/*for(int k=0;k < d.length();k++)
			{
				

				NVUtil::copyToProperties(properties, confSet->configuration_data);

				//CORBA::Char* tmp;
				//CORBA::Any an_any = d.get_buffer()[k].value;
				//an_any <<= tmp;
				//if(an_any >>= tmp)
				//s += CORBA::Any::to_string(d.get_buffer()[k].value);
				

				ofs2 << s << std::endl;
			}*/
		}
		RTC::CorbaConsumer<RTC::ExecutionContext> ec0;
		RTC::ExecutionContextList_var ecs = bl[i]->get_owned_contexts();
		ec0.setObject(ecs[0]);
		double rate = ec0->get_rate();

		s = "exec_cxt.periodic.rate: ";
		s += coil::otos<double>(rate);
		s += "\n";

		ofs2 << s << std::endl;
		
		
		
	}

	ofs.close();
	
	


}

void MainWindow::newFile()
{
	if(mgrc == NULL)
	{
		mgrc = new ManagerControl("");
		createTabs();
	}
	else
	{
		mesBox("既にコンフィギュレーションファイルは開いています");
	}
}

void MainWindow::createAction()
{
	newAct = new QAction(tr("&New..."),this);
	newAct->setShortcuts(QKeySequence::New);
    connect(newAct, SIGNAL(triggered()), this, SLOT(newFile()));


	openAct = new QAction(tr("&Open..."),this);
    openAct->setShortcuts(QKeySequence::Open);
    connect(openAct, SIGNAL(triggered()), this, SLOT(open()));


    saveAct = new QAction(tr("&Save"),this);
    saveAct->setShortcuts(QKeySequence::Save);
    connect(saveAct, SIGNAL(triggered()), this, SLOT(save()));

	
}

void MainWindow::createMenus()
{
	fileMenu = menuBar()->addMenu(tr("&File"));
	fileMenu->addAction(newAct);
    fileMenu->addAction(openAct);
    fileMenu->addAction(saveAct);
}

void MainWindow::createTabs()
{
	ManagerWidget *ManagerTab = new ManagerWidget(mgrc, this);
	tab_widget->addTab(ManagerTab, tc->toUnicode("マネージャ"));
	Tabs.push_back(ManagerTab);
	CorbaWidget *CorbaTab = new CorbaWidget(mgrc, this);
	tab_widget->addTab(CorbaTab, tc->toUnicode("CORBA"));
	Tabs.push_back(CorbaTab);
	ConfigWidget *ConfigTab = new ConfigWidget(mgrc, this);
	tab_widget->addTab(ConfigTab, tc->toUnicode("一般的"));
	Tabs.push_back(ConfigTab);
	NamingWidget *NamingTab = new NamingWidget(mgrc, this);
	tab_widget->addTab(NamingTab, tc->toUnicode("ネームサービス"));
	Tabs.push_back(NamingTab);
	LoggerWidget *LoggerTab = new LoggerWidget(mgrc, this);
	tab_widget->addTab(LoggerTab, tc->toUnicode("ロガー"));
	Tabs.push_back(LoggerTab);
	TimerWidget *TimerTab = new TimerWidget(mgrc, this);
	tab_widget->addTab(TimerTab, tc->toUnicode("タイマ"));
	Tabs.push_back(TimerTab);
	ExecCxtWidget *ExecCxtTab = new ExecCxtWidget(mgrc, ManagerTab, this);
	tab_widget->addTab(ExecCxtTab, tc->toUnicode("実行コンテキスト"));
	Tabs.push_back(ExecCxtTab);
}

void MainWindow::mesBox(std::string mes)
{
	QMessageBox msgBox(this);
	msgBox.setText(tc->toUnicode(mes.c_str()));
	msgBox.exec();
}
