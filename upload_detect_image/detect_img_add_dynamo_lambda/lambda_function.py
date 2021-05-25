import boto3
import objectDetection as od
import uuid
import base64
from urllib.parse import unquote_plus
import json


def lambda_handler(event, context):
    
    # declare s3 object
    s3 = boto3.client('s3')
     
    #If object added to s3 "fit5225-uploaded-image" budget
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        print("File {0} uploaded to {1} bucket".format(key, bucket))
        
        # retrieve the object & its url
        objectFile = s3.get_object(Bucket=bucket, Key=key)
        url = f'https://{bucket}.s3.amazonaws.com/{key}'
        
        # call object detection function
        image_file = objectFile['Body'].read()
        output = od.objectDetect(image_file)
        print(output)



        # PREREQUISITE = I NEED THE STYLE TO WRITE TO DYNAMO
        # Write Output To Dynamo DB 
        TABLE_NAME = 'detectedImage' 
        # declare dynamodb object
        dynamodb = boto3.client('dynamodb')
        
        # if there is object detected
        if len(output) > 0:
            tmp = []
            for detectedObject in output:
                # information for put_item function:
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item
                # item1 = {"M": {
                #       "label": {"S": str(detectedObject[0])},
                #       "accuracy": {"N": str(detectedObject[1])},
                #       "rectangle": {"M": {"height": {"N": str(detectedObject[5])}, "left": {"N": str(detectedObject[2])}, "top": {"N": str(detectedObject[3])}, "width": {"N": str(detectedObject[4])}}}
                #     }}
                # tmp.append(item1)
                item1 = {"S": str(detectedObject[0])}
                tmp.append(item1)
            print(tmp)
            item2 = {
              "url": {"S": url},
              "tag":{"L" : tmp}
            }    
                    
            dynamodb.put_item(TableName=TABLE_NAME, Item=item2)
            
            return {
            'statusCode': 200,
            'body': json.dumps('Images detection data successfully inserted into database...')
            }  
        else: 
            return {
            'statusCode': 200,
            'body': json.dumps('No object detected...')
            }  
        

    
    
    
    # Below is read manually
    # original = s3.get_object(Bucket='fit5225-uploaded-image',Key='000000007454.jpg')
    # thefile = original['Body'].read()
    # output = od.objectDetect(thefile)
    # print(output)
    
    
    
    #TODO: CHECK IF WE NEED UUID, I DONT THINKSO, THE S3 URL IS UNIQUE. ERROR CODE BELOW
    #generate uuid for image
    # print(type(thefile))
    # aaa = base64.b64encode(thefile)
    # print(type(aaa))
    # id =   uuid.UUID(base64.b64encode(thefile))
    # print(str(id))


    