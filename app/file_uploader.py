from minio import Minio
from minio.error import S3Error
from pathlib import Path
from datetime import timedelta
import os
import pandas
import csv



def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "127.0.0.1:9000",
        access_key="admin",
        secret_key="password",
        secure=False,
    )

    upload_files(client)
    list_object = client.list_objects("src-data-csv")
    # list_img_object = client.list_objects("src-data-image")
    gen_output_csv(list_object, client)


    found = client.bucket_exists("processed-data")
    if not found:
        client.make_bucket("processed-data")
    else:
        print("Bucket 'processed-data' already exists")

    output_data = Path.cwd().joinpath("output.csv")
    client.fput_object(
        "processed-data", Path(output_data).name, output_data,
    )


def upload_files(client):

    # Make 'src-data-image' bucket if not exist.
    found = client.bucket_exists("src-data-image")
    if not found:
        client.make_bucket("src-data-image")
    else:
        print("Bucket 'src-data-image' already exists")

    # Make 'src-data-csv' bucket if not exist.
    found = client.bucket_exists("src-data-csv")
    if not found:
        client.make_bucket("src-data-csv")
    else:
        print("Bucket 'src-data-csv' already exists")

    # Getting all source data paths
    path = Path.cwd().parent.joinpath("02-src-data")
    list_of_image = []
    list_of_csv = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if "csv" in file:
                list_of_csv.append(os.path.join(root, file))
            else:
                list_of_image.append(os.path.join(root, file))

    # Upload all files as object name
    # 'basename' to bucket 'src-data'.
    for path in list_of_image:
        client.fput_object(
            "src-data-image", Path(path).name, path, content_type="image/png",
        )

    for path in list_of_csv:
        client.fput_object(
            "src-data-csv", Path(path).name, path,
        )


def gen_output_csv(list_object, client):

    with open('output.csv', mode='w') as output:
        output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        output_writer.writerow(["user_id", " first_name", " last_name", " birthts", " img_path"])
        for obj in list_object:

            df = pandas.read_csv(
                f"s3://src-data-csv/{obj.object_name}",
                storage_options={
                    "key": "admin",
                    "secret": "password",
                    "client_kwargs": {"endpoint_url": "http://127.0.0.1:9000"}
                }
            )
            # print(list(df.columns))
            # print([df[item][0] for item in list(df.columns)])
            url = client.get_presigned_url(
                "GET",
                "src-data-image",
                f"{obj.object_name}".split(".")[0] + ".png",
            )

            count += 1
            output_writer.writerow([count, df["first_name"][0], df[" last_name"][0], df[" birthts"][0], url])


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
