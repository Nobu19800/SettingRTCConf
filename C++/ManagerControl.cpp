
#include "ManagerControl.h"

#include <coil/File.h>
#include <QtWidgets>

PathList::PathList(std::string path)
{
	fname = coil::basename(path.c_str());
	std::vector<std::string> sl = coil::split(fname,".");
	name = sl[0];
	
	if(sl.size() > 1)
	{
		cxt = sl[1];
	}
	else
	{
		cxt = "";
	}
	QString refileName = QDir().relativeFilePath(path.c_str());
	std::string reba = refileName.toLocal8Bit();
	char* repath = const_cast<char*>(reba.c_str());
	dname = coil::dirname(repath);

	char* tmp_p = const_cast<char*>(path.c_str());
	QString inv_refileName = QDir(coil::dirname(tmp_p).c_str()).relativeFilePath(QDir().absolutePath());
	inv_rdir = inv_refileName.toLocal8Bit();
	
}

confName::confName(std::string def, UIList type, std::vector<std::string> list, std::string name, std::string label)
{
	
	m_def = def;
	m_type = type;
	m_list = list;
	/*std::cout << "name:" << name << std::endl;
	for(int i=0;i < list.size();i++)
	{
		std::cout << m_list[i] << std::endl;
	}*/
	m_name = name;
	m_label = label;
}

compParam::compParam(std::string filename, std::string filepath, RTCInitFunction func, std::vector<RTC::RtcBase *> compList)
{
	m_filename = filename;
	m_filepath = filepath;
	m_func = func;
	m_compList = compList;
}


ManagerControl::ManagerControl(std::string conf_filepath)
{
	int argc = 0;
	char** argv;
	if(conf_filepath == "")
	{
		argc = 0;
		argv = new char*[1];
		argv[0] = "SettingRTCConf.exe";
		mgr = RTC::Manager::init(1, argv);
	}
	else
	{
		argc = 3;
		argv = new char*[3];
		argv[0] = "SettingRTCConf.exe";
		argv[1] = "-f";
		coil::replaceString(conf_filepath, "/", "\\");
		argv[2] = const_cast<char*>(conf_filepath.c_str());
		//std::cout << argv[1] << std::endl;
		mgr = RTC::Manager::init(3, argv);
	}

	mgr->init(argc, (char**)argv);

	mgr->activateManager();

	mgr->runManager(true);

	//createComp("CapturePresentation","CapturePresentation");
	//createComp("CapturePresentation","CapturePresentation");

	SetParam();
}

ManagerControl::~ManagerControl()
{
	for(int i=0;i < dllList.size();i++)
	{
		dllList[i]->close();
	}
}

compParam *ManagerControl::getCompFromName(std::string name)
{
	for(int i=0;i < compList.size();i++)
	{
		
		if(compList[i].m_filename == name)
		{
			return &compList[i];
		}
	}
	return NULL;
}

void ManagerControl::deleteComp(std::string name)
{
	
	compParam *c = getCompFromName(name);
	
	if(c)
	{
		if(c->m_compList.size() != 0)
		{
			c->m_compList[c->m_compList.size()-1]->exit();
			c->m_compList.pop_back();
		}
		
	}
		
}

void ManagerControl::addComp(std::string name,RTC::RtcBase * comp)
{
	compParam *c = getCompFromName(name);
	if(c)
	{
		c->m_compList.push_back(comp);
	}
}

bool ManagerControl::createComp(std::string filename,std::string filepath)
{
	//RTCInitFunction InInitFunc = getFunc(filename, filepath);

	RTCInitFunction InInitFunc = NULL;
	compParam *preLoadComp = getCompFromName(filename);
	if(preLoadComp)
	{
		InInitFunc = preLoadComp->m_func;
		
	}

	if(preLoadComp == NULL)
	{
		InInitFunc = getFunc(filename, filepath);
		if(InInitFunc == NULL)
		{
			return false;
		}
		InInitFunc(mgr);
	}

	if(InInitFunc)
	{
		
		RTC::RtcBase *comp = mgr->createComponent(filename.c_str());
		if(!comp)
			return false;
		

		if(preLoadComp)
		{
			preLoadComp->m_compList.push_back(comp);
			
		}
		else
		{
			std::vector<RTC::RtcBase *> rl;
			rl.push_back(comp);
			
			compList.push_back(compParam(filename, filepath, InInitFunc, rl));
		}
		return true;
	}
	else
	{
		return false;
	}
	return false;
	
}

