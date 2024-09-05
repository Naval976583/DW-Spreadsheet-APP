import os

class Config:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'credentials/axial-coyote-413518-58b048e72326.json')

# You can add more configurations here like DevConfig, ProdConfig, etc.
