import urllib3
import json
import base64

from typing import Dict

def objectDetect(imagefile):
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    accessKey = "API키"
    imageFilePath = imagefile
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
    predImage_list = []
    predImage_list=list()

    if response.status == 200:
        try :
            etricall = result['return_object']['data']

            for i in etricall:
                predImage_list.append(i.get('class'))
            predImage_list=list(set(predImage_list))
            predImage_list.sort(key = len)
            return predImage_list

        except:
            return predImage_list
    else:
        return predImage_list