std::vector<std::string> ManagerControl::convertList(int num,...)
{
	std::vector<std::string> ans;

	if(num == 0)
		return ans;

	
	va_list args;

	
	

	va_start(args, num);

	for(int i=0;i < num;i++)
	{
		//std::cout << i << std::endl;
		ans.push_back(va_arg(args, char*));
		
		//ans.push_back(va_arg(args, char*));
		//std::cout << i << "\t" << ans[ans.size()-1] << std::endl;
	}

	va_end(args);

	

	return ans;

}

void ManagerControl::SetParam()
{

	
	
	confList.push_back(confName("localhost",TextBox,convertList(0),"corba.nameservers","RTC等を登録するネームサーバ"));
     confList.push_back(confName("%h.host_cxt/%n.mgr",TextBox,convertList(0),"naming.formats","RTCをネームサーバに登録する際のフォーマット"));
     confList.push_back(confName("NORMAL",Combox,convertList(9,"SILENT","ERROR","WARN","NORMAL","INFO","DEBUG","TRACE","VERBOSE","PARANOID"),"logger.log_level","ログレベル"));
      confList.push_back(confName("1000",SpinBox,convertList(0),"exec_cxt.periodic.rate","実行コンテキストの周期"));
       confList.push_back(confName("NO",Combox,convertList(2,"YES","NO"),"manager.is_master","マスターマネージャにするかどうか？"));
      confList.push_back(confName("",Combox,convertList(0),"manager.modules.load_path","モジュール探索パス"));
     confList.push_back(confName("",Combox,convertList(0),"manager.modules.preload","あらかじめロードしておくモジュール"));
      confList.push_back(confName("",Combox,convertList(0),"manager.components.precreate","スタート時に起動するコンポーネント名"));
     confList.push_back(confName("1.0",TextBox,convertList(0),"config.version","バージョン"));
      confList.push_back(confName("manager",TextBox,convertList(0),"manager.name","managerの名前"));
      confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"manager.corba_servant","マネージャのCORBAサーバントを起動するか"));
     confList.push_back(confName("localhost:2810",TextBox,convertList(0),"corba.master_manager","マスターマネージャのアドレスとポート番号"));
     confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"manager.shutdown_on_nortcs","RTCが一つもなくなった場合にプロセスを終了させるかどうか(RTCの削除で判定)"));
      confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"manager.shutdown_auto","RTCが一つもなくなった場合にプロセスを終了させるかどうか(時間で判定)"));
     confList.push_back(confName("",TextCombox,convertList(3,"C++","Python","Java"),"manager.supported_languages","サポートする言語"));
      confList.push_back(confName("dll",TextBox,convertList(0),"manager.modules.C++.suffixes","RTCモジュールの拡張子"));
     confList.push_back(confName("rtcd",TextBox,convertList(0),"manager.modules.C++.manager_cmd","マネージャプログラム名"));
      confList.push_back(confName("rtcprof",TextBox,convertList(0),"manager.modules.C++.profile_cmd","プロファイル取得コマンド名"));
     confList.push_back(confName("",TextBox,convertList(0),"corba.args","CORBAに与える引数"));
      confList.push_back(confName("",TextBox,convertList(0),"corba.endpoint","エンドポイント"));
     confList.push_back(confName("",TextCombox,convertList(0),"corba.endpoints","エンドポイント(複数)"));
      confList.push_back(confName("",TextBox,convertList(0),"corba.nameservice.replace_endpoint","エンドポイントの置き換え"));
     confList.push_back(confName("corba",Combox,convertList(1,"corba"),"naming.type","ネームサービスのタイプ"));
      confList.push_back(confName("YES",Combox,convertList(1,"YES","NO"),"naming.update.enable","RTC生成後ネームサーバーの起動をした場合に登録できるか"));
     confList.push_back(confName("10.0",DoubleSpinBox,convertList(0),"naming.update.interval","ネームサーバの確認および再登録を行う周期"));
      confList.push_back(confName("NO",Combox,convertList(2,"YES","NO"),"naming.update.rebind","すでに名前と参照が登録されているネームサーバ上で名前が削除されるなどした場合に再度登録を行う"));
     confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"manager.modules.abs_path_allowed","モジュールを絶対パスで指定するか"));
      confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"logger.enable","ロガーの有効化・無効化"));
      confList.push_back(confName("%b %d %H:%M:%S",TextBox,convertList(0),"logger.date_format","ログに記載する日付・時刻のフォーマット"));
     confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"timer.enable","タイマ機能の有効/無効"));
      confList.push_back(confName("0.1",DoubleSpinBox,convertList(0),"timer.tick","タイマの精度"));
     confList.push_back(confName("PeriodicExecutionContext",TextCombox,convertList(5,"PeriodicExecutionContext","ExtTrigExecutionContext","OpenHRPExecutionContext","ArtExecutionContext","RTPreemptEC"),"exec_cxt.periodic.type","実行コンテキストのタイプ"));
    confList.push_back(confName("YES",Combox,convertList(2,"YES","NO"),"exec_cxt.periodic.gui","MultipleOrderedEC使用時にGUIを表示するか"));
    confList.push_back(confName("",TextBox,convertList(0),"exec_cxt.periodic.filename","MultipleOrderedEC使用時に実行順序を設定してあるファイル名"));
	
	for(int i=0;i < confList.size();i++)
	{
		std::string p = getParam(confList[i].m_name);
		confList[i].m_value = coil::split(p,",");
		/*for(int j=0;j < confList[i].m_value.size();j++)
		{
			std::cout << confList[i].m_value[j] << std::endl;
		}*/
	}

}

