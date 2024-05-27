import os
import time
import urllib.request
import zipfile
from pyngrok import ngrok, conf
from dotenv import load_dotenv
import subprocess

load_dotenv()

# Set the ngrok authentication token
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
if NGROK_AUTH_TOKEN is None:
    raise ValueError("NGROK_AUTH_TOKEN not found in environment variables. Please set it.")

# Set a custom ngrok path
NGROK_BIN = "/usr/local/bin/ngrok"  # Update with your preferred ngrok binary path
NGROK_URL = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
NGROK_ZIP = "/tmp/ngrok.zip"

# Download ngrok if not already present or check if an update is required
if not os.path.exists(NGROK_BIN):
    try:
        print("Downloading ngrok...")
        urllib.request.urlretrieve(NGROK_URL, NGROK_ZIP)

        # Extract ngrok to a temporary directory
        with zipfile.ZipFile(NGROK_ZIP, "r") as zip_ref:
            zip_ref.extractall("/tmp/ngrok")

        # Move ngrok binary to the preferred location
        os.rename("/tmp/ngrok/ngrok", NGROK_BIN)
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

try:
    # Set the ngrok authentication token
    result = subprocess.run([NGROK_BIN, "authtoken", NGROK_AUTH_TOKEN], capture_output=True, text=True, check=True)
    print(result.stdout)
    print("Ngrok authentication token set successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error setting ngrok authentication token: {e}")
    print(e.stdout)
    print(e.stderr)
    raise

# Wait for ngrok to be ready
def connect_to_ngrok():
    ngrok_tunnel = None
    while ngrok_tunnel is None:
        try:
            ngrok_tunnel = ngrok.connect(8501)
        except Exception as e:
            print(f"Failed to connect to ngrok: {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying

# Retry connecting to ngrok
for attempt in range(5):  # Retry 5 times
    try:
        connect_to_ngrok()
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed to connect to ngrok: {e}")
        if attempt == 4:
            print("Max retry attempts reached. Exiting...")
            exit(1)
        time.sleep(5)  # Wait 5 seconds before retrying


# Once connected, get the public URL
public_url = ngrok_tunnel.public_url
print(f"Streamlit app is live at: {public_url}")

# Run the Streamlit app
os.system('streamlit run app.py')

# Print the ngrok public URL
print(f"Streamlit app running at: {public_url}")
