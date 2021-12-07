sudo chmod -R a+rwX /home

sudo cp image_pred.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable image_pred.service
sudo systemctl start image_pred.service

