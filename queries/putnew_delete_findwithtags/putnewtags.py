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

def put_handler(event, context):
    
    labels = event['body-json']['tags']
    theurl = event['body-json']['url']
    
    #theurl = 'https://fit5225-uploaded-image.s3.amazonaws.com/000000023401.jpg'  #Retrieve from frontend
    #labels= ['chailam','dinuk']   #Retrieve from frontend
    
    client = boto3.resource("dynamodb")
    table = client.Table("detectedImage")
    
    
    try:
        print("Retrieving original tags...")
        item = table.get_item(Key={'url':  theurl})
        tags = item['Item']['tag']
        concatenateList = tags + labels
            
        print("Attempting a tag update...")
        response = table.update_item(
            Key={
                'url': theurl
            },
            UpdateExpression="set tag =:t",
            ExpressionAttributeValues={
                ':t': concatenateList
            },
            ReturnValues = "UPDATED_NEW"
        )
    
        
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
            "body": "Insertion Complete!"
        }
    