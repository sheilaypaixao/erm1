echo "Building the project..."

yum install pkgconfig

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt