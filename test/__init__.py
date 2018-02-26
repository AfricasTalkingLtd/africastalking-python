
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

USERNAME = os.getenv('USERNAME', 'sandbox')
API_KEY = os.getenv('API_KEY', 'fake')
