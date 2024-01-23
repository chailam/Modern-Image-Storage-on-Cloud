/*
This is a simple JS file to upload the JPG image to S3.

Currently, it is only for JPG image.

Base64 encoded String for image is send in POST request body.
in format {"based64string":"the string"}

*/

const AWS = require('aws-sdk');
const s3 = new AWS.S3();

exports.handler = (event, context, callback) => {
  let request = JSON.parse(event.body);
  let bucket = "fit5225-uploaded-image";
    
    // get the image
    let encodeImage = request.based64string;
    let decodeBufferImage = Buffer.from(encodeImage, 'base64');
    
  
    // Construct a filepath
    var filePath = context.awsRequestId + ".jpg";  // "mime/jpg"
    
    // Construct the parameter
    var params = {
      "Body": decodeBufferImage,
      "Bucket": bucket,
      "Key": filePath,
      "ACL" : "public-read",
      "ContentType " :"mime/jpg"   //fileMime 
      };
      
    // Upload image
    s3.upload(params, function (err, data) {
      // if error
    if (err) {
      console.log(err);
      callback(err, null);
    } else {
      // if successful
      console.log(data);
      let response = {
        "statusCode": 200,
        "headers":{"Access-Control-Allow-Origin":"*"},
        "body": JSON.stringify(data),
        "isBase64Encoded": false
      };
      callback(null, response);
    }
    });
};