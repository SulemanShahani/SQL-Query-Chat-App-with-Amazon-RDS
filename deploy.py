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
