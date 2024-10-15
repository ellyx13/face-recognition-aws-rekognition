import boto3
import io
from PIL import Image
from config import S3_BUCKET_NAME, REKOGNITION_COLLECTION_NAME, DYNAMODB_TABLE_NAME

s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
def update_image(fullname, image_path):
    file = open(image_path,'rb')
    s3_object = s3.Object(S3_BUCKET_NAME,'index/'+ image_path)
    result = s3_object.put(Body=file, Metadata={'FullName':fullname})
    print("Update image result: ", result)
    return result


def check_face(image_path):
    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()

    response = rekognition.search_faces_by_image(CollectionId=REKOGNITION_COLLECTION_NAME, Image={'Bytes':image_binary})

    for match in response['FaceMatches']:
        print(match['Face']['FaceId'],match['Face']['Confidence'])
        face = dynamodb.get_item(TableName=DYNAMODB_TABLE_NAME, Key={'RekognitionId': {'S': match['Face']['FaceId']}})
        print(face)
        if 'Item' in face:
            return face['Item']['FullName']['S'], int(match['Face']['Confidence'])
              
    return None, None