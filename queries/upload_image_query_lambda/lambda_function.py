import json
import objectDetection as od
from botocore.exceptions import ClientError
import boto3
import base64

"""
Base64 encoded String for image is send in POST request body.
in format {"based64string":"the string"}
"""

def lambda_handler(event, context):
    theRequest =event['http-method']
    
    if (theRequest == 'POST'):
        print("POST request")
        try:
            # Call object detection function
            b64string = event['body-json']['based64string']
            image_file = base64.b64decode(b64string)
            result = od.objectDetect(image_file)
            # print(output)
            
            labels = []
            
            for o in result:
                labels.append(o[0])
            #labels = ["laptop","keyboard"]
                
            # Remove duplicate at labels
            labels = list(set(labels))
                
            client = boto3.resource("dynamodb")
            table = client.Table("detectedImage")
            
            items = table.scan()['Items']
            scanned_images = []
        
            for i in items:
                tags = i['tag']
                
                # Check if tags consist of labels 
                flag = True
                for l in labels:
                    if l not in tags:
                        flag = False
                        
                if flag == True:
                    scanned_images.append(i['url'])
                    print(scanned_images)
                
            retrun_items = {"links" : scanned_images}
        
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
