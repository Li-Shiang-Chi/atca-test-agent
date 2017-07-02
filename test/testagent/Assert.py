#/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import time
import subprocess
import shell_server
import FTVM
import FTsystem
import master_monitor
import mmsh
import TA_error
import HAagent_info
import HAagent
import HAagent_terminal
import cmd_HAagent
import FTOS

def backupOS_role_is_Slave_on_MasterOS(parser):
	"""
	detect backup OS role is slave on master host
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                      , parser["PrimaryOS_usr"]
                      , parser["PrimaryOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"], ssh)
	ssh.close()
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["PrimaryOS_name"])

def hostOS_role_is_Slave_on_BackupOS(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["PrimaryOS_name"], ssh)
	ssh.close()
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["PrimaryOS_name"])

def backupOS_role_is_Master_on_BackupOS(parser):

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"], ssh)
	ssh.close()
	if role == "master": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["PrimaryOS_name"])

def primaryOS_role_is_primary(parser):

	role = HAagent_info.get_node_role(parser["PrimaryOS_name"], parser)

	if role == "primary": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not primary" % parser["PrimaryOS_name"])

def primaryOS_role_is_backup(parser):
	role = HAagent_info.get_node_role(parser["PrimaryOS_name"], parser)

	if role == "backup": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not backup" % parser["PrimaryOS_name"])

def primaryOS_role_is_slave(parser):
	role = HAagent_info.get_node_role(parser["PrimaryOS_name"], parser)
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["PrimaryOS_name"])


def backupOS_role_is_primary(parser):
	
	role = HAagent_info.get_node_role(parser["BackupOS_name"], parser)
	
	
	if role == "primary": 
		return True
	raise TA_error.Assert_Error("backup (name : %s) role is not primary" % parser["BackupOS_name"])


def backupOS_role_is_backup(parser):
	
	role = HAagent_info.get_node_role(parser["BackupOS_name"], parser)

	if role == "backup": 
		return True
	raise TA_error.Assert_Error("backup (name : %s) role is not backup" % parser["BackupOS_name"])

def backupOS_role_is_slave(parser):

	role = HAagent_info.get_node_role(parser["BackupOS_name"], parser)

	if role == "slave": 
		return True
	raise TA_error.Assert_Error("backup (name : %s) role is not primary" % parser["BackupOS_name"])

def slaveOS_role_is_primary(parser):

	role = HAagent_info.get_node_role(parser["SlaveOS_name"], parser)

	if role == "primary": 
		return True
	raise TA_error.Assert_Error("slave (name : %s) role is not primary" % parser["SlaveOS_name"])

def slaveOS_role_is_backup(parser):

	role = HAagent_info.get_node_role(parser["SlaveOS_name"], parser)
	if role == "backup": 
		return True
	raise TA_error.Assert_Error("slave (name : %s) role is not backup" % parser["SlaveOS_name"])

def slaveOS_role_is_slave(parser):

	role = HAagent_info.get_node_role(parser["SlaveOS_name"], parser)

	if role == "slave": 
		return True
	raise TA_error.Assert_Error("slave (name : %s) role is not slave" % parser["SlaveOS_name"])



def detect_primaryOS_crash(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                          , parser["BackupOS_usr"]
                          , parser["BackupOS_pwd"]) #獲得ssh
	if mmsh.statehost(parser["PrimaryOS_name"], ssh) == "shutdown": #若回傳之狀態是hardware shutdown，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("Host (name : %s) has not detect host os crash " % parser["PrimaryOS_name"])
	
	

def detect_backupOS_crash(parser):
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                          , parser["PrimaryOS_usr"]
                          , parser["PrimaryOS_pwd"]) #獲得ssh

	if mmsh.statehost(parser["BackupOS_name"], ssh) == "shutdown": #若回傳之狀態是hardware shutdown，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("Host (name : %s) has not detect host os crash " % parser["BackupOS_name"])

def hostOS_status_is_M4(parser):
	"""
	host hardware status is M4 or not

	M4 means hardware ok
	:param parser: config 
	:return: True/raise: exception
	"""
	if "ast_hostOS_running_wait_time" in parser.keys(): #若參數ast_hostOS_running_wait_time存在於parser，則進入
		time.sleep(int(parser["ast_hostOS_running_wait_time"]))
	#print mmsh.stateipmc(parser["PrimaryOS_name"])
	if mmsh.stateipmc(parser["PrimaryOS_name"]) == "M4": #若回傳之狀態是M4，則該test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("Host (name : %s) hardware status is not M4" % parser["PrimaryOS_name"])

#---
def hostOS_status_is_running(parser):
	"""
	hostOS status is running or not
	:param parser: config 
	:return: True/raise exception
	"""
	if "ast_hostOS_running_wait_time" in parser.keys(): #若參數ast_hostOS_running_wait_time存在於parser，則進入
		time.sleep(int(parser["ast_hostOS_running_wait_time"]))
	#print mmsh.statehost(parser["PrimaryOS_name"])
	if mmsh.statehost(parser["PrimaryOS_name"]) == "running": #若回傳之狀態是running，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("Host (name : %s) status is not running" % parser["PrimaryOS_name"])


def vm_recover_in_primaryOS(parser):
	vm_running_in_hostOS(parser)
	vm_is_login_in_hostOS(parser)

def vm_recover_in_backupOS(parser):
	vm_running_in_backupOS(parser)
	vm_is_login_in_backupOS(parser)
	
def vm_recover_in_slaveOS(parser):
	vm_running_in_slaveOS(parser)
	vm_is_login_in_slaveOS(parser)
	
def vm_recover_in_backup_or_slave(parser):
	try:
		vm_recover_in_slaveOS(parser)
	except TA_error.Assert_Error:
		vm_recover_in_backupOS(parser)
def vm_running_in_hostOS(parser):
	"""
	vm is running in hostOS or not

	:param parser: config
	:return: True/raise exception
	"""

	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                  , parser["PrimaryOS_usr"]
                  , parser["PrimaryOS_pwd"]) #獲得ssh

	t_end = time.time()
	if "ast_vm_running_wait_time" in parser.keys(): #若參數ast_vm_running_wait_time存在於parser，則進入
		t_end = time.time()+float(parser["ast_vm_running_wait_time"]) #計算出等待之時間，並存於t_end
	while time.time() < t_end: #超過t_end則跳出迴圈
		#每sleep一秒就詢問一次狀態
		time.sleep(1)
		if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh): #狀態為running就跳出迴圈
			break
	if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh): #若回傳之狀態是running，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not running in hostOS" % parser["vm_name"])

def vm_running_in_BackupOS(parser):
	"""
	vm is running in hostOS or not

	:param parser: config
	:return: True/raise exception
	"""

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                  , parser["BackupOS_usr"]
                  , parser["BackupOS_pwd"]) #獲得ssh

	t_end = time.time()
	if "ast_vm_running_wait_time" in parser.keys(): #若參數ast_vm_running_wait_time存在於parser，則進入
		t_end = time.time()+float(parser["ast_vm_running_wait_time"]) #計算出等待之時間，並存於t_end
	while time.time() < t_end: #超過t_end則跳出迴圈
		#每sleep一秒就詢問一次狀態
		time.sleep(1)
		if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh): #狀態為running就跳出迴圈
			break
	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh): #若回傳之狀態是running，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not running in BackupOS" % parser["vm_name"])


def vm_shudown_in_hostOS(parser):
	"""
	vm is running in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                  , parser["PrimaryOS_usr"]
                  , parser["PrimaryOS_pwd"]) #獲得ssh
	if FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"],ssh): #若回傳之狀態是shut off，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not shutdown in hostOS" % parser["vm_name"])

