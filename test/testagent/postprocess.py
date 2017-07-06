#!/usr/bin/python
#-*- coding: utf-8 -*-

import paramiko

import time

import FTsystem
import FTVM
import FTOS
import TA_error
import mmsh
import NFS
import shell_server
import HAagent


def run_postprocess(parser):
	"""
	when test done , each node will do postprocess
	:param parser: is a dict, get from Test config file
	""" 
	postprocess_nodes(parser)
	print "pos nodes"
	postprocess_Host(parser)
	print "pos host"
	postprocess_Backup(parser)
	print "pos backup"
	postprocess_Slave(parser)
	print "pos slave"
	postprocess_NFS(parser)
	print "pos nfs"
	postprocess_node_reboot(parser)
	print "post nodes reboot"


def postprocess_nodes(parser):
	if parser["pos_check_primaryOS_status"] == "yes":
		if not FTOS.IPMI_OS_is_running(parser["PrimaryOS_ip"], parser):
			postprocess_primaryOS_running(parser)
	if parser["pos_check_backupOS_status"] == "yes":
		if not FTOS.IPMI_OS_is_running(parser["BackupOS_ip"], parser):
			postprocess_backupOS_running(parser)
	if parser["pos_check_slaveOS_status"] == "yes":
		if not FTOS.IPMI_OS_is_running(parser["SlaveOS_ip"], parser):
			postprocess_slaveOS_running(parser)
def postprocess_Host(parser):
	"""
	when test done , primary postprocess
	:param parser: is a dict, get from Test config file
	""" 
	postprocess_hostOS_vm(parser)
	postprocess_hostOS_FTsystem(parser)
	postprocess_hostOS_HAAgent(parser)

def postprocess_Backup(parser):
	"""
	when test done , Backup postprocess
	:param parser: is a dict, get from Test config file
	""" 
	postprocess_backupOS_vm(parser)
	postprocess_backupOS_FTsystem(parser)
	postprocess_backupOS_HAAgent(parser)

def postprocess_Slave(parser):
	"""
	when test done , Slave postprocess
	:param parser: is a dict, get from Test config file
	""" 
	postprocess_slaveOS_vm(parser)
	postprocess_slaveOS_FTsystem(parser)
	postprocess_slaveOS_HAAgent(parser)

def postprocess_NFS(parser):
	"""
	when test done , NFS postprocess
	:param parser: is a dict, get from Test config file
	""" 
	postprocess_NFS_OS(parser)

def postprocess_node_reboot(parser):
	postprocess_Host_OS_reboot(parser)
	postprocess_Backup_OS_reboot(parser)
	postprocess_Slave_OS_reboot(parser)
	
def postprocess_Host_OS_reboot(parser):
	"""
	post process host os part
	:param parser: is a dict, get from Test config file
	"""
	
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh 
	if not FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"] , ssh):
		raise TA_error.Postprocess_Error("vm %s in PrimaryOS cannot shutdown " % parser["vm_name"])
	if parser["pos_hostOS_restart"] == "yes":
		if FTOS.OS_is_running(parser["PrimaryOS_ip"], parser):
			FTOS.reboot(ssh)
	
def postprocess_Backup_OS_reboot(parser):
	"""
	post process backup os part
	:param parser: is a dict, get from Test config file
	"""
	
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh 
	
	if not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"] , ssh):
		raise TA_error.Postprocess_Error("vm %s in BackupOS cannot shutdown " % parser["vm_name"])
	if parser["pos_backupOS_restart"] == "yes":
		if FTOS.OS_is_running(parser["BackupOS_ip"], parser):
			FTOS.reboot(ssh)
	
def postprocess_Slave_OS_reboot(parser):
	"""
	post process slave os part
	:param parser: is a dict, get from Test config file
	"""
	
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
	
	if not FTVM.is_shutoff(parser["vm_name"], parser["SlaveOS_ip"] , ssh):
		raise TA_error.Postprocess_Error("vm %s in SlaveOS cannot shutdown " % parser["vm_name"])
	if parser["pos_slaveOS_restart"] == "yes":
		if FTOS.OS_is_running(parser["SlaveOS_ip"], parser):
			FTOS.reboot(ssh)
	
