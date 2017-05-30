sudo sshpass -p 'root' ssh primary@192.168.1.25 'bash -s' < initP.sh
sudo sshpass -p 'root' ssh backup-node@192.168.1.27 'bash -s' < initB.sh
sudo sshpass -p 'root' ssh slave@192.168.1.28 'bash -s' < initS.sh



sudo sshpass -p 'root' ssh primary@192.168.1.25 'bash -s' < init.sh
#sudo sshpass -p 'root' ssh backup-node@192.168.1.101 'bash -s' < mm_initial.sh
#sudo sshpass -p 'root' ssh slave@192.168.1.102 'bash -s' < xxx_init.sh
