from src.app import app

def handler(event, context):
    from serverless_wsgi import handle_request
    return handle_request(app, event, context)

    
# The handler function is the entry point for AWS Lambda to invoke the Flask application.
# It uses the serverless_wsgi library to convert the AWS Lambda event into a WSGI request
# and then calls the Flask application to handle the request.
# This allows the Flask application to run in a serverless environment, such as AWS Lambda.
# The handler function is defined to take two parameters: event and context.
# The event parameter contains the data from the AWS Lambda event, and the context parameter
# contains runtime information about the Lambda function.
# The function uses the handle_request function from the serverless_wsgi library to convert
# the AWS Lambda event into a WSGI request and then calls the Flask application to handle
# the request. The result is returned as the response to the AWS Lambda event.