def vm_is_login_in_hostOS(parser):
	"""
	vm is login in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	
	print 577
	if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
		return True
	else:
		ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
		
		cmd = "sudo %s" % parser["login_reply_path"]
		#print cmd
		s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
		if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
			print "manually login reply success"
			return True
		ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not login in hostOS" % parser["vm_name"])


		

def vm_is_login_in_backupOS(parser):
	"""
	vm is login in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	

	if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
		return True
	else:
		ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
		
		cmd = "sudo %s" % parser["login_reply_path"]
		#print cmd
		s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
		if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
			return True
		ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not login in backupOS" % parser["vm_name"])	


def vm_is_login_in_slaveOS(parser):
	"""
	vm is login in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	

	if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
		return True
	else:
		ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
		
		cmd = "sudo %s" % parser["login_reply_path"]
		#print cmd
		s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
		if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
			return True
		ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not login in backupOS" % parser["vm_name"])	

def vm_running_in_backupOS(parser):
	"""
	vm is running in backupOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                  , parser["BackupOS_usr"]
                  , parser["BackupOS_pwd"]) #獲得ssh

	print 64
	t_end = time.time()
	if "ast_vm_running_wait_time" in parser.keys(): #若參數ast_vm_running_wait_time存在於parser，則進入
		t_end = time.time()+float(parser["ast_vm_running_wait_time"]) #計算出等待之時間，並存於t_end
	print 65
	while time.time() < t_end: #超過t_end則跳出迴圈
		#每sleep一秒就詢問一次狀態
		time.sleep(1)
		#print 66
		if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh): #狀態為running就跳出迴圈
			break
	print 67
	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh): #若回傳之狀態是running，則test oracle通過，否則raise exception
		ssh.close()
		return True
	print 68
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not running in backupOS" % parser["vm_name"])

def vm_shudown_in_backupOS(parser):
	"""
	vm is running in SlaveOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                  , parser["BackupOS_usr"]
                  , parser["BackupOS_pwd"]) #獲得ssh
	if FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"],ssh): #若回傳之狀態是shut off，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not shutdown in BackupOS" % parser["vm_name"])



def vm_running_in_slaveOS(parser):
	"""
	vm is running in SlaveOS or not

	:param parser: config
	:return: True/raise exception
	"""

	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                  , parser["SlaveOS_usr"]
                  , parser["SlaveOS_pwd"]) #獲得ssh

	t_end = time.time()
	if "ast_vm_running_wait_time" in parser.keys(): #若參數ast_vm_running_wait_time存在於parser，則進入
		t_end = time.time()+float(parser["ast_vm_running_wait_time"]) #計算出等待之時間，並存於t_end
	while time.time() < t_end: #超過t_end則跳出迴圈
		#每sleep一秒就詢問一次狀態
		time.sleep(1)
		if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh): #狀態為running就跳出迴圈
			break
	if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh): #若回傳之狀態是running，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not running in SlaveOS" % parser["vm_name"])

def vm_shudown_in_SlaveOS(parser):
	"""
	vm is running in SlaveOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                  , parser["SlaveOS_usr"]
                  , parser["SlaveOS_pwd"]) #獲得ssh
	if FTVM.is_shutoff(parser["vm_name"], parser["SlaveOS_ip"],ssh): #若回傳之狀態是shut off，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not shutdown in SlaveOS" % parser["vm_name"])

def vm_duplicate_start(parser):
	"""
	check vm can duplicate start or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                  , parser["PrimaryOS_usr"]
                  , parser["PrimaryOS_pwd"]) #獲得ssh
	
	if FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		raise TA_error.Assert_Error("VM name : %s is shut off in PrimaryOS")
	if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		
		out = FTVM.duplicate_ftstart(parser["PrimaryOS_name"], parser["vm_name"], parser["PrimaryOS_ip"], ssh)
		expected = HAagent_terminal.Startvm_addVM_failed % (HAagent_terminal.Vm_has_exist)
		success = ( out == expected )
		
		if success :
			return True
		raise TA_error.Assert_Error("vm : %s duplicate start fail" % parser["vm_name"])

def non_primary_start_ftvm(parser):
	"""
	check non primary node(backup node) can start ftvm or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                  , parser["BackupOS_usr"]
                  , parser["BackupOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
		raise TA_error.Assert_Error("VM : %s already in running" % parser["vm_name"])
	if FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh):
		out = FTVM.ftstart(parser["BackupOS_name"], parser["vm_name"], parser["BackupOS_ip"], ssh)
		expected = HAagent_terminal.Not_primary
		
		success = (out == expected) and FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh) # shell message and FTVM shutoff
		if success :
			return True
	raise TA_error.Assert_Error("non primary start ftvm : %s fail" % parser["vm_name"])

def rm_non_running_ftvm(parser):
	"""
	detect remove non running ftvm
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                  , parser["PrimaryOS_usr"]
                  , parser["PrimaryOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		raise TA_error.Assert_Error("VM : %s already in running" % parser["vm_name"])
	if FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		out = FTVM.ftshutdown(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
		expected = HAagent_terminal.Vm_not_exist
		
		success = (out == expected) 
		if success :
			return True
	raise TA_error.Assert_Error("remove non running ftvm : %s fail" % parser["vm_name"])

def non_primary_rm_ftvm(parser):
	"""
	detect non primary remove ftvm
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                  , parser["BackupOS_usr"]
                  , parser["BackupOS_pwd"]) #獲得ssh
	if FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh):
		raise TA_error.Assert_Error("VM : %s shutoff" % parser["vm_name"])
	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
		out = FTVM.ftshutdown(parser["vm_name"], parser["BackupOS_ip"], ssh)
		expected = HAagent_terminal.Not_primary
	
		success = (out == expected) and FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh) #shell message and FTVM running
		if success :
			return True
	raise TA_error.Assert_Error("remove non running ftvm : %s fail" % parser["vm_name"])


def detect_rm_non_running_ftvm(parser):
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                  , parser["PrimaryOS_usr"]
                  , parser["PrimaryOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		raise TA_error.Assert_Error("VM : %s running in PrimaryOS" % parser["vm_name"])
	if FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		out = HAagent.remove_ftvm(parser["vm_name"], parser, ssh)
		expected = HAagent_terminal.Vm_not_exist
		
		success = (out == expected)
		if success:
			return True
		raise TA_error.Assert_Error("rm non running vm fail")

def libvirt_stop_start_ftvm(parser):
	"""
	detect when libvirt daemon shutdown , can HAAgent start ftvm
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                  , parser["PrimaryOS_usr"]
                  , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cmd = cmd_HAagent.start_ftvm_cmd(parser["PrimaryOS_name"], parser["vm_name"])
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	out = s_stdout.read()
	expected = HAagent_terminal.Startvm_create_vm_failed % ( HAagent_terminal.Libvirt_connection_failed % HAagent_terminal.Libvirt_self_connection)+"\n"
	
	
	success = (out == expected)
	
	print out
	print expected
	
	FTsystem.start(ssh)
	
	#print success
	if success : 
		return True
	raise TA_error.Assert_Error("libvirt stop then start ftvm fail")
	
		
def FTsystem_running_in_hostOS(parser):
	"""
	FTsystem is running in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh

	if FTsystem.get_status(ssh) == "running": #透過ssh詢問FTsystem之狀態是否為running
		ssh.close()
		return True

	ssh.close()
	raise TA_error.Assert_Error("FTsystem is not running in hostOS")

def detect_fail(parser):
	"""
	FTsystem find fail or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh
	if mmsh.infofail(parser["vm_name"],ssh) != "no fail":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no fail in hostOS" % parser["vm_name"])

def detect_no_fail(parser):
	"""
	FTsystem find no fail or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh	
	if mmsh.infofail(parser["vm_name"],ssh) == "no fail":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has fail in hostOS" % parser["vm_name"])

def detect_fail_vm_crash(parser):
	"""
	FTsystem find fail and fail is vm crash or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh
	print 558
	if "ast_vm_crash_time" in parser.keys(): #若參數ast_vm_crash_time存在於parser，則進入
		time.sleep(int(parser["ast_vm_crash_time"]))
	if mmsh.infofail(parser["vm_name"] ,ssh) == "vm crash":
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) has not detect vm crash in hostOS" % parser["vm_name"])

def detect_fail_os_crash(parser):
	"""
	FTsystem find fail and fail is os crash or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh

	if mmsh.infofail(parser["vm_name"],ssh) == "vm os crash":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has not detect vm os crash" % parser["vm_name"])
	
def detect_primary_vm_guestOS_hang_info(parser):
	"""
	detech mmsh overview information fit the guestOS hang reboot message
	:param parser : config
	:return True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_vm_infofail(parser["PrimaryOS_name"],parser["vm_name"], parser, ssh)
	expected = HAagent_terminal.Vm_lastfail_messages[2][0] # guestOS hang and reboot success
	
	if fail != expected:
		raise TA_error.Assert_Error("vm : %s info fail , fail reason : %s  expected : %s"  % (parser["vm_name"] , fail , expected))
	return True

def detect_backup_vm_guestOS_hang_info(parser):
	"""
	detech mmsh overview information fit the guestOS hang reboot message
	:param parser : config
	:return True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	time.sleep(float(5))
	
	fail = HAagent_info.get_vm_infofail(parser["BackupOS_name"],parser["vm_name"], parser, ssh)
	expected = HAagent_terminal.Vm_lastfail_messages[2][0] # guestOS hang and reboot success
	
	if fail != expected:
		raise TA_error.Assert_Error("vm : %s info fail , fail reason : %s  expected : %s"  % (parser["vm_name"] , fail , expected))
	return True

def detect_primary_vm_crash_info(parser):
	"""
	detech mmsh overview information fit the vm crash reboot message
	:param parser : config
	:return True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_vm_infofail(parser["PrimaryOS_name"],parser["vm_name"], parser, ssh)
	expected = HAagent_terminal.Vm_lastfail_messages[0][0] # vm crash and reboot now

	if fail != expected:
		raise TA_error.Assert_Error("vm : %s info fail , fail reason : %s  expected : %s"  % (parser["vm_name"] , fail , expected))
	return True


def detect_backup_vm_crash_info(parser):
	"""
	detech mmsh overview information fit the vm crash reboot message
	:param parser : config
	:return True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_vm_infofail(parser["BackupOS_name"],parser["vm_name"], parser, ssh)
	expected = HAagent_terminal.Vm_lastfail_messages[0][0] # vm crash and reboot now

	if fail != expected:
		raise TA_error.Assert_Error("vm : %s info fail , fail reason : %s  expected : %s"  % (parser["vm_name"] , fail , expected))
	return True

def detect_primaryOS_crash_info(parser):
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_node_infofail(parser["PrimaryOS_name"], parser, ssh)
	expected = HAagent_terminal.Node_status_hostdown
	success = (fail == expected)
	
	if success:
		return True
	raise TA_error.Assert_Error("primary OS crash info fail , Fail msg : %s , Expected msg : %s" % fail , expected)

def detect_primary_network_isolation_info(parser):
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_node_infofail(parser["PrimaryOS_name"], parser, ssh)
	expected = HAagent_terminal.Node_status_self_network_isolation
	success = (fail == expected)
	
	if success:
		return True
	raise TA_error.Assert_Error("primary network isolation info fail , Fail msg : %s , Expected msg : %s" % fail , expected)

def detect_backupOS_crash_info(parser):
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_node_infofail(parser["BackupOS_name"], parser, ssh)
	expected = HAagent_terminal.Node_status_hostdown
	success = (fail == expected)
	
	if success:
		return True
	raise TA_error.Assert_Error("backup OS crash info fail , Fail msg : %s , Expected msg : %s" % fail , expected)

def detect_backupOS_network_isolation_info(parser):
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_node_infofail(parser["BackupOS_name"], parser, ssh)
	expected = HAagent_terminal.Node_status_self_network_isolation
	success = (fail == expected)
	
	if success:
		return True
	raise TA_error.Assert_Error("backup network isolation info fail , Fail msg : %s , Expected msg : %s" % fail , expected)


def detect_slaveOS_crash_info(parser):
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_node_infofail(parser["SlaveOS_name"], parser, ssh)
	expected = HAagent_terminal.Node_status_hostdown
	success = (fail == expected)
	
	if success:
		return True
	raise TA_error.Assert_Error("slave OS crash info fail , Fail msg : %s , Expected msg : %s" % fail , expected)

def detect_slaveOS_network_isolation_info(parser):
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲取ssh
	
	fail = HAagent_info.get_node_infofail(parser["SlaveOS_name"], parser, ssh)
	expected = HAagent_terminal.Node_status_self_network_isolation
	success = (fail == expected)
	
	if success:
		return True
	raise TA_error.Assert_Error("slave network isolation info fail , Fail msg : %s , Expected msg : %s" % fail , expected)

def do_recovery(parser):
	"""
	FTsystem do recovery or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh

	if mmsh.inforecover(parser["vm_name"],ssh) != "no recover":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery" % parser["vm_name"])


def no_recovery(parser):
	"""
	FTsystem no recover or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh

	if mmsh.inforecover(parser["vm_name"],ssh) == "no recover":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has recovery" % parser["vm_name"])

def recovery_vm_p_restart(parser):
	"""
	FTsystem recover vm process restart or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh

	if "ast_vm_p_restart_time" in parser.keys(): #若參數ast_vm_p_restart_time存在於parser，則進入
		time.sleep(int(parser["ast_vm_p_restart_time"]))
	if mmsh.inforecover(parser["vm_name"], ssh) == "vm process restart":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery : vm process restart" % parser["vm_name"])

def recovery_vm_reboot(parser):
	"""
	FTsystem recover vm reboot or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲取ssh

	if mmsh.inforecover(parser["vm_name"],ssh) == "vm reboot":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery : vm reboot" % parser["vm_name"])

def libvirt_running_in_hostOS(parser):
	"""
	libvirt process is running in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	if "ast_libvirt_running_wait_time" in parser.keys(): #若參數ast_libvirt_running_wait_time存在於parser，則進入
		time.sleep(float(parser["ast_libvirt_running_wait_time"]))
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	if FTsystem.is_running(ssh):
		return True
	ssh.close()
	raise TA_error.Assert_Error("libivrt isn't running")

def master_monitor_running(parser):
	"""
	master monitor running or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	if "ast_mm_running_wait_time" in parser.keys(): #若參數ast_mm_running_wait_time存在於parser，則進入
		 time.sleep(float(parser["ast_mm_running_wait_time"]))
	if master_monitor.is_running(ssh):
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("master_monitor isn't running")

def test(parser):
	"""
	test when raise exception
	"""
	raise TA_error.Assert_Error("test FTVMTA log feature")

def detect_create_cluster(parser):
	"""
	cluster created or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cluster = parser["Cluster_name"]
	success =  HAagent_info.is_cluster_exist(cluster, parser)
	ssh.close()	
	
	if success :
		return True
	raise TA_error.Assert_Error("create cluster fail")

def detect_create_duplicate_cluster(parser):
	"""
	duplicate cluster created or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	out = HAagent.create_cluster("test_c", "test_n", "127.0.0.1", "9999", parser, ssh)
	success = (HAagent_terminal.Already_in_cluster in out)
	ssh.close()

	if success :
		return True
	raise TA_error.Assert_Error("create duplicate cluster fail")
	
def detect_de_cluster(parser):
	"""
	cluster deleted or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cluster = parser["Cluster_name"]
	
	success = HAagent_info.is_cluster_exist(cluster, parser)
	ssh.close()
	
	if not success:
		return True
	raise TA_error.Assert_Error("de cluster fail")

def detect_non_primary_de_cluster(parser):
	"""
	non-primary node (in this test case is backup node) delete cluster or not
	:param parser: config
	:return: True/raise exception
	"""
	cluster = parser["Cluster_name"]
	
	success = HAagent_info.is_cluster_exist(cluster, parser)
	
	if success:
		return True
	raise TA_error.Assert_Error("non primary de cluster fail")
	
def detect_de_outer_cluster(parser):
	"""
	outer cluster deleted or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	cluster = "test_c"
	success = HAagent_info.is_cluster_exist(cluster, parser)
	ssh.close()	
	
	if success:
		return True
	raise TA_error.Assert_Error("de outer cluster fail")

def detect_add_node(parser):
	"""
	detect add node to cluster or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh

	primary_success = HAagent_info.is_add_primary_success(parser)
	backup_success = HAagent_info.is_add_backup_success(parser)
	slave_success = HAagent_info.is_add_slave_success(parser)
	
	ssh.close()
	
	if not primary_success:
		raise TA_error.Assert_Error("primary add node fail")
	if not backup_success:
		raise TA_error.Assert_Error("backup add node fail")
	if not slave_success:
		raise TA_error.Assert_Error("slave add node fail")
	return True

def detect_add_duplicate_node(parser):
	"""
	detect add duplicate node to cluster or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	#add the same node and return stdoutput
	HAagent.overview(parser, ssh)
	out = HAagent.add_node(parser["Cluster_name"], parser["PrimaryOS_name"], parser["PrimaryOS_ip"] , parser["PrimaryOS_ipmb"], parser, ssh)
	
	success = (HAagent_terminal.Node_name_repeat in out)
	ssh.close()

	if success:
		return True
	raise TA_error.Assert_Error("add duplicate node fail")

def detect_add_outer_node(parser):
	"""
	detect add outer node to cluster or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	#add node in non exist cluster
	out = HAagent.add_node("test_b", parser["BackupOS_name"], parser["BackupOS_ip"], parser["BackupOS_ipmb"], parser, ssh)
	success = (HAagent_terminal.Not_in_cluster in out)
	ssh.close()

	if success:
		return True
	raise TA_error.Assert_Error("add outer node fail")

def detect_non_primary_node_add_node(parser):
	"""
	detect use non-primary node add node success or not
	:param parser: config
	:return: True/raise exception
	"""
	success = HAagent_info.is_node_exists(parser["Cluster_name"], parser["SlaveOS_name"], parser)
	
	if not success:
		return True
	raise TA_error.Assert_Error("non primary node add node fail")
	
def detect_de_node(parser):
	"""
	detect remove node or not
	:param parser: config
	:return: True/raise exception
	"""
	success = HAagent_info.is_node_exists("test_c", "test_n", parser)
	
	if not success:
		return True
	raise TA_error.Assert_Error("de node fail")
	
def detect_non_primary_de_node(parser):
	"""
	detect remove node or not
	:param parser: config
	:return: True/raise exception
	"""
	success = HAagent_info.is_node_exists(parser["Cluster_name"], parser["PrimaryOS_name"], parser)
	
	if success:
		return True
	raise TA_error.Assert_Error("non primary de node fail")

def detect_overview(parser):
	"""
	detect remove node or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	out = HAagent.overview(parser, ssh)	
	#success = (HAagent_terminal. in out)
	
	#if success:
	#	return True
	#raise TA_error.Assert_Error("overview fail")

if __name__ == '__main__':
	parser = {}
	parser["BackupOS_ip"] = "140.115.53.132"
	parser["BackupOS_usr"] = "user"
	parser["BackupOS_pwd"] = "000000"
	parser["BackupOS_name"] = "h2"
	
	parser["NFS_ip"] = "192.168.1.106"
	parser["NFS_usr"] = "testagent"
	parser["NFS_pwd"] = "root"
	
	parser["PrimaryOS_ip"] = "192.168.1.100"
	parser["PrimaryOS_usr"] = "primary"
	parser["cluster_file_path"] = "/var/ha/images/clusterFile.txt"
	parser["vm_name"] = "test-daemon12"
	parser["PrimaryOS_pwd"] = "root"
	parser["PrimaryOS_name"] = "primary"
	parser["GuestOS_ip"] = "192.168.1.10"
	parser["GuestOS_usr"] = "test-daemon12"
	parser["GuestOS_pwd"] = "root"
	parser["TA_ip"] = "192.168.1.102"
	parser["TA_msg_sock_port"] = "20000"
	parser["ast_vm_login_wait_time"] = "10"
	parser["login_reply_path"] = "/etc/profile.d/login_reply.sh"
	
	#ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
    #                         , parser["PrimaryOS_usr"]
    #                          , parser["PrimaryOS_pwd"]) #獲得ssh
	#FTVM.ftstart(parser["PrimaryOS_name"], parser["vm_name"], parser["PrimaryOS_ip"], ssh)
	#print out
	#print backupOS_role_is_Master_on_BackupOS(parser)
	
	
	detect_primary_vm_crash_info(parser)
	
	"""
	ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
		
	cmd = "sudo %s" % parser["login_reply_path"]
	#print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	if FTVM.is_login(parser["vm_name"]
			, parser["TA_ip"]
			, parser["TA_msg_sock_port"]
			, int(parser["ast_vm_login_wait_time"])):
		
		 #若回傳VM登入完成，則test oracle通過，否則raise exception
		print " lasdasdasd"
	"""
