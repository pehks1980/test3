import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
PACKAGE_NAME = 'demclicker'

PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'

DAEMON_STATE=0
# note that user should have sudo

# Backup your /etc/sudoers file by typing the following command:
# sudo cp /etc/sudoers /root/sudoers.bak
# Edit the /etc/sudoers file by typing the visudo command:
# sudo visudo
# Append/edit the line as follows in the /etc/sudoers file for user named ‘vivek’ to run ‘/bin/kill’ and ‘systemctl’ commands:
# vivek ALL = NOPASSWD: /bin/systemctl restart httpd.service, /bin/kill
# in ubu it looks like this
#user    ALL=(ALL) NOPASSWD: /usr/bin/docker, /bin/systemctl start smbd, /bin/systemctl stop smbd, /bin/systemctl restart smbd

DAEMON_CMD_RUN='sudo /bin/systemctl start smbd'
DAEMON_CMD_STOP='sudo /bin/systemctl stop smbd'
DAEMON_CMD_RESTART='sudo /bin/systemctl restart smbd'
DAEMON_CMD_CHECK='/bin/systemctl status smbd'

LOG_ROTATE = 0 #0
LOG_TO = 'FILE' #'SYSLOG'#'FILE'
LOG_NAME = 'demclicker.log'

DUMP_FILE='dumps.json'