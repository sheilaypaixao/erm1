echo "Building the project..."

yum install python3-devel mysql-devel pkgconfig

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt