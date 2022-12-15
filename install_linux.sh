#!bin/sh
echo "Installing venv"
python3 -m venv .venv

echo "Installing requirements"
.venv/bin/pip3 install -r requirements.txt

echo "Enter bot token:"
read token
echo "TOKEN = \"$token\"" > config.py

echo "Enter admin id:"
read admin
echo "TOKEN = $admin" >> config.py

echo "Installing completed!"