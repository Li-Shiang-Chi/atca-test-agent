#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import time
import socket
import data_dir
import shell_server
import cmd_virsh
import msg_socket
import HAagent
import cmd_HAagent

def get_vm_status(vm_name, ip="", ssh=None):
	"""
	check vm check vm status

	:param vm_name: vm name
	:param ip:vm's  ip
	:return: status (running/paused/shut off)
	"""
	cmd = cmd_virsh.domstate_cmd(vm_name, ip) #獲得virsh domstate指令字串
	if ssh:
		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
		stdout = s_stdout.read()
		return stdout.rstrip()
	else:
		status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate() #執行指令
		#print status.rstrip()
		#print "error :",error
		return status.rstrip()

def is_running(vm_name, ip="", ssh=None):
	"""
	VM is running or not

	:param vm_name: vm name
	:param ip:vm's  ip
	:return: True(if VM is running)/False(else)
	"""
	status = ""
	if ssh:
		status = get_vm_status(vm_name, ip ,ssh)
	else:
		status = get_vm_status(vm_name, ip)

	print status
	if status == "running":
		return True
	return False

def is_shutoff(vm_name, ip="", ssh=None):
	"""
	VM is shutoff or not

	:param vm_name: vm name
	:param ip:vm's  ip
	:return: True(if VM is shut off)/False(else)
	"""
	status = ""
	if ssh:
		status = get_vm_status(vm_name, ip ,ssh)
	else:
		status = get_vm_status(vm_name, ip)
	if status == "shut off":
		return True
	return False

def is_paused(vm_name, ip="", ssh=None):
	"""
	VM is paused or not

	:param vm_name: vm name
	:param ip:vm's  ip
	:return: True(if VM is paused)/False(else)
	"""
	status = ""
	if ssh:
		status = get_vm_status(vm_name, ip ,ssh)
	else:
		status = get_vm_status(vm_name, ip)
	if status == "paused":
		return True
	return False

def is_login(vm_name, ip, port, time=60):
	"""
	VM is login or not

	:param vm_name: vm name
	:param ip:vm's  ip
	:param time: socket open time
	return True (if VM is login)/False(else)
	"""
	import datetime
	import time as t
	sock = msg_socket.Msg_socket(ip, port, time) #設定socket
	sock.open() #開啟socket
	print sock.msg
	if (vm_name+" login") == sock.msg: 
		st = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
                #print "[%s][FTVM] VM %s:%s is logged in." % (st, vm_name, ip)
		return True
	return False


def start(vm_name, ip="", ssh=None):
	"""
	use libvirt
	start vm, when vm status is shutoff 

	:param vm_name: vm name
	:param ip:vm's ip
	"""
	if is_shutoff(vm_name, ip, ssh):
		cmd = cmd_virsh.start_cmd(vm_name, ip) #獲得virsh start之指令字串
		if ssh:
			s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
			print cmd
			stdout = s_stdout.read()
			#return stdout.rstrip()
		else:
			subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令

def ftstart(node_name ,vm_name, ip="", ssh=None):
	"""
	use HAagent
	ftstart vm, when vm status is shutoff

	:param vm_name: vm name
	:param ip: vm's ip
	"""
	if is_shutoff(vm_name,ip, ssh):
		cmd = cmd_HAagent.start_ftvm_cmd(node_name, vm_name)
		if ssh:
			print "HAAgent is running %s" % HAagent.is_running(ssh)
			print cmd
			return HAagent.start_ftvm(node_name, vm_name, None, None, ssh)
		else:
			return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
		
def duplicate_ftstart(node_name ,vm_name, ip="", ssh=None):
	if is_running(vm_name,ip, ssh):
		cmd = cmd_HAagent.start_ftvm_cmd(node_name, vm_name)
		if ssh:
			return HAagent.start_ftvm(node_name, vm_name, None, None, ssh)
		else:
			return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
def shutdown(vm_name, ip="", ssh=None):
	"""
	shutdown vm, when vm status is running

	:param vm_name: vm name
	:param ip: vm's ip
	"""
	import datetime
	if is_running(vm_name, ip, ssh):
		#st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		cmd = cmd_virsh.shutdown_cmd(vm_name, ip) #獲得virsh shutdown之指令字串
		print cmd
		if ssh:
			s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
			stdout = s_stdout.read()
			print stdout
			return stdout
			#return stdout.rstrip()
		else:
			subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
			
