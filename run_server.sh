echo "Starting the uvicorn server"
echo `pwd`
source waterproject/bin/activate
uvicorn C1_webserver:app --port 8000 --reload --host 0.0.0.0
