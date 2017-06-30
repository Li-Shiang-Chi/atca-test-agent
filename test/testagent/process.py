#/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import data_dir
import FTsystem
import FTVM
import cmd_kill
import shell_server
import mmsh
import master_monitor
import time
import HAagent
import TA_error
import os
from testagent import cmd_HAagent
import cmd


def exec_high_temp_danger(parser):
	'''
	execute high temperature danger to primary node
	'''
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cmd = cmd_HAagent.high_temp_danger_cmd()
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()
	
def exec_low_temp_danger(parser):
	'''
	execute low temperature danger to primary node-
	'''
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cmd = cmd_HAagent.low_temp_danger_cmd()
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()
	
def exec_high_volt_danger(parser):
	'''
	execute high voltage to primary node
	'''
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cmd = cmd_HAagent.high_volt_danger_cmd()
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()
	
def exec_low_volt_danger(parser):
	'''
	execute low voltage danger to primary node
	'''
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cmd = cmd_HAagent.low_volt_danger_cmd()
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()
	
def exec_nodeOS_hang(parser):
	'''
	execute node OS hang to targer node
	'''
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	node = "node"
	cmd = cmd_HAagent.nodeOS_hang_cmd(node)
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()

def exec_L1_backupOS_network_isolation(parser):

	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	cmd = "sudo ifconfig %s down" % (parser["BackupOS_network_interface"])
	print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
		
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_primaryOS_network_isolation(parser):

	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	cmd = "sudo ifconfig %s down" % (parser["PrimaryOS_network_interface"])
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	
	ssh.close()

def exec_L1_slaveOS_shutdown(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["slaveOS_ip"]
                              , parser["slaveOS_usr"]
                              , parser["slaveOS_pwd"]) #獲得ssh
	cmd = "sudo poweroff -f" 
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_L1_backupOS_shutdown(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	cmd = "sudo poweroff -f" 
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_L1_hostOS_networkIsolation(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	cmd = "cd /home/user;sudo ./testif.sh;" 
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_primaryOS_shutdown(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	print 77
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	print 78
	cmd = "sudo shutdown -h now" 
	print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()
	print 79
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	print 80

def exec_backupOS_shutdown(parser):
	"""
	execute level 1 crasher in backupOS

	:param parser: is a dict, get from Test config file
	"""
	print 77
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	print 78
	cmd = "sudo shutdown -h now" 
	print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()
	print 79
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	print 80

def exec_L1_hostOS_crasher(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	cmd = "sudo "+cmd_kill.kill_cmd(1,11) #獲得kill -SIGSEGV 1之指令字串
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()
	"""
	#Another way to crash
	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"])
	f_path = parser["PrimaryOS_process_dir"]+"L1_crasher"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close()
	"""

def kill_vm_process(parser):
	"""
	kill vm process on hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_kill_vm_p" in parser.keys(): #若pro_wait_time_kill_vm_p存在於parser
		print "sleep"
		time.sleep(float(parser["pro_wait_time_kill_vm_p"]))
	#print "kill"

	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	pid = FTVM.get_pid(parser["vm_name"], parser["PrimaryOS_ip"], ssh) #獲得VM之pid
	print "vm pid %s" % pid
	cmd = cmd_kill.kill_cmd(pid, 9) #獲得kill vm process之指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	ssh.close()
	
def kill_backup_vm_process(parser):
	"""
	kill vm process on backupOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_kill_vm_p" in parser.keys(): #若pro_wait_time_kill_vm_p存在於parser
		time.sleep(int(parser["pro_wait_time_kill_vm_p"]))
	#print "kill"

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	pid = FTVM.get_pid(parser["vm_name"], parser["BackupOS_ip"], ssh) #獲得VM之pid
	cmd = cmd_kill.kill_cmd(pid, 9) #獲得kill vm process之指令字串
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	ssh.close()
	
def stop_libvirt_process(parser):
	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	FTsystem.stop(ssh)
	if FTsystem.get_status(ssh) == "running":
		raise TA_error.Process_Error("libvirt in host OS cannot stop")
	ssh.close()

def kill_libvirt_process(parser):
	"""
	kill libvirt process on hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_kill_libvirt_p" in parser.keys(): #若pro_wait_time_kill_libvirt_p存在於parser
		time.sleep(int(parser["pro_wait_time_kill_libvirt_p"]))

	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	pid = FTsystem.get_pid(ssh) #透過ssh獲得libvirt之pid
	if pid == False:
		ssh.close()
		raise TA_error.Process_Error("can not get libvirt pid")
	print "libvirt pid %s" % pid
	cmd = cmd_kill.kill_cmd(pid, 9) #獲得kill libvirt process之指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	ssh.close()
	
def kill_master_monitor_process(parser):
	"""
	kill master monitor process on hostOS

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	if "pro_wait_time_kill_mm_p" in parser.keys(): #若pro_wait_time_kill_mm_p存在於parser
		time.sleep(int(parser["pro_wait_time_kill_mm_p"]))
	
	pid = master_monitor.get_pid(ssh) #獲得master monitor之pid
	if pid == False:
		raise TA_error.Process_Error("can not get master monitor pid")
	print pid
	cmd = "sudo "+cmd_kill.kill_cmd(pid, 9) #獲得kill master monitor process之指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	#subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
	ssh.close()

def exec_primary_vm_guestOS_crasher(parser):
	"""
	execute level 1 crasher in vm 
	kill init process

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["GuestOS_ip_P"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
	cmd = "sudo "+cmd_kill.kill_cmd(1,11) #獲得kill -SIGSEGV 1之指令字串
	#print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()

def exec_backup_vm_guestOS_crasher(parser):
	"""
	execute level 1 crasher in vm 
	kill init process

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["GuestOS_ip_B"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
	cmd = "sudo "+cmd_kill.kill_cmd(1,11) #獲得kill -SIGSEGV 1之指令字串
	#print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()
	
def exec_slave_vm_guestOS_crasher(parser):
	"""
	execute level 1 crasher in vm 
	kill init process

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["GuestOS_ip_S"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
	cmd = "sudo "+cmd_kill.kill_cmd(1,11) #獲得kill -SIGSEGV 1之指令字串
	#print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()

def vm_start(parser):
	"""
	normaly start vm

	:param parser: is a dict, get from Test config file
	"""


	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	if "pro_wait_time_start" in parser.keys():
		time.sleep(int(parser["pro_wait_time_start"]))	

	FTVM.start(parser["vm_name"], parser["PrimaryOS_ip"],ssh)

	ssh.close()

def host_vm_ftstart(parser):
	"""
	ftstart vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	if "pro_wait_time_start" in parser.keys():
		time.sleep(int(parser["pro_wait_time_start"]))
	FTVM.ftstart(parser["PrimaryOS_name"],parser["vm_name"], parser["PrimaryOS_ip"],ssh) #執行開啟容錯機制之開機
	ssh.close()
def backup_vm_ftstart(parser):
	"""
	ftstart vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	if "pro_wait_time_start" in parser.keys():
		time.sleep(int(parser["pro_wait_time_start"]))
	
	FTVM.ftstart(parser["BackupOS_name"],parser["vm_name"], parser["BackupOS_ip"],ssh) #執行開啟容錯機制之開機
	ssh.close()
	
def slave_vm_ftstart(parser):
	"""
	ftstart vm

	:param parser: is a dict, get from Test config file
	"""
	
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh

	if "pro_wait_time_start" in parser.keys():
		time.sleep(int(parser["pro_wait_time_start"]))
	
	FTVM.ftstart(parser["SlaveOS_name"],parser["vm_name"], parser["BackupOS_ip"],ssh) #執行開啟容錯機制之開機
	ssh.close()

def host_vm_shutdown(parser):
	"""
	shutdown vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	if "pro_wait_time_shutdown" in parser.keys():
		time.sleep(int(parser["pro_wait_time_shutdown"]))
	
	FTVM.shutdown(parser["vm_name"], parser["PrimaryOS_ip"],ssh)
	ssh.close()
	
def host_vm_ftshutdown(parser):
	"""
	host ftshutdown vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	if "pro_wait_time_shutdown" in parser.keys():
		time.sleep(int(parser["pro_wait_time_shutdown"]))
	
	FTVM.ftshutdown(parser["vm_name"], parser["PrimaryOS_ip"],ssh)
	ssh.close()
	
def backup_vm_ftshutdown(parser):
	"""
	backup ftshutdown vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	if "pro_wait_time_shutdown" in parser.keys():
		time.sleep(int(parser["pro_wait_time_shutdown"]))
	
	FTVM.ftshutdown(parser["vm_name"], parser["BackupOS_ip"],ssh)
	ssh.close()
	
def slave_vm_ftshutdown(parser):
	"""
	slave ftshutdown vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	if "pro_wait_time_shutdown" in parser.keys():
		time.sleep(int(parser["pro_wait_time_shutdown"]))
	
	FTVM.ftshutdown(parser["vm_name"], parser["BackupOS_ip"],ssh)
	ssh.close()
	
	
def exec_create_cluster(parser):
	"""
	HAagent create cluster
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	ssh.close()

def exec_create_duplicate_cluster(parser):
	"""
	HAagent create duplicate cluster
	:param parser: is a dict, get from Test config file
	"""	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	ssh.close()

def exec_de_cluster(parser):
	"""
	HAagent delete cluster
	:param parser: is a dict, get from Test config file
	"""	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.de_cluster(parser["Cluster_name"], parser, ssh)
	ssh.close()

def exec_de_outer_cluster(parser):
	"""
	HAagent external cluster primary delete cluster
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster("test_c", parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.de_cluster("test_b", parser, ssh)
	ssh.close()
	
def exec_non_primary_de_cluster(parser):
	"""
	HAagent add node to cluster
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	# create cluster
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.add_backup_node(parser , ssh)
	time.sleep(float(1))
	ssh.close()
	
	#use backup node to decluster
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	HAagent.de_cluster(parser["Cluster_name"], parser, ssh)
	ssh.close()
	
def exec_add_node(parser):
	"""
	HAagnet add node (primary , backup , slave)
	:param parser: is a dict, get from Test config file
	"""	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	backup = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
		
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	time.sleep(float(parser["pro_wait_add_node_time"]))
	HAagent.add_backup_node(parser, ssh)
	time.sleep(float(parser["pro_wait_add_node_time"]))
	HAagent.add_slave_node(parser, ssh)
	time.sleep(float(parser["pro_wait_add_node_time"]))
	
	ssh.close()

def exec_non_primary_add_node(parser):
	"""
	HAagnet non primary add node to cluster
	:param parser: is a dict, get from Test config file
	"""	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	#use primary node create cluster
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.add_backup_node(parser, ssh)
	time.sleep(float(parser["pro_wait_add_node_time"]))
	#use backup node to add node
	backup = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	HAagent.add_node(parser["Cluster_name"], parser["SlaveOS_name"], parser["SlaveOS_ip"], parser["SlaveOS_ipmb"], parser, backup)
	backup.close()
	
	
def exec_add_duplicate_node(parser):
	"""
	HAagent add duplicate node to cluster
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh) 
	ssh.close()
	
def exec_add_outer_node(parser):
	"""
	HAagent add outer node to cluster
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	time.sleep(1)
	ssh.close()
	
def exec_de_node(parser):
	"""
	HAagent remove node in cluster
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	time.sleep(1)
	HAagent.rm_node(parser["Cluster_name"], parser["PrimaryOS_name"], parser, ssh)
	time.sleep(1)
	ssh.close()

def exec_non_primary_de_node(parser):
	"""
	use non-primary node remove node 
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	#use primary node create cluster
	HAagent.create_cluster(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.add_backup_node(parser, ssh)
	time.sleep(float(parser["pro_wait_add_node_time"]))
	#use backup node to remove node
	backup = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	HAagent.rm_node(parser["Cluster_name"], parser["PrimaryOS_name"], parser, backup)
	backup.close()
	
def exec_overview(parser):
	"""
	HAagent overview
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	#HAagent.quick_create_cluster(parser, ssh)
	time.sleep(1)
	ssh.close()
    
if __name__ == '__main__':
	parser = dict()
	parser["PrimaryOS_name"] = "primary"
	parser["PrimaryOS_ip"] = "192.168.1.100"
	parser["PrimaryOS_usr"] = "primary"
	parser["PrimaryOS_pwd"] = "root"
	parser["PrimaryOS_ipmb"] = "85"
	parser["Cluster_name"] = "test_c"
	parser["BackupOS_ip"] = "192.168.1.101"
	parser["BackupOS_name"] = "backup"
	parser["BackupOS_ipmb"] = "86"
	parser["Shelf_ip"] = "127.0.0.1"
	parser["pro_wait_add_node_time"] = "5"
	
	exec_primaryOS_shutdown(parser)
	
