import json
import math
from math import cos, asin, sqrt, pi
import requests
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, make_response


def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class InrixHack:
    domain = 'https://api.iq.inrix.com/'

    def __init__(self):
        self.auth_tkn = None
        self.drivable_pts = []
        self.loc_flags = None
        self.charger_loc = []

    def get_vendor_data(self):
        f = open('data.json')
        data = json.load(f)
        return data['data']

    def gen_token(self):
        payload = {
            'appId': 'xalx86idf9',
            'hashToken': 'eGFseDg2aWRmOXxhbDloUzBWUm1NMUdXWUExYXd6RlA4Q21jVG8wbEpaeTROcTlpNjhV'
        }

        r = requests.get(self.domain + 'auth/v1/appToken', params=payload)
        resp = r.json()

        self.auth_tkn = resp['result']['token']

    def get_drivetime_poly(self, coords, dur):
        payload = {
            'center': str(coords[0]) + '|' + str(coords[1]),
            'rangeType': 'A',
            'duration': dur,
            'dateTime': '2022-11-09T16:00:00Z'
        }

        r = requests.get(
            self.domain + 'drivetimePolygons',
            auth=BearerAuth(self.auth_tkn),
            params=payload,
            timeout=3
        )

        try:
            root = ET.fromstring(r.text)
            for drive_time in root[0][0]:
                pos_list = drive_time[0][0][0].text.split()
                pos_list = list(map(float, pos_list))

                pos_list2 = []
                for i in range(0, len(pos_list), 2):
                    pos_list2.append([pos_list[i], pos_list[i+1]])

                self.drivable_pts.append(pos_list2)
        except:
            # print(r.text)
            return False
        return True

    def find_suitable_locations(self):
        for idx1, location1_list in enumerate(self.drivable_pts):
            if self.loc_flags[idx1] != 1:
                for idx2, location2_list in enumerate(self.drivable_pts):
                    if idx1 == idx2 or self.loc_flags[idx2] == 1:
                        continue
                    else:
                        for loc1 in location1_list:
                            flag1 = True
                            for loc2 in location2_list:
                                dist = distance(
                                    loc1[0], loc1[1],
                                    loc2[0], loc2[1]
                                )
                                if dist <= 0.5:
                                    self.charger_loc.append([idx1, idx2, loc1])
                                    self.loc_flags[idx1] = self.loc_flags[idx2] = 1
                                    flag1 = False
                                    break

                            if not flag1:
                                break


app = Flask(__name__)


@app.route("/app/get/locations", methods=["POST", "OPTIONS"])
def get_locations():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        loc = []
        time = 0

        ih = InrixHack()
        ih.gen_token()

        data = ih.get_vendor_data()
        for item in data:
            if 5 <= item['time'] <= 60:
                loc.append(item['dst'])
                time += item['time']

        ih.loc_flags = [0] * len(loc)
        avg_time = int(math.floor(time/len(loc)))

        for idx, item in enumerate(loc):
            status = ih.get_drivetime_poly(item, avg_time)
            if not status:
                del loc[idx]
                del ih.loc_flags[idx]

        ih.find_suitable_locations()

        charger_loc = []
        for item in ih.charger_loc:
            charger_loc.append(item[2])

        del ih

        return _corsify_actual_response(jsonify({
            "hubs": loc,
            "locations": charger_loc
        }))
