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
        

def get_handler(event, context):
    labels = event['body-json']['tags']
    print(labels)
    #labels = ["laptop","keyboard"] # Retrieve from frontend
    
    client = boto3.resource("dynamodb")
    table = client.Table("detectedImage")
    
    items = table.scan()['Items']
    
    scanned_images = []
    try:
        # Remove duplicate at labels
        labels = list(set(labels))
    
        for i in items:
            tags = i['tag']
            print(tags)
            
            # Check if tags consist of labels 
            flag = True
            for l in labels:
                if l not in tags:
                    flag = False
                    
            if flag == True:
                scanned_images.append(i['url'])
                print(scanned_images)
            
        retrun_items = {"links" : scanned_images}
        
        
        #for i in items:
         #  tags = i['tag']
         #  for x in tags:
          #     if x in __labels:  # make it to AND logic
          ##       scanned_images.append(i[__url])
           #      break

        #retrun_items = {"links": scanned_images}
        
        # Get url , put into JSON list, return back
        
    except ClientError as e:
        print (e)
        # Return Error JSON or http error code
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(e)
        }

    else:
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(retrun_items)
        }
