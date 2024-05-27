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
if not ngrok_auth_token:
    raise ValueError("NGROK_AUTH_TOKEN environment variable is not set.")

try:
    print("Setting ngrok authentication token...")
    command = [NGROK_BIN, "authtoken", ngrok_auth_token, "--log=stdout"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(f"ngrok output: {result.stdout}")
    print("ngrok authentication token set successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to set ngrok authentication token: {e}")
    print(f"Command output: {e.output}")
    print(f"Command stderr: {e.stderr}")
    raise

# Start ngrok tunnel
try:
    public_url = ngrok.connect(8501).public_url
    print("Streamlit app is live at:", public_url)
except Exception as e:
    print(f"Failed to start ngrok tunnel: {e}")
    raise

# Your Streamlit app code


# Your Streamlit app code



# Set the custom ngrok configuration
pyngrok_config = conf.PyngrokConfig(ngrok_path=NGROK_BIN)
conf.set_default(pyngrok_config)

# Set ngrok authentication token
ngrok_auth_token = os.getenv("NGROK_AUTH_TOKEN")
if not ngrok_auth_token:
    raise ValueError("NGROK_AUTH_TOKEN environment variable is not set.")

try:
    print("Setting ngrok authentication token...")
    command = [NGROK_BIN, "config", "add-authtoken", ngrok_auth_token, "--log=stdout"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(f"ngrok output: {result.stdout}")
    print("ngrok authentication token set successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to set ngrok authentication token: {e}")
    print(f"Command output: {e.output}")
    print(f"Command stderr: {e.stderr}")
    raise

# Start ngrok tunnel
try:
    public_url = ngrok.connect(8501).public_url
    print("Streamlit app is live at:", public_url)
except Exception as e:
    print(f"Failed to start ngrok tunnel: {e}")
    raise


# Set the custom ngrok configuration
pyngrok_config = conf.PyngrokConfig(ngrok_path=NGROK_BIN)
conf.set_default(pyngrok_config)

# Set ngrok authentication token
ngrok_auth_token = os.getenv("NGROK_AUTH_TOKEN")
if not ngrok_auth_token:
    raise ValueError("NGROK_AUTH_TOKEN environment variable is not set.")

try:
    print("Setting ngrok authentication token...")
    ngrok.set_auth_token(ngrok_auth_token)
    print("ngrok authentication token set successfully.")
except Exception as e:
    print(f"Failed to set ngrok authentication token: {e}")
    raise

# Start ngrok tunnel
try:
    public_url = ngrok.connect(8501).public_url
    print("Streamlit app is live at:", public_url)
except Exception as e:
    print(f"Failed to start ngrok tunnel: {e}")
    raise


# Start ngrok to create a public URL for the Streamlit app
public_url = ngrok.connect(8501)
print(f"Streamlit app will be accessible at: {public_url}")

# Run the Streamlit app
os.system('streamlit run app.py')

# Print the ngrok public URL
print(f"Streamlit app running at: {public_url}")
