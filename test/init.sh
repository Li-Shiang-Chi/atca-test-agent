sudo mmsh createcluster test_c primary 85 127.0.0.1
sudo mmsh addnode test_c backup 192.168.1.27 86
sudo mmsh addnode test_c slave 192.168.1.28 87
