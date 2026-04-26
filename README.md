# Classification

# To clone the github repo to vscode
git clone https://github.com/yout-username/your-git-repo.git
cd your-repo
code .

# to create the python envirnoment in vscode
python -m venv venv

# to activate
venv\Scripts\activate

# to install requirements.txt
pip install -r requirements.txt

# to run docker image
docker-compose up --build

# To run FastAPI
uvicorn src.app:app --reload

# to run streamlite
streamlit run src/ui.py

# to open mlflow
mlflow ui 


What you need next

You now must:

Build Docker image locally
Tag it with Azure Container Registry
Push image to ACR
Deploy it (App Service or Container Instance)
🟢 STEP 1: Login to Azure from terminal
az login
🟢 STEP 2: Login to your ACR

Replace yourACRname with your registry name:

az acr login --name yourACRname
🟢 STEP 3: Build your Streamlit Docker image

From your project folder:

docker build -t iris-streamlit .
🟢 STEP 4: Tag image for ACR

Format:

docker tag iris-streamlit yourACRname.azurecr.io/iris-streamlit:v1

Example:

docker tag iris-streamlit myregistry.azurecr.io/iris-streamlit:v1
🟢 STEP 5: Push image to Azure
docker push yourACRname.azurecr.io/iris-streamlit:v1


STEP 6: Now deploy (choose one option)
🔵 OPTION A (EASY): Azure Container Instance (fastest)
az container create \
  --resource-group your-rg \
  --name iris-streamlit \
  --image yourACRname.azurecr.io/iris-streamlit:v1 \
  --dns-name-label iris-streamlit-app \
  --ports 8501

  az container create --resource-group classifier --name iris-streamlit --image classifier.azurecr.io/iris-streamlit:v1 --dns-name-label iris-streamlit-app --ports 8501 --os-type Linux --cpu 1 --memory 1.5

👉 Then open:

http://iris-streamlit-app.eastus.azurecontainer.io:8501
🔵 OPTION B (PRODUCTION): Azure App Service (Docker)
Go to Azure Portal
Create Web App
Choose:
Publish: Docker Container
Image: your ACR image


## STEP 1: Push BOTH Docker images to ACR
# 1. First move flask app
docker build -t iris-api -f dockerfile.api .
docker tag iris-api classifier.azurecr.io/iris-api:v1
docker push classifier.azurecr.io/iris-api:v1

# 2. Streamlit image
docker build -t iris-streamlit -f dockerfile.ui .
docker tag iris-streamlit classifier.azurecr.io/iris-streamlit:v1
docker push classifier.azurecr.io/iris-streamlit:v1

# STEP 2: Deploy FastAPI to Azure
 az container create --resource-group classifier --name iris-api --image classifier.azurecr.io/iris-api:v1 --dns-name-label iris-api --ports 8000 --os-type Linux --cpu 1 --memory 1.5

# STEP 3: Get FastAPI URL
After deployment, Azure will show: iris-api.eastus.azurecontainer.io
Your API URL becomes:
http://iris-api.eastus.azurecontainer.io:8000/docs

# STEP 4: Deploy Strimlite to Azure
az container create --resource-group classifier --name iris-streamlit --image classifier.azurecr.io/iris-streamlit:v1 --dns-name-label iris-streamlit-app --ports 8501 --os-type Linux --cpu 1 --memory 1.5