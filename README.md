## FastAPI Mongo(pymongo) DB CRUD Application ##

#### Pre requisites ####
- you must have preinstalled python3 preferably (3.8+) in your machine
- you must have running mongo db server on the localhost port 27017.

#### Clone the repo ####
```
$ git clone https://github.com/ecedreamer/fastapi-pymongo-crud.git

# move to the cloned project directory
$ cd fastapi_mongo_crud
```
#### Make a Python Virtual Environment ####
```
$ python3 -m venv venv
```
#### Activate the Python Virtual Environment ####
```
# in linux or mac
$ source venv/bin/activate 

# windows
$ venv\scripts\activate
```
#### Install the dependencies ####
```
$ pip install -r requirements.txt

# if fails, try below
$ pip install fastapi uvicorn pymongo
```
#### To Run the server ####
```
$ python server.py
```

#### View the API Docs ####
Go to your browser and open http://127.0.0.1:8000/docs 
