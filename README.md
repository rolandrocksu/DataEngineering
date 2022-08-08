
## How to run
* `sh run.sh` - run services
* `sh run.sh --clear` - stop and remove containers


## Input data description

In a provided archive, there's a `02-src-data` folder which contains some CSV files with information about users, and image files for some of the users. If the base CSV filename matches to the image base filename, then the image is a picture of that user. The base name of a CSV file / image is a user's ID.

E.g. 

* `01-src-data/1000.csv` - information about user #1000
* `01-src-data/1000.png` - user #1000's picture

You will have to load the source data to Minio for your service to process.

## Data transformation

1. Reading CSV files
2. Matching images to users
3. Aggregating data into a single CSV file (see format below)
4. Storing the output data to [Minio](https://min.io/) (overwriting the earlier version of the output)

This should happen periodically. so once source data is updated in Minio, the output should eventually be updated. The update of the output has to happen not later then in 1 hour from source update.

## Output data format
Updating `processed_data/output.csv` CSV file and incorporate new data coming from input. Note: we can update data for previously processed user, in this case the record for a user should be overwritten. The output CSV file should not contain duplicate user records. 

Output CSV file format: `user_id, first_name, last_name, birthts, img_path`

## Serving the data
The service implemented web server with following endpoints:

* `GET /data` - get all records from DB in JSON format. Implemented filtering by: is_image_exists = True/False, user min_age and max_age in years.
* `POST /data` - manually trigger reprocessing the source data in  `02-src_data`
* `GET /stats` - calculate and return the average age of users matching the filters (`is_image_exists=True/False`, `min_age`, `max_age`)

It should answer on `localhost:8080` when your service is running.
