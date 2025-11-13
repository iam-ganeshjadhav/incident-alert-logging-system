import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('IncidentLogs')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        build_name = body.get('build_name', 'unknown')
        status = body.get('status', 'FAILED')
        error_message = body.get('error_message', 'N/A')

        table.put_item(
            Item={
                'incident_id': str(uuid.uuid4()),
                'build_name': build_name,
                'status': status,
                'error_message': error_message,
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Incident logged successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
