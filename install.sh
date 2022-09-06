#!/bin/bash
REPO_PATH=${1:="/Repos/hygrometer-reporter"}

echo "Installing Python requirements"
pip install -r ${REPO_PATH}/requirements.txt

echo "Installing systemd service"
cat << EOF > /etc/systemd/system/hygrometer.service;
[Unit]
Description=Hygrometer Reporter
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python main.py
WorkingDirectory=${REPO_PATH}
User=root

[Install]
WantedBy=multi-user.target
EOF

echo "Adding service to startup sequence and starting it now"
systemctl enable hygrometer.service
systemctl start hygrometer.service

echo "Done"