def postprocess_NFS_OS(parser):
	"""
	post process nfs os part
	:param parser: is a dict, get from Test config file
	"""
	
	postprocess_NFS_reset(parser)
	
	if parser["pos_NFSOS_restart"] == "yes":
		postprocess_NFS_OS_reboot(parser)
	

def postprocess_NFS_OS_reboot(parser):
	"""
	when test case done , Host OS reboot
	:param parser: is a dict, get from Test config file
	"""
	
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲得ssh
	if FTOS.OS_is_running(parser["NFS_ip"], parser):
		FTOS.reboot(ssh)
def postprocess_NFS_reset(parser):
	"""
	when test done , clear nfs file

	:param parser: is a dict, get from Test config file
	:param ssh : shell server
	""" 
	ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲得ssh
	NFS.reset(parser, ssh)
	ssh.close()
	
def postprocess(parser):
	"""
	when testing done, postprocess something

	:param parser: is a dict, get from Test config file
	"""
	time.sleep(1)
	print "POST"
	postprocess_hostOS(parser)
	print "POST1"
	postprocess_backupOS(parser)

def postprocess_hostOS(parser):
	"""
	postprocess hostOS

	:called func: postprocess
	:param parser: is a dict, get from Test config file
	"""
	#postprocess_hostOS_OS(parser)
	postprocess_hostOS_FTsystem(parser)
	print "POST2"
	postprocess_hostOS_vm(parser)
	print "POST3"
	postprocess_hostOS_OS_running(parser)
	
def postprocess_backupOS(parser):
	"""
	postprocess backupOS

	:called func: postprocess
	:param parser: is a dict, get from Test config file
	"""
	postprocess_backupOS_vm(parser)
	print "POST4"
	postprocess_backupOS_OS_running(parser)
	print "POST5"
	postprocess_hostOS_ATCA_OS_running(parser)
	print "POST6"
	postprocess_backupOS_ATCA_OS_running(parser)

