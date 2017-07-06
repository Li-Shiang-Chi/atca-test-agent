#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import time
import data_dir
import shell_server
import mmsh
import os
import TA_error
import msg_socket
import cmd
	
def OS_is_running(ip,parser):
	"""
	use ping to check host os is running
	:param ip : FTOS ip
	:param parser : parser: is a dict, get from Test config file
	"""
	if("pre_wait_node_os_shutdown_time" in parser.keys()):
		time.sleep(float(parser["pre_wait_node_os_shutdown_time"]))
	return __OS_is_ping(ip ,parser)

def __OS_is_ping(ip , parser):
	"""
	use ping to check host os is running
	:param ip : FTOS ip
	:param parser : parser: is a dict, get from Test config file
	"""
	t_start = time.time()
	while ( (time.time() - t_start) < float(parser["pre_wait_node_boot_time"])) :
		response = os.system("ping -c 1 %s >/dev/null" % ip)
		print "ping %s" % ip
		if response == 0:
			return True;
		time.sleep(float(1))
	return False

def IPMI_OS_is_running(ipmb ,parser):
	t_start = time.time()
	while ( (time.time() - t_start) < float(parser["pre_wait_node_boot_time"])) :
		status = IPMI_get_power_status(ipmb)
		print status
		if status == "ON":
			return True;
		time.sleep(float(1))
	return False


def ssh_is_ready(ip,user,pwd,parser):
	"""
	use netcat check ssh port (22) is open
	and check the ssh daemon is running
	:param ip : FTOS ip
	:param user : FTOS user
	:param pwd : FTOS user password
	:param parser : parser: is a dict, get from Test config file
	"""
	
	if __ssh_port_is_ready(ip, parser) :
		if __ssh_daemon_is_running(ip, user, pwd, parser):
			return True
	return False
		
	

def __ssh_port_is_ready(ip , parser):
	"""
	use netcat check ssh port (22) is open
	and check the ssh daemon is running
	:param ip : FTOS ip
	:param parser : parser: is a dict, get from Test config file
	"""
	t_start = time.time()
	while((time.time() - t_start) < float(parser["pre_wait_ssh_port_time"])):
		response = os.system("nc -z %s 22 >/dev/null" % ip)
		#print "check %s ssh" % ip
		#print "response %s" % response
		if response == 0:
			return True
		time.sleep(float(1))
	return False

def __ssh_daemon_is_running(ip,user,pwd,parser):
	"""
	use ssh log in to the shell , check ssh is ready
	:param ip : FTOS ip
	:param user : FTOS user
	:param pwd : FTOS user password
	:param parser : parser: is a dict, get from Test config file
	"""
	t_start = time.time()
	while((time.time() - t_start) < float(parser["pre_wait_ssh_ready_time"])):
		time.sleep(float(1))
		try:
			ssh = shell_server.get_ssh(ip
                                  , user
                                  , pwd) #獲得ssh 
		except Exception:
			#print " checking %s ssh " % user
			continue
		ssh.close()
		return True
	try:	
		ssh = shell_server.get_ssh(ip , user , pwd) #獲得ssh
	except Exception:
		print " %s ssh not ready" % user
		return False; 
	ssh.close()
	
def reset_pid(node , parser):
	__reset_pid(node , parser)
	
def __reset_pid(node , parser):
	if node == "primary":
		ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
							, parser["PrimaryOS_usr"]
							, parser["PrimaryOS_pwd"]) #獲得ssh
		ssh.exec_command("sudo rm /home/primary/Desktop/pid.txt")
	elif node == "backup":
		ssh = shell_server.get_ssh(parser["BackupOS_ip"]
							, parser["BackupOS_usr"]
							, parser["BackupOS_pwd"]) #獲得ssh
		ssh.exec_command("sudo rm /home/backup-node/Desktop/pid.txt")
	elif node == "slave":
		ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
							, parser["SlaveOS_usr"]
							, parser["SlaveOS_pwd"]) #獲得ssh
		ssh.exec_command("sudo rm /home/slave/Desktop/pid.txt")
	ssh.close()
	
def reboot(ssh):
	cmd = "reboot"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)	
	ssh.close()

def IPMI_get_power_status(ipmb):
	cmd = " ipmitool -t 0x%s picmg power get 0 0" % ipmb
	
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
							, parser["SlaveOS_usr"]
							, parser["SlaveOS_pwd"]) #獲得ssh
	
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)	
	
	for line in s_stdout:
		if "Actual Power Level" in line:
			power = line.split(":")[1];
			power = power.strip()
			if power == "1":
				return "ON"
			elif power == "0":
				return "OFF"

def get_OS_status(OS_name):
	"""
	get OS status

	status : running / shutdown / initializing
	:param os_name: host OS name
	:return status : running / shutdown / initializing
	"""
	return mmsh.statehost(OS_name).rstrip()

def is_running(OS_name):
	"""
	ask OS is running or not

	:param os_name: host OS name
	:return: True (if OS is running)/False (if OS isn't running)
	"""
	if get_OS_status(OS_name) == "running":
		return True
	return False

def is_shutdown(OS_name):
	"""
	ask OS is running or not

	:param os_name: host OS name
	:return: True (if OS is shutdown)/False (if OS isn't shutdown)ATCA
	"""
	if get_OS_status(OS_name) == "shutdown":
		return True
	return False

def boot(OS_name):
	"""
	boot OS

	:param os_name: host OS name
	:return: success / [nothing]
	"""
	return mmsh.starthost(OS_name)

def shutdown(OS_name):
	"""
	shutdown OS

	:param os_name: host OS name
	:return: success / [nothing]
	"""
	return mmsh.stophost(OS_name)


def L1_boot(Network_adaptor_phy_address):
	"""
	boot L1 OS

	:param os_name: Network adaptor Physical address
	:return: success / [nothing]
	"""
	cmd = "wakeonlan %s" %  Network_adaptor_phy_address
	print cmd
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	#print error
	
def IPMI_boot(ipmb , ssh):
	
	cmd = "sudo ipmitool -t 0x%s picmg policy set 0 1 0" % ipmb
	print cmd
	ssh.exec_command(cmd)
	ssh.close()

def is_login(host_name, ip, port, time=60):
	"""
	host is login or not

	:param host_name: host name
	:param ip:host's  ip
	:param time: socket open time
	return True (if host is login)/False(else)
	"""
	import datetime
	import time as t
	sock = msg_socket.Msg_socket(ip, port, time) #設定socket
	sock.open() #開啟socket
	#print sock.msg
	if (host_name+" login") == sock.msg: 
		st = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
                #print "[%s][FTVM] VM %s:%s is logged in." % (st, vm_name, ip)
		return True
	return False
if __name__ == "__main__":
	parser = {}
	parser["pre_hostOS_boot_time"] = "200"
	parser["PrimaryOS_ip"] = "192.168.1.100"
	parser["SlaveOS_ip"] = "192.168.1.28"
	parser["SlaveOS_usr"] = "slave"
	parser["SlaveOS_pwd"] = "root"
	IPMI_get_power_status(86)
	#HostOSIsRunning(parser)