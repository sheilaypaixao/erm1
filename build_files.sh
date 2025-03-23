echo "Building the project..."
curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

pip install -r requirements.txt