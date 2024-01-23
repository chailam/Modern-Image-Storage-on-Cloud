import findimagesbytags as fit
import deleteimages as di
import putnewtags as pnt

"""
Author: Chai Lam Loi and Dinuk Hashinka Ganearachchi
Aim: This is the lamda function to check the request method.
If the request method is DELETE, it will use the deleteimage.py
If the request method is PUT, it will use the putnewtags.py
If the request method is POST, it will use the findimagesbytags.py

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
        
