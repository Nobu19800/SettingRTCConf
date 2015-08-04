#!/bin/env python
# -*- encoding: utf-8 -*-

import rtctree.tree
import sys
import os


def main():

  cpath = []
  file_name = ""
  mode = False
  for c in range(0, len(sys.argv)):
    #print sys.argv[c]
    if mode:
      cpath.append(sys.argv[c])
      
    if sys.argv[c] == "-f":
      c += 1
      file_name = sys.argv[c]
      mode = False
    elif sys.argv[c] == "-c":
      mode = True

  if file_name == "":
    print u"ファイル名を入力してください"
    return
  
  if len(cpath) < 2:
    print u"RTCのパスを入力してください"
    return
  
  tree = rtctree.tree.RTCTree(servers=cpath[0])
  l = ["/"]
  for i in cpath:
    l.append(i)
  comp = tree.get_node(l)

  if comp == None:
    print u"RTCが見つかりませんでした"
  #print l,comp.object.get_sdo_id()
  c = comp.object
  

  fname = os.path.basename(file_name)
  name, ext = os.path.splitext(fname)
  dname = os.path.dirname(os.path.relpath(file_name))


  f = open(file_name, "a")
  
  
  s = c.get_sdo_id() + ".conf"

  f2 = open(dname+s, "w")
  
  
  s = c.get_component_profile().category + "." + c.get_sdo_id() + ".config_file: " + c.get_sdo_id() + ".conf\n"
  f.write(s)
  cstes = c.get_configuration().get_active_configuration_set()
  s = "configuration.active_config: " + cstes.id + "\n"
  f2.write(s)

  for l in c.get_configuration().get_configuration_sets():
      for d in l.configuration_data:
          s = "conf." + l.id + "." + d.name + ": " + d.value.value() + "\n"
          f2.write(s)

  oEC = c.get_owned_contexts()[0]
  rate = oEC.get_rate()
  s = "exec_cxt.periodic.rate: " + str(rate) + "\n"
  f2.write(s)

  f.close()
  f2.close()

  return

if __name__ == "__main__":
  main()
