# Water project
for my raspberry pi controlled garden watering system

using virtual envirometnt or conda

enviroment is called

`waterproject`

export depedency lsit with pip
```bash
pip freeze > requirements.txt
```

create conda env with 
```bash
# conda create --name waterproject --file requirements.txt
 conda create --name waterproject  python=3.11
 pip install -r requirements.txt
```