sudo rm /var/ha/images/clusterFile.txt
sudo rm -rf /var/ha/images/nodeFileFolder/
sudo systemctl restart HAAgent.service
#ROLE="primary"
#OUTPUT="./a.out"
#pid=0
#ps -ef | grep HAAgent.py | awk '{if(NR==1) print $2}' >> $OUTPUT
#pid=$(<$OUTPUT)
#echo $pid
#sudo rm $OUTPUT
#sudo kill -9 $pid
#sudo rm /home/$ROLE/Desktop/pid.txt
#/etc/profile.d/HAagent.sh


