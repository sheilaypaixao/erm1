echo "Building the project..."

yum install pkg-config
yum install gcc
yum install -y mysql-devel

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt