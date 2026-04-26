# WSGI entry point for Vercel
from app import app as application

def handler(event, context):
    return application(event, context)