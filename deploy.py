import os
import urllib.request
import zipfile
import subprocess
from pyngrok import ngrok, conf
from dotenv import load_dotenv

load_dotenv()

# Set a custom ngrok path
NGROK_BIN = "/tmp/ngrok/ngrok"
NGROK_URL = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
NGROK_ZIP = "/tmp/ngrok.zip"

# Ensure the ngrok binary directory exists
os.makedirs(os.path.dirname(NGROK_BIN), exist_ok=True)

# Download ngrok if not already present or check if an update is required
if not os.path.exists(NGROK_BIN):
    try:
        print("Downloading ngrok...")
        urllib.request.urlretrieve(NGROK_URL, NGROK_ZIP)

        with zipfile.ZipFile(NGROK_ZIP, "r") as zip_ref:
            zip_ref.extractall("/tmp/ngrok")

        os.chmod(NGROK_BIN, 0o755)  # Ensure the binary is executable
        print("ngrok downloaded and installed successfully.")
    except Exception as e:
        print(f"Failed to download and install ngrok: {e}")
        raise
else:
    try:
        # Check the current ngrok version
        current_version = subprocess.check_output([NGROK_BIN, "version"], text=True).strip()
        print(f"Current ngrok version: {current_version}")

        # Check if the installed version meets the minimum requirement
        if "2." in current_version:
            print("Updating ngrok to the latest version...")
            subprocess.run([NGROK_BIN, "update"], check=True)
            print("ngrok updated successfully.")
        elif "3.2." in current_version or "3.3." in current_version:
            print("ngrok version meets requirements.")
        else:
            raise ValueError(f"Unsupported ngrok version: {current_version}")
    except Exception as e:
        print(f"Failed to update ngrok: {e}")
        raise

# Set the custom ngrok configuration
pyngrok_config = conf.PyngrokConfig(ngrok_path=NGROK_BIN)
conf.set_default(pyngrok_config)

# Set ngrok authentication token
ngrok_auth_token = os.getenv("NGROK_AUTH_TOKEN")
# Update ngrok to the latest version
print("Updating ngrok to the latest version...")
ngrok_version = ngrok.get_version()
if ngrok_version.startswith('2.'):
    ngrok.kill()

# Wait for ngrok to be ready
print("Waiting for ngrok to be ready...")
ngrok_tunnel = None
while ngrok_tunnel is None:
    try:
        ngrok_tunnel = ngrok.connect(8501)
    except Exception as e:
        print(f"Failed to connect to ngrok: {e}")
        time.sleep(2)  # Wait for 2 seconds before retrying

# Once connected, get the public URL
public_url = ngrok_tunnel.public_url
print(f"Streamlit app is live at: {public_url}")

# Start ngrok tunnel
try:
    public_url = ngrok.connect(8501).public_url
    print("Streamlit app is live at:", public_url)
except Exception as e:
    print(f"Failed to start ngrok tunnel: {e}")




# Your Streamlit app code



# Set the custom ngrok configuration
pyngrok_config = conf.PyngrokConfig(ngrok_path=NGROK_BIN)
conf.set_default(pyngrok_config)



# Start ngrok to create a public URL for the Streamlit app
public_url = ngrok.connect(8501)
print(f"Streamlit app will be accessible at: {public_url}")

# Run the Streamlit app
os.system('streamlit run app.py')

# Print the ngrok public URL
print(f"Streamlit app running at: {public_url}")
