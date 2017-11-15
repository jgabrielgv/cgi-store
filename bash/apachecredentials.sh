#!/bin/bash
userName=pf3895
#(1) Allow Apache access to the folders and the files.
sudo chgrp -R apache /var/www/html
sudo find /var/www/html -type d -exec chmod g+rx {} +
sudo find /var/www/html -type f -exec chmod g+r {} +
sudo find /var/www/html/cgi-bin/pages -type f -exec chmod g+rx {} +
sudo find /var/www/html/cgi-bin/js -type f -exec chmod g+rx {} +
sudo find /var/www/html/cgi-bin/css -type f -exec chmod g+rx {} +
#(2) Give your owner read/write privileges to the folders and the files, 
#and permit folder access to traverse the directory structure.
sudo chown -R ${userName} /var/www/html/
sudo find /var/www/html -type d -exec chmod u+rwx {} +
sudo find /var/www/html -type f -exec chmod u+rw {} +
#(3) (Optional) Make sure every new file after this is created with www-data as the 'access' user.
sudo find /var/www/html -type d -exec chmod g+s {} +
#(4) (Optional) Final security cleanup, if you don't want other users to be able to see the data
sudo chmod -R o-rwx /var/www/html/

#(5)assign permissions to a local folder to copy the cookies
mkdir -p /var/www/html/cgi-bin/Sites
mkdir -p /var/www/html/cgi-bin/Sites/session
sudo find /var/www/html/cgi-bin/Sites/session -type f -exec chmod u+rw {} +

mkdir -p /home/pf3895/Sites
mkdir -p /home/pf3895/Sites/session
sudo chown -R apache:apache /home/pf3895/Sites
#cd /home/pf3895/Sites
 
# File permissions, recursive
#find . -type f -exec chmod 0644 {} \;
 
# Dir permissions, recursive
#find . -type d -exec chmod 0755 {} \;
 
# SELinux serve files off Apache, resursive
#sudo chcon -t httpd_sys_content_t /home/pf3895/Sites -R
 
# Allow write only to specific dirs
sudo chcon -R -t httpd_sys_content_rw_t /home/pf3895/Sites/session

sudo semanage fcontext -a -t public_content_rw_t '/home/pf3895(/.*)?'
sudo restorecon -R /home/pf3895

#sudo chmod -R u=rwx /home/pf3895/Sites

