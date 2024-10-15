from __future__ import print_function

import boto3

print('Loading function')

# Replace DYNAMODB_TABLE_NAME and REKOGNITION_COLLECTION_NAME with your DynamoDB table name and Rekognition collection name in config.py
DYNAMODB_TABLE_NAME = "face_metadata"
REKOGNITION_COLLECTION_NAME = "face_recognition" 

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


# --------------- Helper Functions ------------------

def index_faces(bucket, key):
    image_object = {}
    image_object['S3Object'] = {
        "Bucket": bucket,
        "Name": key
    }
    response = rekognition.index_faces(Image=image_object, CollectionId=REKOGNITION_COLLECTION_NAME)
    return response
    
def update_index(face_id, fullname):
    item_object = {}
    item_object['RekognitionId'] = {'S': face_id}
    item_object['FullName'] = {'S': fullname}
    dynamodb.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item_object)
    
# --------------- Main handler ------------------

def lambda_handler(event, context):

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("Records: ",event['Records'])
    key = event['Records'][0]['s3']['object']['key']
    print("Key: ",key)

    try:

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
    
        response = index_faces(bucket, key)
        
        # Commit faceId and full name object metadata to DynamoDB
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            face_id = response['FaceRecords'][0]['Face']['FaceId']

            ret = s3.head_object(Bucket=bucket,Key=key)
            fullname = ret['Metadata']['fullname']

            update_index(face_id, fullname)

        # Print response to console
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e