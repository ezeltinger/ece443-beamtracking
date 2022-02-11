dpkg -s python3.8-venv
var="$?"
echo $var
if [ $var != "0" ]; then 
    sudo apt install -y python3.8-venv
fi
python3 -m venv ../py-env
source ../py-env/bin/activate
pip install -r ../requirements.txt
pip freeze
