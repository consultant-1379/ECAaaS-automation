#!/bin/env python2.7
from jumpssh import SSHSession
import jump_box_list
import json

#Define class attributes and methods
class jump_box:
    def __init__(self,ipaddress,username,password,datacenter):
        self.ip = ipaddress
        self.user = username
        self.password = password
        self.dc = datacenter

    @staticmethod
    def free_and_used_mem(mem_line):
        line_fields = mem_line.split()
        total_mem = line_fields[1]
        used_mem = line_fields[2]
        free_mem = line_fields[3]
        shared_mem = line_fields[4]
        buffers_mem = line_fields[5]
        cached_mem = line_fields[6]
        return used_mem,free_mem,total_mem,shared_mem,buffers_mem,cached_mem

#Function to connect to remote servers through a jumpbox and excute commands
    def excute_command(self,cmd):

        for object in jump_box_list.ip_list:
            final_result = {}
            vnf_name = object["name"]
            if object["ip"] == self.ip:

              for IP in object["list_of_reachable_ips"]:
                try:
                  jumpbox_session = SSHSession(self.ip, username=self.user, password=self.password).open()
  
                  #check if it's a standalone VM or jumpbox to other VMs inside /etc/hosts
                  if IP == "127.0.0.1":
                      host_name = str(jumpbox_session.get_cmd_output('hostname'))
                      cmd_result = str(jumpbox_session.get_cmd_output(cmd))
                  else:
                      remote_session = jumpbox_session.get_remote_session(IP, password=self.password)
                      host_name = str(remote_session.get_cmd_output('hostname'))
                      cmd_result = str(remote_session.get_cmd_output(cmd))
  
                  #remote_session = jumpbox_session.get_remote_session(IP, password=self.password)
                  #host_name = str(remote_session.get_cmd_output('hostname'))
  
  
  
  
                  host_name_lines = host_name.splitlines()
                  if host_name_lines[0] == "Failed to retrieve unit: Access denied":
                      host_name = vnf_name+"-"+str(host_name_lines[1])
                  else:
                      host_name = vnf_name+"-"+str(host_name_lines[0])
  
                  #cmd_result = str(remote_session.get_cmd_output(cmd))
                  cmd_lines = cmd_result.splitlines()
                  if cmd_lines[0] == "Failed to retrieve unit: Access denied":
                      used_mem,free_mem,total_mem,shared_mem,buffers_mem,cached_mem = jump_box.free_and_used_mem(cmd_lines[2])
  
                  else:
                      used_mem,free_mem,total_mem,shared_mem,buffers_mem,cached_mem = jump_box.free_and_used_mem(cmd_lines[1])
                except Exception as e:
                    continue

                machine_stats = {}
                machine_stats["total_mem"] = str(total_mem)
                machine_stats["used_mem"] = str(used_mem)
                machine_stats["free_mem"] = str(free_mem)
                machine_stats["shared_mem"] = str(shared_mem)
                machine_stats["buffers_mem"] = str(buffers_mem)
                machine_stats["cached_mem"] = str(cached_mem)
                machine_stats["datacenter"] = self.dc
                final_result[host_name] = machine_stats
              return final_result

            else:
                continue

#Function to initialize instances from jump_box class
def class_instance(x, dc, y, z):
    vnf_node = jump_box(ipaddress=x,username=y,password=z,datacenter=dc)
    result = vnf_node.excute_command('free -m')
    if result == {}:
        pass
    else:
        return result


def get_all_vm_memory_metrics():
    metric_dict = {}
    for vnf in jump_box_list.ip_list:
        dc = vnf["datacenter"]
        user = vnf["username"]
        pwd = vnf["password"]
        vnf_metric = class_instance(vnf["ip"], dc, user, pwd)
        metric_dict[vnf["name"]] = vnf_metric

    return metric_dict

