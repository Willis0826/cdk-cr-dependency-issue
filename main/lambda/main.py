import random
import string
from urllib.request import Request, urlopen
import time
import json


def random_id_string(length):
    return "".join(
        random.choice(string.ascii_uppercase) for _ in range(length)
    )


def handler(event, context):
    print(f"event: {json.dumps(event)}")

    # sleep few seconds for EIP to finish the disassociation
    if event["RequestType"] == "Delete":
        time.sleep(50)

    # form a valid response
    physical_id = event.get("PhysicalResourceId") or random_id_string(8)
    response_body = {
        "RequestId": event["RequestId"],
        "StackId": event["StackId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "PhysicalResourceId": physical_id,
        "Status": "SUCCESS",
    }
    response_body = json.dumps(response_body)

    # send request to fulfill the creation, deletion or update
    urlopen(Request(
        method="PUT",
        url=event["ResponseURL"],
        headers={"Content-Type": "application/json"},
        data=response_body.encode("utf-8"),
    ))
