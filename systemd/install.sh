set -ev

mv .service.tmp $1
systemctl daemon-reload
systemctl enable $2
systemctl restart $2