def ftshutdown(vm_name , ip="" , ssh=None):
	"""
	use HAagent shutdown vm, when vm status is running

	:param vm_name: vm name
	:param ip: vm's ip
	"""
	
	if is_running(vm_name, ip, ssh):
		cmd = cmd_HAagent.remove_ftvm_cmd(vm_name)
		print cmd
		if ssh:
			return HAagent.remove_ftvm(vm_name, None, ssh)
		else:
			return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
			
			
def destroy(vm_name , ip="" , ssh=None):
	"""
	destroy vm, when vm status is running

	:param vm_name: vm name
	:param ip: vm's ip
	"""
	if is_running(vm_name, ip, ssh):
		cmd = cmd_virsh.destroy_cmd(vm_name, ip)
		print cmd
		if ssh:
			s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
			stdout = s_stdout.read()
			print stdout
			return stdout
		else:
			return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
			
def ftdestroy(vm_name , ip="" , ssh=None):
	if is_running(vm_name, ip, ssh):
		if ssh:
			return HAagent.remove_ftvm(vm_name, None, ssh)
		else:
			return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
def resume(vm_name, ip="", ssh=None):
	"""
	resume vm, when vm status is paused

	:param vm_name: vm name
	:param ip: vm's ip
	"""
	if is_paused(vm_name, ip, ssh):
		cmd = cmd_virsh.resume_cmd(vm_name, ip) #獲得virsh resume之指令字串
		if ssh:
			s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
			stdout = s_stdout.read()
			#return stdout.rstrip()
		else:
			subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令

def restart(vm_name, ip="", ssh=None):
	"""
	restart vm

	:param vm_name: vm name
	:param ip: vm's ip
	"""
	destroy(vm_name, ip, ssh) #讓vm關機
	t_begin = time.time()
	while time.time() < (t_begin+100):
		time.sleep(1)
		#print time.time()-t_begin
		if is_shutoff(vm_name, ip) == True: #若VM之狀態為shut off 則進入
			time.sleep(1)
			#print "in"
			start(vm_name, ip, ssh) #VM開機
			break

def ftrestart(vm_name, ip="", level="1", ssh=None):
	"""
	ftrestart vm

	:param vm_name: vm name
	:param ip: vm's ip
	:param level: fault tolerance level
	"""
	destroy(vm_name, ip, ssh) #讓vm關機
	t_begin = time.time()
	while time.time() < (t_begin+100):
		time.sleep(1)
		if is_shutoff(vm_name, ip) == True: #若VM之狀態為shut off 則進入
			time.sleep(1)
			ftstart(vm_name, ip, level, ssh) #VM採取開啟容錯功能支開機
			break

def get_pid(vm_name, ip, ssh):
	"""
	get vm process id in OS

	:param vm_name: vm name
	:param ip: vm's ip
	:param ssh: ssh object
	:return: pid/False(get no pid)
	"""
	pid_file_path = data_dir.VM_PID_DIR+vm_name+".pid" #獲得VM.pid的路徑
	cmd = "sudo cat %s" % pid_file_path #組合cat指令
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #執行指令
	pid = s_stdout.read()
	if pid != "":
		return int(pid)
	return False

	




if __name__ == '__main__':
	"""
	if get_vm_status("VM1", "140.115.53.42") != "running":
		start("VM1", "140.115.53.42")
	get_vm_status("VM1", "140.115.53.42")
	"""
	print "start"
	#print "start"
	#if get_vm_status("VM1", "140.115.53.42") == "running":
		#print "in"
	#ssh = shell_server.get_ssh("192.168.1.27"
	#                   , "user"
	#                    , "pdclab!@#$") #獲得ssh
	ssh = shell_server.get_ssh("192.168.1.102"
    						, "slave"
    						, "root") #獲得ssh
	print get_vm_status("test-daemon12", "192.168.1.100")
	print get_vm_status("test-daemon12", "192.168.1.100") == "shut off"
	destroy("test-daemon12", "192.168.1.102",ssh)
	#print is_shutoff("VM1", "140.115.53.42")
	#shutdown("VM01", "140.115.53.127")
	#shutdown("VM1", "140.115.53.42")
	#ssh = shell_server.get_ssh("140.115.53.42", "ting", "oolabting")
	#print get_pid("VM1", "140.115.53.42", ssh)
