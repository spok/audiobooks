import urllib.request
import json


class Recognize:
    def __init__(self):
        self.key = 'AQVNzLJrizP3pU9S1bFmk4K4HktOVRRSnh5ISmsL'
        self.folder_id = 'b1gvf14g88gtdrsuh1hm'
        self.filename = "recorded.ogg"
        self.params = "&".join([
            "topic=general",
            "folderId=%s" % self.folder_id,
            "lang=ru-RU"
        ])

    def get_recognize(self) -> list:
        with open(self.filename, "rb") as f:
            data = f.read()
        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % self.params,
                                     data=data)
        url.add_header("Authorization", 'Api-Key {}'.format(self.key))

        responsedata = urllib.request.urlopen(url).read().decode('UTF-8')
        decodeddata = json.loads(responsedata)

        if decodeddata.get("error_code") is None:
            return decodeddata.get("result")
