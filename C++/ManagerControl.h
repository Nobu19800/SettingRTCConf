#ifndef ManagerControl_H
#define ManagerControl_H

#include <vector>

#include <rtm/RTC.h>
#include <rtm/Manager.h>
#include <rtm/DataFlowComponentBase.h>
#include <coil/DynamicLib.h>

class PathList
{
public:
	PathList(std::string path);
	std::string fname;
	std::string name;
	std::string cxt;
	std::string dname;
	std::string inv_rdir;
};



typedef void (*RTCInitFunction)(RTC::Manager* pManager);

enum UIList{TextBox,Combox,TextCombox,SpinBox,DoubleSpinBox};

class confName
{
public:
	confName(std::string def, UIList type, std::vector<std::string> list, std::string name, std::string label);
	std::string m_def;
	UIList m_type;
	std::vector<std::string> m_list;
	std::string m_name;
	std::string m_label;
	std::vector<std::string> m_value;
};

class compParam
{
public:
	compParam(std::string filename, std::string filepath, RTCInitFunction func, std::vector<RTC::RtcBase *> compList);
	std::string m_filename;
	std::string m_filepath;
	RTCInitFunction m_func;
	std::vector<RTC::RtcBase *> m_compList;
};



class ManagerControl
{
public:
	ManagerControl(std::string conf_filepath);
	~ManagerControl();
	void deleteComp(std::string name);
	void addComp(std::string name,RTC::RtcBase *comp);
	bool createComp(std::string filename,std::string filepath);
	std::string conf_filepath;
	RTC::Manager* mgr;

	std::vector<coil::DynamicLib*> dllList;
	compParam *getCompFromName(std::string name);
	std::vector<confName> confList;
	std::vector<compParam> compList;

private:
	void SetParam();
	std::vector<std::string> convertList(int num,...);
	std::string getParam(std::string name);
	template <class T>
    void getProperty(coil::Properties& prop, const char* key, T& value)
    {
    if (prop.findNode(key) != 0)
      {
        T tmp;
        if (coil::stringTo(tmp, prop[key].c_str()))
          {
            value = tmp;
          }
      }
    }
	RTCInitFunction getFunc(std::string filename,std::string filepath);
	
	
	
	

};

#endif