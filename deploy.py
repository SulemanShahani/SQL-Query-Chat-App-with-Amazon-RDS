
import os
from pyngrok import ngrok, conf
from dotenv import load_dotenv
import urllib.request
import zipfile

load_dotenv()

# Set a custom ngrok path
NGROK_BIN = "/tmp/ngrok"

# Ensure the ngrok binary directory exists
os.makedirs(os.path.dirname(NGROK_BIN), exist_ok=True)

# Download ngrok if not already present
if not os.path.exists(NGROK_BIN):
    ngrok_url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
    ngrok_zip = "/tmp/ngrok.zip"
    
    urllib.request.urlretrieve(ngrok_url, ngrok_zip)
    
    with zipfile.ZipFile(ngrok_zip, "r") as zip_ref:
        zip_ref.extractall("/tmp")
    
    os.rename("/tmp/ngrok", NGROK_BIN)
    os.chmod(NGROK_BIN, 0o755)  # Ensure the binary is executable

# Set the custom ngrok configuration
pyngrok_config = conf.PyngrokConfig(ngrok_path=NGROK_BIN)
conf.set_default(pyngrok_config)
import os

# Install required libraries
os.system('pip install -r requirements.txt')


from pyngrok import ngrok

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set ngrok authentication token
ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))



# Start ngrok to create a public URL for the Streamlit app
public_url = ngrok.connect(8501)
print(f"Streamlit app will be accessible at: {public_url}")

# Run the Streamlit app
os.system('streamlit run app.py')

# Print the ngrok public URL
print(f"Streamlit app running at: {public_url}")
