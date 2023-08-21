import argparse
import shutil
import zipfile
from datetime import datetime, date
import pandas as pd
import boto3
from pathlib import Path


def pull_logs(user: str, region: str, date: datetime):
    """
    Pulls cloudtrail logs for a specific user and region.

    Parameters:
        user (str): The user to pull logs for.
        region (str): The region to pull logs from.
        date (datetime): The date to pull logs for.

    Returns:
        generator: A generator that yields events from the logs.
    """
    print(f"Pulling {user} for {region}")
    client = boto3.client("cloudtrail", region_name=region)
    next_token = ""
    while True:
        kwargs = {
            "LookupAttributes": [{"AttributeKey": "Username", "AttributeValue": user}],
            "StartTime": date,
            "EndTime": datetime.combine(date, datetime.max.time()),
        }
        if next_token:
            kwargs["NextToken"] = next_token
        response = client.lookup_events(**kwargs)
        for event in response["Events"]:
            yield event
        next_token = response.get("NextToken", "")
        if not next_token:
            break


def read_file(path):
    """
    Reads a file and returns its contents as a list of strings.

    Parameters:
        path (Path): The path to the file to read.

    Returns:
        list: The contents of the file as a list of strings.
    """
    with open(path, "r") as file:
        return file.readline().strip().split(",")


def zip_folder(folder_path, output_path):
    """
    Zips the contents of a folder and saves it to a specified output path.

    Parameters:
        folder_path (str): The path to the folder to zip.
        output_path (str): The path to save the zipped file to.
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_obj:
        for file_path in Path(folder_path).rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(folder_path)
                zip_obj.write(file_path, relative_path)


parser = argparse.ArgumentParser()
parser.add_argument('--date', help='Enter the date in YYYY-MM-DD format')
args = parser.parse_args()

if args.date is None:
    today = date.today().strftime("%Y-%m-%d")
else:
    today = args.date

current_folder = Path.cwd() / f"{today} - Accountability"

if current_folder.exists():
    shutil.rmtree(current_folder)

current_folder.mkdir(parents=True)

names = read_file(Path.cwd() / "names")
regions = read_file(Path.cwd() / "regions")

for name in names:
    (current_folder / name).mkdir()
    for region in regions:
        df = pd.DataFrame(pull_logs(name, region, datetime.strptime(today, '%Y-%m-%d')))
        with open(current_folder / name / f"{today}_{name}_{region}.csv", "w+") as file:
            file.write(df.to_csv(index=False))

zip_folder(current_folder, Path.cwd() / f"{today} - Accountability.zip")

shutil.rmtree(current_folder)
