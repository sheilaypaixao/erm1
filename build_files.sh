echo "Building the project..."

curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python3.9 get-pip.py

python3.9 -m pip install -r requirements.txt