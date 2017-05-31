#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import time
import shell_server
import FTsystem
import FTVM
import FTOS
import master_monitor
import mmsh
import TA_error
import subprocess
import HAagent
import NFS



def run_preprocess(parser):
    print "nodes"
    preprocess_nodes(parser)
    print "mm"
    preprocess_mm(parser)
    print "host"
    preprocess_Host(parser)
    print "backup"
    preprocess_Backup(parser)
    print "slave"
    preprocess_Slave(parser)
    print "nfs"
    preprocess_NFS(parser)

def preprocess_nodes(parser):
    """
    check every node is alive and  ssh accessible
    :param parser : is a dict , get from test config file
    """
    print "host node"
    preprocess_host_OS(parser)  
    print "backup node" 
    preprocess_backup_OS(parser)
    print "slave node" 
    preprocess_slave_OS(parser)
    print "nfs node"
    preprocess_NFS_OS(parser)
    
def preprocess_Host(parser):
    """
    when test case start host node do some preprocess
    :param parser : is a dict , get from test config file
    """
    
    preprocess_host_OS(parser)
    preprocess_hostOS_Mount(parser)
    preprocess_hostOS_HAagent(parser)
    preprocess_hostOS_vm(parser)
    preprocess_hostOS_FTsystem(parser)
    
def preprocess_Backup(parser):
    """
    when test case start backup node do some preprocess
    :param parser : is a dict , get from test config file
    """
    preprocess_backup_OS(parser) 
    preprocess_backupOS_Mount(parser)
    preprocess_backupOS_HAagent(parser)
    preprocess_backupOS_vm(parser)
    preprocess_backupOS_FTsystem(parser)
    
def preprocess_Slave(parser):
    """
    when test case start slave node do some preprocess
    :param parser : is a dict , get from test config file
    """
    preprocess_slave_OS(parser)
    preprocess_slaveOS_Mount(parser)
    preprocess_slaveOS_HAagent(parser)
    preprocess_slaveOS_vm(parser)
    preprocess_slaveOS_FTsystem(parser)

def preprocess_NFS(parser):
    preprocess_NFS_OS(parser)

def preprocess_host_OS(parser):
    """
    preprocess  , Host os part , check Host node is booted and ssh accessible
    :param parser : is a dict , get from test config file
    """

    if FTOS.OS_is_running(parser["PrimaryOS_ip"], parser) == False:
        if parser["IPMI_supported"] == "yes":
            ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
            FTOS.IPMI_boot(parser["PrimaryOS_ipmb"], ssh)
            ssh.close()
        elif parser["IPMI_supported"] == "no":
            FTOS.L1_boot(parser["PrimaryOS_NetworkAdaptor"])
    if FTOS.OS_is_running(parser["PrimaryOS_ip"], parser) == False:
        raise TA_error.Preprocess_Error("PrimaryOS node cannot boot")
    if FTOS.ssh_is_ready(parser["PrimaryOS_ip"], parser["PrimaryOS_usr"], parser["PrimaryOS_pwd"], parser) == False:
        raise TA_error.Preprocess_Error("Host node ssh can not access")
    
def preprocess_hostOS_Mount(parser):
    """
    preprocess , check Host node is mounting to nfs
    :param parser : is a dict , get from test config file
    """
    
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                        , parser["PrimaryOS_usr"]
                        , parser["PrimaryOS_pwd"]) #獲得ssh
    
    if preprocess_is_OS_Mount_NFS(parser , ssh) == False: # check node is mount to nfs
        preprocess_OS_Mount_NFS(parser , ssh) # mount to nfs
    if preprocess_is_OS_Mount_NFS(parser , ssh) == False: # re check node is mount to nfs
        raise TA_error.Preprocess_Error("Host os not mount to nfs") # not mount to nfs , raise error
    ssh.close()
    
def preprocess_backup_OS(parser):
    """
    preprocess  , backup os part , check backup node is booted and ssh accessible
    :param parser : is a dict , get from test config file
    """
    if FTOS.OS_is_running(parser["BackupOS_ip"], parser) == False:
        if parser["IPMI_supported"] == "yes":
            ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
            FTOS.IPMI_boot(parser["BackupOS_ipmb"], ssh)
            ssh.close()
        elif parser["IPMI_supported"] == "no":
            FTOS.L1_boot(parser["BackupOS_NetworkAdaptor"])
    if FTOS.OS_is_running(parser["BackupOS_ip"], parser) == False:
        raise TA_error.Preprocess_Error("BackupOS node cannot boot")
    if FTOS.ssh_is_ready(parser["BackupOS_ip"], parser["BackupOS_usr"], parser["BackupOS_pwd"], parser) == False:
        raise TA_error.Preprocess_Error("Backup node ssh can not access")
    
def preprocess_backupOS_Mount(parser):
    """
    preprocess , check backup node is mounting to nfs
    :param parser : is a dict , get from test config file
    """
    
    ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                                  , parser["BackupOS_usr"]
                                  , parser["BackupOS_pwd"]) #獲得ssh
    if preprocess_is_OS_Mount_NFS(parser , ssh) == False: # check node is mount to nfs
        preprocess_OS_Mount_NFS(parser , ssh) # mount to nfs
    if preprocess_is_OS_Mount_NFS(parser , ssh) == False: # re check node is mount to nfs
        raise TA_error.Preprocess_Error("Host os not mount to nfs") # not mount to nfs , raise error
    ssh.close()
    
def preprocess_slave_OS(parser):
    """
    preprocess  , Host os part , check slave node is booted
    :param parser : is a dict , get from test config file
    """
    if FTOS.OS_is_running(parser["SlaveOS_ip"], parser) == False:
        if parser["IPMI_supported"] == "yes":
            ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh 
            FTOS.IPMI_boot(parser["SlaveOS_ipmb"], ssh)
            ssh.close()
        elif parser["IPMI_supported"] == "no":
            FTOS.L1_boot(parser["SlaveOS_NetworkAdaptor"])
    if FTOS.OS_is_running(parser["SlaveOS_ip"], parser) == False:
        raise TA_error.Preprocess_Error("SlaveOS node cannot boot")
    if FTOS.ssh_is_ready(parser["SlaveOS_ip"], parser["SlaveOS_usr"], parser["SlaveOS_pwd"], parser) == False:
        raise TA_error.Preprocess_Error("Slave node ssh can not access")
def preprocess_slaveOS_Mount(parser):
    """
    preprocess , slave Host node is mounting to nfs
    :param parser : is a dict , get from test config file
    """
    ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                                  , parser["SlaveOS_usr"]
                                  , parser["SlaveOS_pwd"]) #獲得ssh 
    
    if preprocess_is_OS_Mount_NFS(parser , ssh) == False: # check node is mount to nfs
        preprocess_OS_Mount_NFS(parser , ssh) # mount to nfs
    if preprocess_is_OS_Mount_NFS(parser , ssh) == False: # re check node is mount to nfs
        raise TA_error.Preprocess_Error("Host os not mount to nfs") # not mount to nfs , raise error
    ssh.close()

def preprocess_NFS_OS(parser):
    if FTOS.OS_is_running(parser["NFS_ip"], parser) == False:
        #FTOS.L1_boot(parser["NFS_NetworkAdaptor"])
        if FTOS.OS_is_running(parser["NFS_ip"], parser) == False:
            raise TA_error.Preprocess_Error("NFS node can not start")
    if FTOS.ssh_is_ready(parser["NFS_ip"], parser["NFS_usr"], parser["NFS_pwd"], parser) == False:
        raise TA_error.Preprocess_Error("NFS node ssh can not access")
    
    ssh = shell_server.get_ssh(parser["NFS_ip"]
                                  , parser["NFS_usr"]
                                  , parser["NFS_pwd"]) #獲得ssh 
    
def preprocess_OS_Mount_NFS(parser , ssh = None):
    cmd = "mount -t nfs %s:%s %s" % (parser["NFS_ip"],parser["NFS_share_folder"],parser["NFS_local_path"])
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
       
