import pandas as ps
from datetime import datetime, date

def filter_data(is_image_exists, min_age, max_age):
    df = ps.read_csv(
        "s3://processed-data/output.csv",
        storage_options={
            "key": "admin",
            "secret": "password",
            "client_kwargs": {"endpoint_url": "http://127.0.0.1:9000"}
        }
    )
    df[" age"] = df.apply(lambda x: get_age_from_ts(x[" birthts"]), axis=1)
    if is_image_exists is not None:
        is_image_exists = is_image_exists.lower() == 'false'
        df = df[(df[" img_path"] == " ") == is_image_exists]
    if min_age:
        df = df[df[" age"] >= int(min_age)]
    if max_age:
        df = df[df[" age"] <= int(max_age)]

    return df


def get_age_from_ts(ts):

    birthdate = datetime.fromtimestamp(ts)
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age