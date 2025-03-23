echo "Building the project..."

yum install yum python3-dev default-libmysqlclient-dev build-essential pkg-config

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt