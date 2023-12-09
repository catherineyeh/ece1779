# App to demonstrate making API requests to deployed model on Azure ML Studio
Prerequesite: need to create .env file to store ```AZURE_API_KEY```.

## Steps to run locally
### Option 1
1. Create python virtual environment with ```python -m venv \path\to\venv```.
2. activate virtual environment ```source \path\to\venv\bin\activate```
3. ```pip install -r requirements.txt```
4. run ```python app.py```

### Option 2 - Use Docker image
https://hub.docker.com/repository/docker/catherineyeh/ece1779-project/general
1. ```docker-compose build```
2. ```docker-compose up -d```

# UI
<img width="721" alt="image" src="https://github.com/catherineyeh/ece1779/assets/33914784/5b8c009d-be8b-4e14-a651-8eeaa8b64d34">

