from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_HA3_low_temp_danger(parser):
    
    preprocess.run_preprocess(parser)
    print 110
    process.exec_low_temp_danger(parser)
    print 111
    Assert.vm_recover_in_backup_or_slave(parser)
    print 112
    Assert.primaryOS_role_is_slave(parser)
    print 113
    Assert.backupOS_role_is_primary(parser)
    print 114
    Assert.slaveOS_role_is_backup(parser)
    print 115