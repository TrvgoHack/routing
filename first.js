var request = require('request')
var querystring=require('querystring')

var gmap = 'http://maps.googleapis.com/maps/api/'
var directions = 'directions/json?'
var test_data = {origin: 'Toronto', destination: 'Montreal', avoid: 'highways', mode: 'bicycling'}

// sub is the subpath, object contains all parameters
function get (sub, obj) {
	 ret=""
	callback = function(response) {

	  ret=response.body
	}
	var req=request(gmap + sub + querystring.stringify(obj)).end()
	return ret
}
get(directions,test_data)