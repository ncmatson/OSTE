var map;
var ratio;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 32.84445431845944, lng: -96.78474766922},
    zoom: 15,
    tilt: 0,
    mapTypeId: 'satellite',
    rotateControl: false,
    streetViewControl: false
  });
  updateCoord();
}

$(function mapClickOrMove(){
  $("#map").on('mouseup mouseout', function(){
    updateCoord();
  });
});

$("#edgebutton").on('click', function(){
  var url = $("form[name='edgeit']").attr("action")

  // get center point
  var latlon = map.getCenter();
  console.log('center ', latlon.lat(), latlon.lng())
  var lat = latlon.lat();
  var lon = latlon.lng();

  // get NE corner to calculate px/m ratio
  var bounds = map.getBounds();
  var corner = bounds.getNorthEast();
  console.log('corner ', corner.lat(), corner.lng());
  ratio = haversine(lat, lon, corner.lat(), corner.lng());

  var z = map.getZoom();
  $.post(url, {'lat':lat, 'lon':lon, 'zoom':z}, function(result){
    // update the location for the image showing contours
    $("#edge").attr('src', result.url);
    $("#nn").attr('src',result.url_nn);
    $("#dumy").attr('src',result.url_dum);
    $("#good").attr('src',result.url_good);
    // clear the HTML listing the areas
    $("#areas").html("");

    // write the area for each contour to a table
    for (i = 0; i < result.areas.length; ++i){
      console.log('the ratio is ', ratio);
      var area = "<tr><td>"+(i)+"</td><td>"+result.areas[i]*Math.pow(ratio,2)+"</td></tr>";
      $("#areas").append(area);
    }
  }, "json");
});

function updateCoord() {
  var latlon = map.getCenter();
  var zoom = map.getZoom();
  document.getElementById('current').innerHTML = latlon + ', ' + zoom;
}


Number.prototype.toRad = function() {
   return this * Math.PI / 180;
}

function haversine(lat1, lon1, lat2, lon2) {
  var R = 6371; // km
  //has a problem with the .toRad() method below.
  var x1 = lat2-lat1;
  var dLat = x1.toRad();
  var x2 = lon2-lon1;
  var dLon = x2.toRad();
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1.toRad()) * Math.cos(lat2.toRad()) *
                  Math.sin(dLon/2) * Math.sin(dLon/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var half_diagonal_m = R * c * 1000;
  console.log('distance ', half_diagonal_m)

  var half_diagonal_px = (512/2) * Math.sqrt(2);
  console.log('pixel distance ', half_diagonal_px);

  return half_diagonal_m/half_diagonal_px;

}


$(function changeMap(){
  $("input[name='submit']").on('click', function(){
    var lat = Number($("#lat").val());
    var lon = Number($("#lon").val());
    var ew = $("select[name='eorw']").val();
    var ns = $("select[name='nors']").val();

    if(ew == "E") {ew = 1;}
    else {ew = -1;}
    if(ns == "N") {ns = 1;}
    else {ns = -1;}

    // check for buffoonery
    if (lat == NaN | lon == NaN) {
      alert('Not a Valid GPS location');
    }

    // convert to decimal and update map
    else {
      lat *= ns;
      lon *= ew;
      map.setCenter({lat: lat, lng: lon});
      updateCoord();
    }
  });
});
