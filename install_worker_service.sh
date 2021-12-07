sudo chmod -R a+rwX /home

sudo cp worker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable worker.service
sudo systemctl start worker.service

