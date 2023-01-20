import boto3
from datetime import datetime

# Connect to S3
s3 = boto3.client("s3")

# Set the name of the S3 bucket
bucket_name = "TESTE_s3"

# Get a list of all objects in the bucket
objects = s3.list_objects(Bucket=bucket_name)["Contents"]

# Initialize variables to keep track of the most recent file
most_recent_file = None
most_recent_time = None

# Iterate through the list of objects
for obj in objects:
    # Get the current object's timestamp
    obj_time = obj["LastModified"]
    # Compare the current object's timestamp with the most recent timestamp
    if most_recent_time is None or obj_time > most_recent_time:
        # Update the most recent file and timestamp
        most_recent_file = obj["Key"]
        most_recent_time = obj_time

# Print the name of the most recent file
print("The most recent file is: " + most_recent_file)
