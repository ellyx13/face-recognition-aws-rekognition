# This file contains the configuration for the AWS services used in the project. 
# You can change the values here to match your own configuration.

REKOGNITION_COLLECTION_NAME = "face_recognition"
# If you encounter a BucketAlreadyExists error, make sure your S3 bucket name is unique.
S3_BUCKET_NAME = "face-recognition-bucket"

DYNAMODB_TABLE_NAME = "face_metadata"

IAM_ROLE_NAME = "face_recognition_role"

LAMBDA_NAME = "face_recognition_lambda"