def preprocess_is_OS_Mount_NFS(parser , ssh = None):
    cmd = "ls %s" % parser["NFS_local_path"]
    t_start = time.time()
    while (time.time() - t_start) < parser["pre_node_wait_mount_nfs_time"]: # use while loop to check , once mounted break the loop
        time.sleep(1) # check each sec
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
        if s_stdout != "":
            return True
    return False

def preprocess_hostOS_HAagent(parser):
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                                  , parser["PrimaryOS_usr"]
                                  , parser["PrimaryOS_pwd"]) #獲得ssh 
    if HAagent.is_running(ssh, parser):
        ssh.close()
        return True
    ssh.close()
    raise TA_error.Preprocess_Error("Host OS HAAgent process not ready")

def preprocess_backupOS_HAagent(parser):
    ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                                  , parser["BackupOS_usr"]
                                  , parser["BackupOS_pwd"]) #獲得ssh 
    if HAagent.is_running(ssh, parser):
        ssh.close()
        return True
    ssh.close()
    raise TA_error.Preprocess_Error("Backup OS HAAgent process not ready")

def preprocess_slaveOS_HAagent(parser):
    ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                                  , parser["SlaveOS_usr"]
                                  , parser["SlaveOS_pwd"]) #獲得ssh 
    if HAagent.is_running(ssh, parser):
        ssh.close()
        return True
    ssh.close()
    raise TA_error.Preprocess_Error("Slave OS HAAgent process not ready")
    
def preprocess(parser):
    """
    when test case start, preprocess something
    :param parser: is a dict, get from Test config file
    """
    preprocess_mm(parser)
    print "pre"
    preprocess_hostOS(parser)
    print "pre1"
    preprocess_backupOS(parser)


def preprocess_mm(parser):
    """
    preprocess master monitor part

    :called func: preprocess
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_mm"] == "yes": #若需確認master monitor之狀態，則進入
        if master_monitor.get_status() != "running":
            #master_monitor.temp_start()
            time.sleep(float(parser["pre_mm_start_time"]))
            if master_monitor.get_status() != "running":
                raise TA_error.Preprocess_Error("master monitor can not start")

    if parser["pre_init_mm"] == "yes":
        #print 99
        cmd = "bash initAll.sh"
        status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
        #print status
        #print 100
    if parser["pre_init_mm"] == "no":
        #print 99
        cmd = "bash non_mm_initAll.sh"
        status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
        #print status
        #print 100
    

def preprocess_hostOS(parser):
    """
    preprocess PrimaryOS

    :called func: preprocess
    :param parser: is a dict, get from Test config file
    """
    #preprocess_hostOS_hw(parser)
    """
    because of some unknow problem of FTKVM , we can't check PrimaryOS status 
    """
    preprocess_hostOS_OS(parser)
  
    #preprocess_hostOS_wd(parser)
    print 46
    preprocess_hostOS_FTsystem(parser)
    print 47
    preprocess_hostOS_vm(parser)
    print 48

def preprocess_backupOS(parser):
    """
    preprocess backupOS

    :called func: preprocess
    :param parser: is a dict, get from Test config file
    """
    #preprocess_backupOS_OS(parser)
    #preprocess_backupOS_FTsystem(parser)
    #print 9
    preprocess_backupOS_vm(parser)
    #print 10
def preprocess_hostOS_hw(parser):
    """
    perprocess hostOS hardware part

    :called func: preprocess_hostOS
    :param parser: is a dict, get from Test config file
      """
    if parser["pre_check_hostOS_hw"] == "yes":
        if mmsh.stateshmgr(parser["PrimaryOS_shmgr_name"]) == "stop":
            raise TA_error.Preprocess_Error("PrimaryOS hw shmgr stop")
        if mmsh.stateipmc(parser["PrimaryOS_ipmc_name"]) == "stop":
            raise TA_error.Preprocess_Error("PrimaryOS hw ipmc stop")

def preprocess_hostOS_OS(parser):
    """
    preprocess hostOS OS part

    :called func: preprocess_hostOS
    :param parser: is a dict, get from Test config file 
    """
    if parser["pre_check_FT_hostOS"] == "yes":
        if parser["pre_FT_hostOS_status"] == "running":
            preprocess_hostOS_OS_boot(parser)
        elif parser["pre_FT_hostOS_status"] == "shutdown":
            preprocess_hostOS_OS_shutdown(parser)

def preprocess_hostOS_OS_boot(parser):
    """
    preprocess hostOS OS boot part

    :called func: preprocess_hostOS_OS
    :param parser: is a dict, get from Test config file
    """
    if not FTOS.is_running(parser["PrimaryOS_name"]):
        if FTOS.is_shutdown(parser["PrimaryOS_name"]):
            status = FTOS.boot(parser["PrimaryOS_name"])
            if status != "success":
                raise TA_error.Preprocess_Error("PrimaryOS OS boot command fail")
        time.sleep(float(parser["pre_hostOS_boot_time"]))
    if not FTOS.is_running(parser["PrimaryOS_name"]):
        raise TA_error.Preprocess_Error("PrimaryOS OS can not boot")
  

def preprocess_hostOS_OS_shutdown(parser):
    """
    preprocess hostOS OS shutdown part

    :called func: preprocess_hostOS_OS
    :param parser: is a dict, get from Test config file
    """
    if not FTOS.is_shutdown(parser["PrimaryOS_name"]): #若host不為關機狀態
        if FTOS.is_running(parser["PrimaryOS_name"]):
            status = FTOS.shutdown(parser["PrimaryOS_name"])
            if status != "success":
                raise TA_error.Preprocess_Error("PrimaryOS OS shutdown command fail")
        time.sleep(float(parser["pre_hostOS_shutdown_time"]))
        if not FTOS.is_shutdown(parser["PrimaryOS_name"]):
            raise TA_error.Preprocess_Error("PrimaryOS OS can not shutdown")

def preprocess_backupOS_OS(parser):
    """
    preprocess backupOS OS part

    :called func: preprocess_backupOS_OS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_FT_hostOS"] == "yes":
        if parser["pre_FT_hostOS_status"] == "running":
            preprocess_hostOS_OS_boot(parser)
        elif parser["pre_FT_hostOS_status"] == "shutdown":
            pass

def preprocess_backupOS_OS_boot(parser):
    """
    preprocess backupOS OS boot

    :called func: preprocess_hostOS_OS
    :param parser: is a dict, get from Test config file
    """
    if not FTOS.is_running(parser["BackupOS_name"]):
        if FTOS.is_shutdown(parser["BackupOS_name"]):
            status = FTOS.boot(parser["BackupOS_name"])
            if status != "success":
                raise TA_error.Preprocess_Error("BackupOS OS boot command fail")
        time.sleep(float(parser["pre_backupOS_boot_time"]))
        if not FTOS.is_running(parser["BackupOS_name"]):
            raise TA_error.Preprocess_Error("BackupOS OS can not boot")

def preprocess_hostOS_wd(parser):
    """
    preprocess watchdog for fault tolerant hardware part

    :called func: preprocess_hostOS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_hostOS_hw"] == "yes":
        if mmsh.statewd(parser["PrimaryOS_name"]) == "stop":
            status = mmsh.startwd(parser["PrimaryOS_name"])
            if status != "success":
                raise TA_error.Preprocess_Error("PrimaryOS watchdog process can not start")
  

def preprocess_hostOS_FTsystem(parser):
    """
    preprocess PrimaryOS FTsystem part
  
    check FTsystem status 

    start/stop FTsystem

    raise exception if FTsystem can not start/stop

    :called func: preprocess_hostOS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_hostOS_FTsystem"] == "yes":
        ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                              , parser["PrimaryOS_usr"]
                              , parser["PrimaryOS_pwd"]) #獲得ssh
        status = FTsystem.get_status(ssh)
        if status == "not running" and parser["pre_hostOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數必需是running則進入
            FTsystem.start(ssh) #透過ssh開啟libvirt
            time.sleep(float(parser["pre_hostOS_FTsystem_start_time"]))
        if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
            ssh.close()
            raise TA_error.Preprocess_Error("PrimaryOS FTsystem can not start")
        if status == "running" and parser["pre_hostOS_FTsystem_start"] == "no": #若狀態為running且根據參數必需不是running則進入
            FTsystem.stop(ssh)
            time.sleep(float(parser["pre_hostOS_FTsystem_start_time"]))
            if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
                ssh.close()
                raise TA_error.Preprocess_Error("PrimaryOS FTsystem can not stop")
        ssh.close()

def preprocess_backupOS_FTsystem(parser):
    """
    preprocess backupOS FTsystem part
  
    check FTsystem status 

    start/stop FTsystem

    raise exception if FTsystem can not start/stop

    :called func: preprocess_backupOS_OS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_backupOS_FTsystem"] == "yes":
        ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
        status = FTsystem.get_status(ssh)
        if status == "not running" and parser["pre_backupOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數必需是running則進入
            FTsystem.start(ssh) #透過ssh開啟libvirt
            time.sleep(float(parser["pre_backupOS_FTsystem_start_time"]))
        if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
            ssh.close()
            raise TA_error.Preprocess_Error("backupOS FTsystem can not start")
        if status == "running" and parser["pre_backupOS_FTsystem_start"] == "no": #若狀態為running且根據參數必需不是running則進入
            FTsystem.stop(ssh)
            time.sleep(float(parser["pre_backupOS_FTsystem_start_time"]))
            if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
                ssh.close()
                raise TA_error.Preprocess_Error("backupOS FTsystem can not stop")
    ssh.close()
  

def preprocess_hostOS_vm(parser):
    """
    preprocess hostOS vm part

    :called func: preprocess_hostOS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_hostOS_VM"] == "yes":
        if parser["pre_hostOS_VM_status"] == "running":
            print 51
            preprocess_hostOS_vm_running(parser)
        if parser["pre_hostOS_VM_login"] == "yes":
            print 52
            preprocess_hostOS_vm_login(parser)
            print 53
        elif parser["pre_hostOS_VM_status"] == "shut off":
            preprocess_hostOS_vm_shutdown(parser)
        elif parser["pre_hostOS_VM_status"] == "paused":
            pass


def preprocess_hostOS_vm_running(parser):
    """
    preprocess vm become running

    :called func: preprocess_hostOS_vm
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                            , parser["PrimaryOS_usr"]
                            , parser["PrimaryOS_pwd"]) #獲得ssh

    if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
        print 59
        if "pre_hostOS_VM_restart" in parser.keys() and parser["pre_hostOS_VM_restart"] == "yes": #根據參數若VM需重新啟動
            print 54
            prepocess_hostOS_vm_restart(parser)
            print 55
            time.sleep(float(parser["pre_hostOS_VM_boot_time"]))
    elif FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
        print 56
        prepocess_hostOS_vm_start(parser)
        print 57
        time.sleep(float(parser["pre_hostOS_VM_boot_time"]))
    print 58
    if not FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
        ssh.close()
        raise TA_error.Preprocess_Error("PrimaryOS VM: %s can not start" % parser["vm_name"])
    
    ssh.close()

def prepocess_hostOS_vm_start(parser):
    """
    according to fault tolerant level, preprocess vm start

    :called func: preprocess_hostOS_vm_running
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                        , parser["PrimaryOS_usr"]
                        , parser["PrimaryOS_pwd"]) #獲得ssh

    if parser["level"] == "0": #若為不開啟容錯機制之開機，則進入
        #print 58
        FTVM.start(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
        #print 58.5
    else:
        #print parser["level"]
        print "host ftstart"
        FTVM.ftstart(parser["PrimaryOS_name"],parser["vm_name"], parser["PrimaryOS_ip"], ssh)
        #print 59
    ssh.close()

def prepocess_hostOS_vm_restart(parser):
    """
    according to fault tolerant level, preprocess vm restart

    :called func: preprocess_hostOS_vm_running
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                        , parser["PrimaryOS_usr"]
                        , parser["PrimaryOS_pwd"]) #獲得ssh

    if parser["level"] == "0": #若為不開啟容錯機制之重新啟動，則進入
        FTVM.restart(parser["vm_name"], parser["PrimaryOS_ip"],ssh)
    else:
        FTVM.ftrestart(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
    ssh.close()

def preprocess_hostOS_vm_shutdown(parser):
    """
    preprocess hostOS vm become shutdown

    :called func: preprocess_hostOS_vm
    :param parser: is a dict, get from Test config file
    """

    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                        , parser["PrimaryOS_usr"]
                        , parser["PrimaryOS_pwd"]) #獲得ssh
    if FTVM.is_running(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
        FTVM.destroy(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
        time.sleep(float(parser["pre_hostOS_VM_shutdown_time"]))
    elif FTVM.is_paused(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
        FTVM.resume(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
        FTVM.destroy(parser["vm_name"], parser["PrimaryOS_ip"], ssh)
        time.sleep(float(parser["pre_hostOS_VM_shutdown_time"]))
    if not FTVM.is_shutoff(parser["vm_name"], parser["PrimaryOS_ip"], ssh):
        ssh.close()
        raise TA_error.Preprocess_Error("PrimaryOS %s can not shutdown" % parser["vm_name"])
    ssh.close()

def preprocess_hostOS_vm_login(parser):
    """
    preprocess check hostOS vm is login

    :called func: preprocess_hostOS_OS_vm
    :param parser: is a dict, get from Test config file
    """
    if not FTVM.is_login(parser["vm_name"]
                  , parser["TA_ip"]
                  , parser["TA_msg_sock_port"]
                  , int(parser["pre_hostOS_VM_login_time"])):
        raise TA_error.Preprocess_Error("PrimaryOS %s is not login" % parser["vm_name"])

def preprocess_backupOS_vm(parser):
    """
    preprocess backupOS vm

    :called func: preprocess_backupOS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_backupOS_VM"] == "yes":
        if parser["pre_backupOS_VM_status"] == "running":
            preprocess_backupOS_vm_running(parser)
        elif parser["pre_backupOS_VM_status"] == "shut off":
            preprocess_backupOS_vm_shutdown(parser)
        elif parser["pre_backupOS_VM_status"] == "paused":
            pass

def preprocess_backupOS_vm_shutdown(parser):
    """
    preprocess backupOS vm become shutdown

    :called func: preprocess_backupOS_vm
    :param parser: is a dict, get from Test config file
    """
    print "GG"
    ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                            , parser["BackupOS_usr"]
                            , parser["BackupOS_pwd"]) #獲得ssh
    if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"],ssh):
        FTVM.destroy(parser["vm_name"], parser["BackupOS_ip"],ssh)
        time.sleep(float(parser["pre_backupOS_VM_shutdown_time"]))
    elif FTVM.is_paused(parser["vm_name"], parser["BackupOS_ip"],ssh):
        FTVM.resume(parser["vm_name"], parser["BackupOS_ip"],ssh)
        FTVM.destroy(parser["vm_name"], parser["BackupOS_ip"],ssh)
        time.sleep(float(parser["pre_backupOS_VM_shutdown_time"]))
    if not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"],ssh):
        ssh.close()
        raise TA_error.Preprocess_Error("backupOS %s can not shutdown" % parser["vm_name"])
    ssh.close()

def preprocess_backupOS_vm_running(parser):
    """
    according to fault tolerant level, preprocess vm start

    :called func: preprocess_hostOS_vm_running
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                          , parser["PrimaryOS_usr"]
                          , parser["PrimaryOS_pwd"]) #獲得ssh
    if parser["level"] == "0": #若為不開啟容錯機制之開機，則進入
        FTVM.start(parser["vm_name"], parser["BackupOS_ip"], ssh)
    else:
        FTVM.ftstart(parser["BackupOS_name"],parser["vm_name"], parser["BackupOS_ip"], ssh)
    ssh.close()
  
  
  
def preprocess_slaveOS_vm(parser):
    """
    preprocess hostOS vm part

    :called func: preprocess_hostOS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_slaveOS_VM"] == "yes":
        if parser["pre_slaveOS_VM_status"] == "running":
            preprocess_slaveOS_vm_running(parser)
    elif parser["pre_slaveOS_VM_status"] == "shut off":
        preprocess_slaveOS_vm_shutdown(parser)
    elif parser["pre_slaveOS_VM_status"] == "paused":
        pass
  
def preprocess_slaveOS_vm_running(parser):
    """
    preprocess vm become running

    :called func: preprocess_slaveOS_vm
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                            , parser["SlaveOS_usr"]
                            , parser["SlaveOS_pwd"]) #獲得ssh

    if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh):
        pass
        print 59
    elif FTVM.is_shutoff(parser["vm_name"], parser["SlaveOS_ip"], ssh):
        print 56
        prepocess_slaveOS_vm_start(parser)
        print 57
        time.sleep(float(parser["pre_slaveOS_VM_boot_time"]))
    print 58
    if not FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"], ssh):
        ssh.close()
        raise TA_error.Preprocess_Error("SlaveOS VM: %s can not start" % parser["vm_name"])
    ssh.close()


def prepocess_slaveOS_vm_start(parser):
    """
    according to fault tolerant level, preprocess vm start

    :called func: preprocess_hostOS_vm_running
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["PrimaryOS_ip"]
                        , parser["PrimaryOS_usr"]
                        , parser["PrimaryOS_pwd"]) #獲得ssh

    if parser["level"] == "0": #若為不開啟容錯機制之開機，則進入
        #print 58
        FTVM.start(parser["vm_name"], parser["SlaveOS_ip"], ssh)
        #print 58.5
    else:
        #print parser["level"]
        FTVM.ftstart(parser["SlaveOS_name"],parser["vm_name"], parser["SlaveOS_ip"], ssh)
        #print 59
    ssh.close()

