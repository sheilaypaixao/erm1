echo "Building the project..."

yum install mariadb-dev pkg-config

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt