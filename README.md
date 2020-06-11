# Coursera_Capstone
Capstone project for professional certificate in Data Science @ IBM

- app.py is the python script
- .jpg images are being used by the app
- requirements, config.toml, credentials.toml required to Streamlit
- setup.ph and Procfile are required to run at Heroku cloud
- Dockerfile has the configurations to build with docker

#Docker (optional)
Commands to type on the terminal in the folder of this repository:

- "docker build --tag capstone:latest ."
- "docker run --publish 8000:8080 --detach --name capstone capstone:latest"

Building an image with docker enables you to share the app to a website in the cloud (Azure, AWS, Google)