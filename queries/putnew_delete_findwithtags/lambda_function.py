import findimagesbytags as fit
import deleteimages as di
import putnewtags as pnt
import objectDetection as od

"""
url should be named as "url"
tag should be named as "tags"
#set($allParams = $input.params())
{
"body-json" : $input.json('$'),
"http-method" : "$context.httpMethod"}
"""


def lambda_handler(event, context):
    theRequest =event['http-method']
    
    if (theRequest == 'DELETE'):
        print("DELETE request")
        returnItem = di.delete_handler(event, context)
        
    elif (theRequest == 'PUT'):
        print("PUT request")
        returnItem = pnt.put_handler(event, context)
        
    elif (theRequest == 'POST'):
        print("POST request")
        returnItem = fit.get_handler(event, context)
        
        
    # elif (theRequest == 'POST'): #temporary changed
    #     print("this is post")
    #     returnItem = testpost.get_handler(event, context)
        
    #     # Get image (how to parse image from front end as image to backend)
    #     # call object detection function
    #     # image_file = None  # get the image and put it here
    #     # output = od.objectDetect(image_file)
    #     # print(output)
        
    return returnItem
        
    
    # if url of data does not exist, show error to users.
    """
    1. delete from s3 as well - done
    2. get all tags, put it in list, update the list - done
    3. make it to AND logic, instead or OR - done
    4. Get image (how to parse image from front end as image to backend): wait for front end first
    5. API gateway for REST METHOD
    6. test it on postman (w11 tut recording, last 30 mins for postman)
    """