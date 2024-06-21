echo "run as 'bash run_server.sh'"
echo "Starting the uvicorn server"
echo `pwd`
source waterproject/bin/activate
python -m pip install -e .
python -m uvicorn waterproject.C1_webserver:app --port 8000 --reload --host 0.0.0.0
