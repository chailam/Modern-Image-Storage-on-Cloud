import boto3
from botocore.exceptions import ClientError
import json


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, set):  #<---resolving sets as lists
            return list(o)
        return super(DecimalEncoder, self).default(o)

def delete_handler(event, context):
    
    theurl = event['body-json']['url']
    #__url_to_delete = 'https://fit5225-uploaded-image.s3.amazonaws.com/000000007454.jpg'   #Retrieve from frontend 48
    #__url = 'url'

    client = boto3.resource("dynamodb")
    table = client.Table("detectedImage")
    s3 = boto3.resource('s3')
    
    print("Attempting a delete...")

    try:
    
        response = table.delete_item(
            Key={
                'url': theurl
            }
        )
        
        s3 = boto3.resource("s3")
        obj = s3.Object("fit5225-uploaded-image", theurl[48:])  #Retrieve from frontend
        obj.delete()

    # delete non-existent item does not fail, because:
    # Unless you specify conditions, the DeleteItem is an idempotent operation; 
    # running it multiple times on the same item or attribute does not result in an error response.
    # https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html
    
    except ClientError as e:
        print (e)
        # Return Error JSON or http error code
        retrun_items = {"error": e}
        return retrun_items
    
    else:
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": "Delete Complete!"
        }
    