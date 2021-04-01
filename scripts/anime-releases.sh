#!/bin/bash

cat <<EOF

     _          _                  ____      _
    / \   _ __ (_)_ __ ___   ___  |  _ \ ___| | ___  __ _ ___  ___  ___
   / _ \ | '_ \| | '_ \` _ \ / _ \ | |_) / _ \ |/ _ \/ _\` / __|/ _ \/ __|
  / ___ \| | | | | | | | | |  __/ |  _ <  __/ |  __/ (_| \__ \  __/\__ \\
 /_/   \_\_| |_|_|_| |_| |_|\___| |_| \_\___|_|\___|\__,_|___/\___||___/


EOF

cat <<EOF
Hello! You're currently running the anime-releases setup script. Before continuing,
be sure to have the following installed:
- Python (3.8+; this project doesn't use any specific Python 3.8 features, so you
  may be able to get away with 3+)
- Pip3 (to install Python packages)
- Docker + Docker Compose (Compose should be installed alongside Docker, but you may
  have to install it manually!)
- OPTIONAL: Redis (if you want to use your own Redis instance, or you could just run
  it using a container)

Enjoy! :)


EOF

# exit early if no arguments
if [ $# = 0 ]; then
  exit 0
fi

function install() {
  echo "Downloading docker-compose file..."
  curl -s -o docker-compose.yml \
    https://raw.githubusercontent.com/Sulaxan/anime-releases/master/webhook/docker-compose.yml

  echo "Downloading environment file..."
  curl -s -o ar.env \
    https://raw.githubusercontent.com/Sulaxan/anime-releases/master/webhook/ar.env
  echo "######################################################"
  echo "IMPORTANT! Before running, edit the ar.env file first!"
  echo "######################################################"
  sleep 2

  echo 'Done! Run the `run` (or `docker-compose up`) command to download the images and run the containers'
}

function fullInstall() {
  echo 'Currently not supported; use `install` instead'
}

function run() {
  docker-compose up -d
}


case $1 in
  "install")
    install
    ;;
  "fullinstall")
    fullInstall
    ;;
  "run")
    run
    ;;
esac

