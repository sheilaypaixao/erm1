echo "Building the project..."

#yum install mariadb105-devel
#mysql_config --cflags
#mysql_config --libs

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt