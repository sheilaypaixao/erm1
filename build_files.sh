echo "Building the project..."

yum install pkg-config
yum install make glibc-devel gcc patch
yum install mariadb105-devel

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt