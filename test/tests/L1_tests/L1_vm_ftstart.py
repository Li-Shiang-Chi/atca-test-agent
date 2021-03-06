from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_vm_ftstart(parser):
	"""
	test vm start 
	"""
	#preprocess
	preprocess.preprocess(parser)
	#process
	process.vm_ftstart(parser)
	#assert
	Assert.vm_running_in_hostOS(parser)
	Assert.vm_is_login_in_hostOS(parser)