echo "Building the project..."

curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python3.12 get-pip.py

apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

python3.12 -m pip install -r requirements.txt