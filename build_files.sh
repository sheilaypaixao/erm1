echo "Building the project..."

curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python3.12 get-pip.py

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt