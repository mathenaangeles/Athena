import os
AUTHORITY= os.getenv("AUTHORITY")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

ENDPOINT = 'https://graph.microsoft.com/v1.0/me'  
SCOPE = ["User.Read"]

SESSION_TYPE = "filesystem"