def preprocess_slaveOS_vm_shutdown(parser):
    """
    preprocess backupOS vm become shutdown

    :called func: preprocess_backupOS_vm
    :param parser: is a dict, get from Test config file
    """
    ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                            , parser["SlaveOS_usr"]
                            , parser["SlaveOS_pwd"]) #獲得ssh
    if FTVM.is_running(parser["vm_name"], parser["SlaveOS_ip"],ssh):
        FTVM.destroy(parser["vm_name"], parser["SlaveOS_ip"],ssh)
        time.sleep(float(parser["pre_slaveOS_VM_shutdown_time"]))
    elif FTVM.is_paused(parser["vm_name"], parser["SlaveOS_ip"],ssh):
        FTVM.resume(parser["vm_name"], parser["SlaveOS_ip"],ssh)
        FTVM.destroy(parser["vm_name"], parser["SlaveOS_ip"],ssh)
        time.sleep(float(parser["pre_slaveOS_VM_shutdown_time"]))
    if not FTVM.is_shutoff(parser["vm_name"], parser["SlaveOS_ip"],ssh):
        ssh.close()
        raise TA_error.Preprocess_Error("SlaveOS %s can not shutdown" % parser["vm_name"])
    ssh.close()

def preprocess_slaveOS_FTsystem(parser):
    """
    preprocess backupOS FTsystem part
  
    check FTsystem status 

    start/stop FTsystem

    raise exception if FTsystem can not start/stop

    :called func: preprocess_backupOS_OS
    :param parser: is a dict, get from Test config file
    """
    if parser["pre_check_slaveOS_FTsystem"] == "yes":
        ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh
        status = FTsystem.get_status(ssh)
        if status == "not running" and parser["pre_slaveOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數必需是running則進入
            FTsystem.start(ssh) #透過ssh開啟libvirt
            time.sleep(float(parser["pre_slaveOS_FTsystem_start_time"]))
        if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
            ssh.close()
            raise TA_error.Preprocess_Error("slaveOS FTsystem can not start")
        if status == "running" and parser["pre_slaveOS_FTsystem_start"] == "no": #若狀態為running且根據參數必需不是running則進入
            FTsystem.stop(ssh)
            time.sleep(float(parser["pre_slaveOS_FTsystem_start_time"]))
            if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
                ssh.close()
                raise TA_error.Preprocess_Error("slaveOS FTsystem can not stop")
    ssh.close()
    

if __name__ == '__main__':
  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect("140.115.53.42", username="ting", password="oolabting")
  #s_stdin, s_stdout, s_stderr = ssh.exec_command("service libvirt-bin status | egrep -oi '([0-9]+)$'")
  #print "output", s_stdout.read()
  s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo service libvirt-bin start")
  #print s_stdout.readlines()
  ssh.close()