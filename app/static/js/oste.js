var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 32.84445431845944, lng: -96.78474766922},
    zoom: 18,
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

  var latlon = map.getCenter();
  var lat = latlon.lat();
  var lon = latlon.lng();

  var z = map.getZoom();
  $.post(url, {'lat':lat, 'lon':lon, 'zoom':z}, function(result){
    console.log(result.url);
    console.log(result.areas);
    $("#edge").attr('src', result.url);
    console.log(result.areas.length);
    for (i = 0; i < result.areas.length; ++i){
      var x = "<tr><td>"+(i+1)+"</td><td>"+result.areas[i]+"</td></tr>";
      $("#areas").append(x);
    }
  }, "json");
});

function updateCoord() {
  var latlon = map.getCenter();
  var zoom = map.getZoom();
  document.getElementById('current').innerHTML = latlon + ', ' + zoom;
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
