#!/bin/bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce \
git \
docker-compose -y -y
groupadd docker
usermod -aG docker $USER
systemctl enable docker
git clone https://github.com/17011986/python_telegram_aws.git
myip=`curl http://169.254.169.254/latest/meta-data/public-ipv4`

cat <<EOF > /python_telegram_bot_lite/.env
  TOKEN=${TOKEN}
  ManheimLogin=${ManheimLogin}
  ManheimPass=${ManheimPass}
  REDIS_PASS=${REDIS_PASS}
  ADMIN_ID=${ADMIN_ID}
  CopartURL=${CopartURL}
  WEBHOOK_HOST=$myip
  WEBHOOK_PORT=443
EOF
cd python_telegram_bot_lite

openssl req -newkey rsa:2048 -sha256 -nodes  \
    -keyout url_private.key -x509 -days 3560 -out url_cert.pem  \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=$myip"
docker-compose -f docker-compose.yml up --build
