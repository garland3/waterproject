echo "Starting the uvicorn server"
echo `pwd`
pip install -e .
source waterproject/bin/activate
uvicorn waterproject.C1_webserver:app --port 8000 --reload --host 0.0.0.0