def postprocess_hostOS_OS(parser):
	"""
	postprocess hostOS OS part

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_hostOS_shutdown"] == "yes": #若pos_hostOS_shutdown為yes則進入
		if mmsh.statehost(parser["PrimaryOS_name"]) != "shutdown": #詢問mmsh，vm所在host的狀態，若不為shutdown 則進行關機之動作
			mmsh.stophost(parser["PrimaryOS_name"])
			time.sleep(float(parser["pos_hostOS_shutdown_time"]))
	if mmsh.statehost(parser["PrimaryOS_name"]) != "shutdown": #若狀態不為shutdown則raise exception
		raise TA_error.Postprocess_Error("PrimaryOS can not shutdown")


def postprocess_hostOS_FTsystem(parser):
	"""
	postprocess PrimaryOS FTsystem part

	check FTsystem status 

	start/stop FTsystem

	raise exception if FTsystem can not start/stop

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_hostOS_FTsystem"] == "yes":
		ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
								, parser["PrimaryOS_usr"]
								, parser["PrimaryOS_pwd"]) #獲得ssh
		status = FTsystem.get_status(ssh) #獲得libvirt status
		if status == "not running" and parser["pos_hostOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數pos_hostOS_FTsystem_start必須為running，則進入
			FTsystem.start(ssh) #透過ssh開啟libvirt
			time.sleep(float(parser["pos_hostOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("PrimaryOS FTsystem can not start")
		if status == "running" and parser["pos_hostOS_FTsystem_start"] == "no": #若狀態為running且根據參數pos_hostOS_FTsystem_start必須不為running，則進入
			FTsystem.stop(ssh) #透過ssh關閉libvirt
			time.sleep(float(parser["pos_hostOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("PrimaryOS FTsystem can not stop")
		ssh.close()
def postprocess_hostOS_HAAgent(parser):
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh 
	if HAagent.is_running(ssh, parser):
		HAagent.exit(parser, ssh)
		if HAagent.is_running(ssh, parser):
			ssh.close()
			raise TA_error.Postprocess_Error("Primary HAAgent cannot shutdown")
	else:
		pass

def postprocess_hostOS_vm(parser):
	"""
	postprocess hostOS vm part

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_hostOS_VM"] == "yes": #需要確認VM狀態，則進入
		if parser["pos_hostOS_VM_status"] == "running":
			postprocess_hostOS_vm_running(parser)
		elif parser["pos_hostOS_VM_status"] == "shut off":
			postprocess_hostOS_vm_shutdown(parser)
		elif parser["pos_hostOS_VM_status"] == "paused":
			pass

def postprocess_hostOS_vm_running(parser):
	"""
	postrocess vm become running

	:called func: postprocess_hostOS_vm
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
							, parser["PrimaryOS_usr"]
							, parser["PrimaryOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		FTVM.restart(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
	elif FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		FTVM.start(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
	time.sleep(float(parser["pos_hostOS_VM_boot_time"]))
	if not FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("PrimaryOS %s can not start" % parser["vm_name"])
	ssh.close()

def postprocess_hostOS_vm_shutdown(parser):
	"""
	postprocess vm become shutdown

	:called func: postprocess_hostOS_vm
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
							, parser["PrimaryOS_usr"]
							, parser["PrimaryOS_pwd"]) #獲得ssh

	if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		print "shutdown now 1"
		time.sleep(float(parser["pos_hostOS_wait_VM_enable_shutdown_time"]))
		FTVM.destroy(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
	elif FTVM.is_paused(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		print "shutdown now 2"
		time.sleep(float(parser["pos_hostOS_wait_VM_enable_shutdown_time"]))
		FTVM.resume(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
		FTVM.destroy(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
	time.sleep(float(parser["pos_hostOS_VM_shutdown_time"]))
	#print FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"])
	
	times = 0
	while times < 30:
		if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
			print "destroy primary os vm "
			FTVM.destroy(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
			break;
		time.sleep(float(1))
		times += 1

	if not FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("PrimaryOS vm : %s can not shutdown" % parser["vm_name"])

	ssh.close()

def postprocess_backupOS_vm(parser):
	"""
	postprocess backupOS vm part

	:called func: postprocess_backupOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_backupOS_VM"] == "yes":
		if parser["pos_backupOS_VM_status"] == "running":
			postprocess_backupOS_vm_running(parser)
			pass
		elif parser["pos_backupOS_VM_status"] == "shut off":
			postprocess_backupOS_vm_shutdown(parser)
		elif parser["pos_backupOS_VM_status"] == "paused":
			pass
		
def postprocess_backupOS_vm_running(parser):
	"""
	postrocess vm become running

	:called func: postprocess_BackupOS_vm
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
							, parser["BackupOS_usr"]
							, parser["BackupOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
		FTVM.restart(parser["vm_name"], parser["BackupOS_ip"], ssh)
	elif FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh):
		FTVM.start(parser["vm_name"], parser["BackupOS_ip"], ssh)
	time.sleep(float(parser["pos_BackupOS_VM_boot_time"]))
	if not FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("BackupOS vm : %s can not start" % parser["vm_name"])
	ssh.close()
		
def postprocess_backupOS_vm_shutdown(parser):
	"""
	postprocess backupOS vm shutdown

	:called func: postprocess_backupOS_vm
	:param parser: is a dict, get from Test config file
	"""

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
    						, parser["BackupOS_usr"]
    						, parser["BackupOS_pwd"]) #獲得ssh

	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
		time.sleep(float(parser["pos_backupOS_wait_VM_enable_shutdown_time"]))
		FTVM.destroy(parser["vm_name"], parser["BackupOS_ip"], ssh)
	elif FTVM.is_paused(parser["vm_name"], parser["BackupOS_ip"], ssh):
		FTVM.resume(parser["vm_name"], parser["BackupOS_ip"], ssh)
		time.sleep(float(parser["pos_backupOS_wait_VM_enable_shutdown_time"]))
		FTVM.destroy(parser["vm_name"], parser["BackupOS_ip"], ssh)
	time.sleep(float(parser["pos_backupOS_VM_shutdown_time"]))


	times = 0
	while times < 30:
		if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
			print "destroy backup os vm "
			FTVM.destroy(parser["vm_name"], parser["BackupOS_ip"], ssh)
			break;
		time.sleep(float(1))
		times += 1

	if not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("backupOS vm : %s can not shutdown" % parser["vm_name"])

	ssh.close()
	
def postprocess_backupOS_FTsystem(parser):
	"""
	postprocess backupOS FTsystem part

	check FTsystem status 

	start/stop FTsystem

	raise exception if FTsystem can not start/stop

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_backupOS_FTsystem"] == "yes":
		ssh = shell_server.get_ssh(parser["BackupOS_ip"]
								, parser["BackupOS_usr"]
								, parser["BackupOS_pwd"]) #獲得ssh
		status = FTsystem.get_status(ssh) #獲得libvirt status
		if status == "not running" and parser["pos_backupOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數pos_hostOS_FTsystem_start必須為running，則進入
			FTsystem.start(ssh) #透過ssh開啟libvirt
			time.sleep(float(parser["pos_backupOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("backupOS FTsystem can not start")
		if status == "running" and parser["pos_backupOS_FTsystem_start"] == "no": #若狀態為running且根據參數pos_hostOS_FTsystem_start必須不為running，則進入
			FTsystem.stop(ssh) #透過ssh關閉libvirt
			time.sleep(float(parser["pos_backupOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("backupOS FTsystem can not stop")
		ssh.close()
		
		
def postprocess_backupOS_HAAgent(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh 
	if HAagent.is_running(ssh, parser):
		HAagent.exit(parser, ssh)
		if HAagent.is_running(ssh, parser):
			ssh.close()
			raise TA_error.Postprocess_Error("Backup HAAgent cannot shutdown")
	else:
		pass

def postprocess_primaryOS_running(parser):
	"""
	postrocess host OS become running

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_primaryOS_status"] == "yes":
		if parser["IPMI_supported"] == "yes":
			ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
			FTOS.IPMI_boot(parser["PrimaryOS_ipmb"], ssh)
			ssh.close()
		elif parser["IPMI_supported"] == "no":
			FTOS.L1_boot(parser["PrimaryOS_NetworkAdaptor"])
	if FTOS.OS_is_running(parser["PrimaryOS_ip"], parser):
		return True
	raise TA_error.Postprocess_Error("primary OS can not boot")

def postprocess_backupOS_running(parser):
	"""
	postrocess backup OS become running

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_backupOS_status"] == "yes":
		if parser["IPMI_supported"] == "yes":
			ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
			FTOS.IPMI_boot(parser["BackupOS_ipmb"], ssh)
			ssh.close()
		elif parser["IPMI_supported"] == "no":
			FTOS.L1_boot(parser["BackupOS_NetworkAdaptor"])
	if FTOS.OS_is_running(parser["BackupOS_ip"], parser):
		return True
	raise TA_error.Postprocess_Error("backup OS can not boot")	
		
def postprocess_slaveOS_running(parser):
	"""
	postrocess slave OS become running

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_slaveOS_status"] == "yes":
		if parser["IPMI_supported"] == "yes":
			ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh 
			FTOS.IPMI_boot(parser["SlaveOS_ipmb"], ssh)
			ssh.close()
		elif parser["IPMI_supported"] == "no":
			FTOS.L1_boot(parser["SlaveOS_NetworkAdaptor"])
	if FTOS.OS_is_running(parser["SlaveOS_ip"], parser):
		return True
	raise TA_error.Postprocess_Error("slave OS can not boot")	
		
	
def postprocess_hostOS_ATCA_OS_running(parser):

	if parser["pos_boot_ATCA_hostOS"] == "yes":
		cmd = "ssh 172.16.33.222 'clia activate %s 0'" % (parser["PrimaryOS_ipmc_name"])

		ssh = shell_server.get_ssh(parser["BackupOS_ip"]
							, parser["BackupOS_usr"]
							, parser["BackupOS_pwd"]) #獲得ssh

		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
		ssh.close()

		if not FTVM.is_login(parser["PrimaryOS_name"]
			, parser["TA_ip"]
			, parser["TA_msg_sock_port"]
			, int(parser["pos_hostOS_login_time"])):
			raise TA_error.Postprocess_Error("PrimaryOS %s is not login" % parser["PrimaryOS_name"])

		#postprocess_hostOS_mount_nfs(parser)


def postprocess_backupOS_ATCA_OS_running(parser):

	if parser["pos_boot_ATCA_backupOS"] == "yes":
		cmd = "ssh 172.16.33.222 'clia activate %s 0'" % (parser["BackupOS_ipmc_name"])

		print cmd

		ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
    						, parser["PrimaryOS_usr"]
    						, parser["PrimaryOS_pwd"]) #獲得ssh

		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
		ssh.close()

		if not FTVM.is_login(parser["BackupOS_name"]
			, parser["TA_ip"]
			, parser["TA_msg_sock_port"]
			, int(parser["pos_backupOS_login_time"])):
			raise TA_error.Postprocess_Error("PrimaryOS %s is not login" % parser["BackupOS_name"])

		#postprocess_hostOS_mount_nfs(parser)

def postprocess_hostOS_mount_nfs(parser):

	if parser["pos_hostOS_mount_nfs"] == "yes":
		cmd = "mount -t nfs %s:%s %s" % (parser["nfs_ip"],parser["nfs_share_folder"],parser["local_nfs_path"])

		ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
						, parser["PrimaryOS_usr"]
						, parser["PrimaryOS_pwd"]) #獲得ssh

		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
		ssh.close()
		
def postprocess_slaveOS_vm(parser):	
	"""
	postprocess slaveOS vm part
	:param parser: is a dict, get from Test config file
	"""
	
	if parser["pos_check_slaveOS_VM"] == "yes":
		if parser["pos_slaveOS_VM_status"] == "running":
			postprocess_slaveOS_vm_running(parser)
		elif parser["pos_slaveOS_VM_status"] == "shut off":
			postprocess_slaveOS_vm_shutdown(parser)
		elif parser["pos_slaveOS_VM_status"] == "paused":
			pass	
		
def postprocess_slaveOS_vm_running(parser):
	"""
	Slave OS vm become running
	"""
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
								,parser["SlaveOS_usr"]
								,parser["SlaveOS_pwd"])
	
	if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh):
		print 59
	elif FTVM.is_shutoff(parser["vm_name"], parser["SlaveOS_ip"], ssh):
		print 56
		postprocess_slaveOS_vm_start(parser)
		print 57
		time.sleep(float(parser["pos_slaveOS_VM_boot_time"]))
	if not FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("SlaveOS VM: %s can not start" % parser["vm_name"])
	ssh.close()
def postprocess_slaveOS_vm_start(parser):
	"""
	according to fault tolerant level, postprocess vm start
	:called func: postprocess_hostOS_vm_running
	:param parser: is a dict, get from Test config file
	"""
	
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                        , parser["SlaveOS_usr"]
                        , parser["SlaveOS_pwd"]) #獲得ssh
	
	if parser["level"] == "0": #若為不開啟容錯機制之開機，則進入
		#print 58
		FTVM.start(parser["vm_name"], parser["SlaveOS_ip"], ssh)
		#print 58.5
	else:
		#print parser["level"]
		FTVM.ftstart(parser["vm_name"], parser["SlaveOS_ip"], parser["level"], ssh)
		#print 59
	ssh.close()
def postprocess_slaveOS_vm_shutdown(parser):
	"""
  	postprocess backupOS vm become shutdown

  	:called func: postprocess_backupOS_vm
  	:param parser: is a dict, get from Test config file
  	"""
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                            , parser["SlaveOS_usr"]
                            , parser["SlaveOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"],ssh):
		FTVM.destroy(parser["vm_name"], parser["SlaveOS_ip"],ssh)
		time.sleep(float(parser["pos_slaveOS_VM_shutdown_time"]))
	elif FTVM.is_paused(parser["vm_name"], parser["SlaveOS_ip"],ssh):	
		FTVM.resume(parser["vm_name"], parser["SlaveOS_ip"],ssh)
		FTVM.destroy(parser["vm_name"], parser["SlaveOS_ip"],ssh)
		time.sleep(float(parser["pos_slaveOS_VM_shutdown_time"]))
	times = 0	
	while times < 30:	
		if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh):
			print "destroy slave os vm "
			FTVM.destroy(parser["vm_name"], parser["SlaveOS_ip"],ssh)
			break;
		time.sleep(float(1))	
		times += 1
	if not FTVM.is_shutoff(parser["vm_name"], parser["SlaveOS_ip"],ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("SlaveOS %s can not shutdown" % parser["vm_name"])
	ssh.close()
			

def postprocess_slaveOS_FTsystem(parser):
	"""
  	postprocess backupOS FTsystem part
  
  	check FTsystem status 

  	start/stop FTsystem

  	raise exception if FTsystem can not start/stop

  	:called func: postprocess_backupOS_OS
  	:param parser: is a dict, get from Test config file
  	"""
	print parser["pos_check_slaveOS_FTsystem"]
	if parser["pos_check_slaveOS_FTsystem"] == "yes":
		ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh
		status = FTsystem.get_status(ssh)
		if status == "not running" and parser["pos_slaveOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數必需是running則進入
			FTsystem.start(ssh) #透過ssh開啟libvirt
		time.sleep(float(parser["pos_slaveOS_FTsystem_start_time"]))
		if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
			ssh.close()
			raise TA_error.Postprocess_Error("slaveOS FTsystem can not start")
		if status == "running" and parser["pos_slaveOS_FTsystem_start"] == "no": #若狀態為running且根據參數必需不是running則進入
			FTsystem.stop(ssh)
			time.sleep(float(parser["pos_slaveOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("slaveOS FTsystem can not stop")
		ssh.close()
		
		
def postprocess_slaveOS_HAAgent(parser):
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
	if HAagent.is_running(ssh, parser):
		HAagent.exit(parser, ssh)
		if HAagent.is_running(ssh, parser):
			ssh.close()
			raise TA_error.Postprocess_Error("Slave HAAgent cannot shutdown")
	else:
		pass

if __name__ == '__main__':
	#parser = {}
	#parser["BackupOS_ip"] = "192.168.1.25"
	#parser["BackupOS_usr"] = "user"
	#parser["BackupOS_pwd"] = "pdclab!@#$"
	#parser["vm_name"] = "T01"
	
	parser = {}
	parser["PrimaryOS_ip"] = "192.168.1.100"
	parser["PrimaryOS_usr"] = "primary"
	parser["PrimaryOS_pwd"] = "root"
	parser["NFS_ip"] = "192.168.1.29"
	parser["NFS_usr"] = "share"
	parser["NFS_pwd"] = "00000000"
	parser["cluster_file_path"] = "/var/ha/images/clusterFile.txt"
	parser["node_files_folder_path"] = "/var/ha/images/nodeFileFolder/"
	ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
	
	#NFS.reset(parser, ssh)
	#postProcessPrimaryOSReboot(parser)
	postprocess_hostOS_HAAgent(parser)
	print HAagent.is_running(ssh, parser)