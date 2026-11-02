import json
import logging

# Initialize the logger (Best practice: configure outside the handler to reuse across invocations)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Standard AWS Lambda handler function.
    
    :param event: A dict containing data passed by the invoking service (e.g., API Gateway, S3, SQS).
    :param context: An AWS Lambda Context object providing runtime information.
    :return: A dict containing the response payload (crucial for synchronous integrations like API Gateway).
    """
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        # 1. Parse and extract data from the incoming 'event'
        # Example: body = json.loads(event.get('body', '{}'))
        
        # 2. Insert your core business logic here
        message = "Hello from AWS Lambda using Python!"
        
        # 3. Construct and return a structured response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': message,
                'success': True
            })
        }
        
    except Exception as e:
        logger.error("An error occurred: %s", str(e), exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal Server Error',
                'details': str(e)
            })
        }
