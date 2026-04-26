# Vercel Python Handler for Flask
from werkzeug.wrappers import Request, Response
from app import app as application

def handler(event, context):
    request = Request(event)
    response = Response.from_app(application, request.environ)
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }