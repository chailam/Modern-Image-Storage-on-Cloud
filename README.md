# Cloud-Based Image Detection, Storage and Retrieval System

## Project Summary

This is a cloud-based image detection, storage and retrieval system designed to enable users to upload images to public cloud storage and retrieve them based on auto-generated tags. The project employs serverless architecture, utilizing AWS cloud services such as S3, Lambda, API Gateway, and DynamoDB. The primary features include automated object-detection tagging and querying based on detected objects.

### Project Objectives

1. **Image Upload:** Users can upload images to an S3 bucket, triggering a Lambda function for automatic object detection using Yolo. The detected objects (tags) are stored in DynamoDB along with the image's S3 URL.

2. **Queries:** Users can perform various queries, including finding images based on specific tags, finding images with similar tags to a provided image, adding extra tags to an image, and deleting an image.

3. **Authentication and Authorization:** The system ensures security through AWS Cognito, managing user authentication and authorization. Users must sign in to access services, and the application records user information.

4. **User Interface (UI):** While optional, a simple web-based UI is suggested to enhance user experience. The UI can include pages for login, sign-up, image upload, query submission, and viewing query results.

## System Workflow

1. **Authentication:** Users must sign in to access the system. New users register through a sign-up page, and AWS Cognito handles email verification and password changes.

2. **Image Upload:** Users can upload images either API Gateway endpoints. The Lambda function is triggered upon image upload, performing object detection and storing detection object as tags in DynamoDB.

3. **Queries:** Users can query images based on specific tags or the tags of a provided image. The system responds with URLs of matching images.

4. **Additional Features:** Users can add extra tags to an image and delete images from the system.


## Implementation Details

- **Authentication:** AWS Cognito user pool is used for authentication, ensuring secure access to endpoints.
- **Image Processing:** Yolo is employed for object detection in images, with Lambda functions handling the processing.
- **Data Storage:** DynamoDB stores detected objects along with image URLs for efficient querying.
![alt text](./doc/FIT5225%20A2%20Architecture%20Design.jpeg "System Architecture")



## Installation

Currently this system is not hosted on AWS due to billing and pricing. To set up the service:

- Set up the DynamoDb, S3 storage, Amazon Incognito and the permission required for those services using AWS IAM.
- Use the code provided to setup the AWS Lambda function and API Gateway.
- Connecting all services together.