std::string ManagerControl::getParam(std::string name)
{
	coil::Properties& prop(::RTC::Manager::instance().getConfig());
	std::string param = "";
	getProperty(prop, name.c_str(), param);
	coil::eraseBlank(param);
	return param;
}

RTCInitFunction ManagerControl::getFunc(std::string filename,std::string filepath)
{
	char szFullPath[MAX_PATH];
	_fullpath(szFullPath, filepath.c_str(), sizeof(szFullPath)/sizeof(szFullPath[0]));
	std::string path = "PATH=";
	path += getenv("PATH");
	path += ";";
	path += szFullPath;
	putenv(path.c_str());
	//std::cout << getenv("PATH") << std::endl;

	std::string fn = filename + ".dll";
	//wchar_t *wfn = new wchar_t[fn.length() + 1];
	//mbstowcs(wfn, fn.c_str(), fn.length() + 1);

	//std::wstring ws = coil::string2wstring(fn);
	
	//HMODULE hInDll = LoadLibrary( ws.c_str() );
	coil::DynamicLib *dl = new coil::DynamicLib();

	//delete wfn;


	
	//HMODULE hInDll = LoadLibrary( TEXT("CapturePresentation.dll") );
	/*if (hInDll == NULL) {
		
		return NULL;
	}
	dllList.push_back(hInDll);*/

	int ret = dl->open(fn.c_str());
	if (ret != 0) {
		
		return NULL;
	}
	dllList.push_back(dl);


	std::string fun = filename + "Init";
	
	
	//RTCInitFunction InInitFunc = (RTCInitFunction)GetProcAddress(hInDll,(fun.c_str()));
	RTCInitFunction InInitFunc = (RTCInitFunction)RTCInitFunction(dl->symbol(fun.c_str()));
	
	return InInitFunc;
}

