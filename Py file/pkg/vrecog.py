import urllib3
import json
import base64

def voiceRecognition(myaudioFile):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "API키"
    audioFilePath = myaudioFile
    languageCode = "english"

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
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
    etricall =""
    
    if response.status == 200:
        try :
            etricall = result['return_object']['recognized']
            etricall = etricall.rstrip('\n')
            etricall = etricall.lstrip()
            return etricall

        except:
            return etricall
    else:
        etricall = str(response.status)
        return etricall