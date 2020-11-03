import urllib3
import json
import base64

from typing import Dict

def objectDetect():
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    accessKey = "api키"
    imageFilePath = "image\\myPhoto.jpg"
    type = "jpg"

    file = open(imageFilePath, "rb")
    imageContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "type": type,
            "file": imageContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    result = json.loads(response.data.decode('utf-8'))

    etricall = result['return_object']['data']

    predImage_list = []
    predImage_list=list()


    for i in etricall:
        predImage_list.append(i.get('class'))

    predImage_list=list(set(predImage_list))

    return predImage_list