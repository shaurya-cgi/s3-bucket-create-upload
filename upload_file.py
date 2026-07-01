import os
import sys

import boto3
from botocore.exceptions import ClientError


def create_bucket(s3_client, bucket_name):
	try:
		s3_client.head_bucket(Bucket=bucket_name)
		print(f"Bucket '{bucket_name}' already exists.")
		return
	except ClientError:
		pass

	region = s3_client.meta.region_name or "us-east-1"

	if region == "us-east-1":
		s3_client.create_bucket(Bucket=bucket_name)
	else:
		s3_client.create_bucket(
			Bucket=bucket_name,
			CreateBucketConfiguration={"LocationConstraint": region},
		)

	print(f"Bucket '{bucket_name}' created in region '{region}'.")


def main():
	if len(sys.argv) != 3:
		print("Usage: python upload_file.py <bucket_name> <file_name>")
		sys.exit(1)

	bucket_name = sys.argv[1]
	file_name = sys.argv[2]

	if not os.path.isfile(file_name):
		raise FileNotFoundError(f"File not found: {file_name}")

	s3 = boto3.client("s3")
	create_bucket(s3, bucket_name)

	object_key = os.path.basename(file_name)
	s3.upload_file(file_name, bucket_name, object_key)
	print(f"Uploaded '{file_name}' to bucket '{bucket_name}' as '{object_key}'.")


if __name__ == "__main__":
	main()