var request = require("request")

function composeHttpUrl(startCity, eindCity)
{
   var base = 
      "https://maps.googleapis.com/maps/api/directions/json?origin="+startCity+"&destination="+eindCity"+"&avoid=highways&mode=bicycling"
   return url;
};


