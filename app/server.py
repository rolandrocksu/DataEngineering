from fastapi import FastAPI
from  app import file_uploader
from  app.utils import filter_data
from minio.error import S3Error


app = FastAPI()

@app.get("/")
def root():
    # try:
    #     file_uploader.main()
    # except S3Error as exc:
    #     print("error occurred.", exc)

    return {
        "data link": "/data",
        "stats link": "/stats"
            }


@app.get("/data")
async def root_data(is_image_exists=None, min_age=None, max_age=None):
    df = filter_data(is_image_exists, min_age, max_age)

    return df.to_dict()


@app.post("/data")
async def root_data_post():
    try:
        file_uploader.main()
    except S3Error as exc:
        print("error occurred.", exc)
    return {"message": "Data updated"}

@app.get("/stats")
async def root_stats(is_image_exists=None, min_age=None, max_age=None):
    df = filter_data(is_image_exists, min_age, max_age)
    age = df[" age"].mean()
    return {"Average age": f"{age:.2f}"}


