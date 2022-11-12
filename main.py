import requests
import pprint


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class InrixHack:
    domain = 'https://api.iq.inrix.com/'
    auth_tkn = None

    def gen_token(self):
        payload = {
            'appId': 'xalx86idf9',
            'hashToken': 'eGFseDg2aWRmOXxhbDloUzBWUm1NMUdXWUExYXd6RlA4Q21jVG8wbEpaeTROcTlpNjhV'
        }

        r = requests.get(self.domain + 'auth/v1/appToken', params=payload)
        resp = r.json()

        self.auth_tkn = resp['result']['token']

    def get_seg_speed(self):
        payload = {
            'box': '37.757386|-122.490667,37.746138|-122.395481',
            'RoadSegmentType': 'TMC'
        }

        r = requests.get(
            self.domain + 'v1/segments/speed',
            auth=BearerAuth(self.auth_tkn),
            params=payload
        )
        resp = r.json()
        pprint.pprint(resp)

    def get_seg_speed(self):
        payload = {
            'box': '37.757386|-122.490667,37.746138|-122.395481',
            'RoadSegmentType': 'TMC'
        }

        r = requests.get(
            self.domain + 'v1/segments/speed',
            auth=BearerAuth(self.auth_tkn),
            params=payload
        )
        resp = r.json()
        pprint.pprint(resp)


if __name__ == "__main__":
    ih = InrixHack()
    ih.gen_token()
    ih.get_seg_speed()
    # print(ih.auth_tkn)
