import urllib
import urllib.request
import json
from flask import Flask
from flask import request


app = Flask(__name__)



gmap = 'http://maps.googleapis.com/maps/api/'
directions = 'directions/json?'
test_data = {"origin": 'Toronto', "destination": 'Montreal', "avoid": 'highways', "mode": 'bicycling'}

#composes the url
def build_url(sub,obj):
	return gmap+sub+urllib.parse.urlencode(obj)

#makes a simple http get request
def get(url):
	r=urllib.request.urlopen(url)
	return json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

def weighted(wght,frm,to):
	wght = wght if wght < 1 else 1
	return {"lat":frm["lat"]+wght*(to["lat"]-frm["lat"]), "lng":frm["lng"]+wght*(to["lng"]-frm["lng"])}


def get_pnt(leg,dist):
	for s in leg["steps"]:
		cur_dist=s["distance"]["value"]
		if (cur_dist > dist):
			return weighted(dist/cur_dist,s["start_location"],s["end_location"])
		dist = dist - cur_dist


test_url=build_url(directions,test_data)
dat=get(test_url)
leg=dat["routes"][0]["legs"][0]

def get_routes(src,dest):
	return get(build_url(directions, {"origin": src, "destination": dest , "alternatives": "true"}))["routes"]

def get_points_for_src_dest(src,dest,reach):
	return [get_points(route,reach) for route in get_routes(src,dest)]

#1. function
@app.route("/get_routes",methods=['GET'])
def get_routes_wrap():
	src,dest=[request.args.get(i) for i in ["start","end"]]
	return json.dumps(get_routes(src,dest))

#2. function
def get_points(route,reach):
	return get_pnt(route["legs"][0],reach)

#3. function
@app.route("/get_points_for_src_dest",methods=['GET'])
def get_points_for_src_dest_wrap():
	src,dest,reach=[request.args.get(i) for i in ["start","end","reach"]]
	return json.dumps(get_points_for_src_dest(src,dest,float(reach)))


if __name__ == "__main__":
    app.run()