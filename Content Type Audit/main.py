import os
import requests
import csv
from datetime import datetime

SPACE_ID = os.environ["CONTENTFUL_SPACE_ID"]
DOMAIN = os.environ["CONTENTFUL_DOMAIN"]
ENV_ID = os.environ["CONTENTFUL_ENVIRONMENT_ID"]
ACCESS_TOKEN = os.environ["CONTENTFUL_ACCESS_TOKEN"]

def main():
    fields = ['Space ID', 'Content Type ID', 'Number of Entries']

    filename = "contenttype_audit_" + datetime.now().strftime("%m-%d-%Y-%H:%M:%S") + ".csv"
    # Note: MacOS will display the file in Finder with a slash in the timestamp

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        cts = getContentTypes()

        print("Found " + str(len(cts)) + " content types...")

        for ct in cts:
            entries = getEntries(ct)
            # print(f"{ct}:", len(entries))
            rows = [SPACE_ID, ct, len(entries)]    
            csvwriter.writerow(rows)


def getContentTypes():
    cts = []

    r = requests.get(
        f"https://{DOMAIN}/spaces/{SPACE_ID}/environments/{ENV_ID}/content_types",
        params={
            "access_token": ACCESS_TOKEN,
            "limit": 1000
        },
    ).json()

    for ct in r["items"]:
        cts.append(ct["sys"]["id"])

    cts.sort()
    return cts


def getEntries(content_type):
    entries = []
    skip = 0

    while True:
        r = requests.get(
            f"https://{DOMAIN}/spaces/{SPACE_ID}/environments/{ENV_ID}/entries",
            params={
                "access_token": ACCESS_TOKEN,
                "content_type": content_type,
                "skip": skip,
            },
        ).json()
        entries.extend(r["items"])

        if len(r["items"]) < 100:
            break
        else:
            skip += 100

    return entries


if __name__ == "__main__":
    main()
    
