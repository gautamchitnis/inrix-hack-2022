
function myMap() {
    var mapProp= {
        
      center:new google.maps.LatLng(37.770615458787795, -122.42753365146659),
      zoom:12,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
    var map2 = new google.maps.Map(document.getElementById("googleMap2"),mapProp);
        async function postData(url = '', data = {}) {
        const response = await fetch(url, {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify(data) // body data type must match "Content-Type" header
        });
        return response; 
        }
        postData('https://c572-129-210-115-231.ngrok.io/app/get/locations',{}).then(
            response=>response.json()).then((data2)=>{
                console.log(data2.locations.length,data2.locations)
                var infowindow =  new google.maps.InfoWindow({});
                var marker, count;
                for (count = 0; count < data2.hubs.length; count++) {
                    // console.log(data2.hubs[count])
                    marker = new google.maps.Marker({
                    position: new google.maps.LatLng(data2.hubs[count][0], data2.hubs[count][1]),
                    map: map,
                    icon:{url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"},
                    title: ""
                    });
                google.maps.event.addListener(marker, 'click', (function (marker, count) {
                    return function () {
                        infowindow.setContent('');
                        infowindow.open(map, marker);
                    }
                    })(marker, count));
                }
                for (count = 0; count < data2.locations.length; count++) {
                    marker = new google.maps.Marker({
                    position: new google.maps.LatLng(data2.locations[count][0], data2.locations[count][1]),
                    map: map,
                    title: ""
                    });
                google.maps.event.addListener(marker, 'click', (function (marker, count) {
                    return function () {
                        infowindow.setContent("");
                        infowindow.open(map, marker);
                    }
                    })(marker, count));
                }
            })
        
    fetch('https://api.openchargemap.io/v3/poi?key="9Bob6Tv6Kgx-FLEFMhfLJp-qMkYWX9XZU03dmHlXCCw"&distance=100&latitude=37.752644&longitude=-122.446876').then(
        response=>response.json()).then(data3=>{
                var infowindow =  new google.maps.InfoWindow({});
                var marker, count;
                // console.log(data3.length,data3[0].AddressInfo.Latitude)
                for (count = 0; count < data3.length; count++) {
                    marker = new google.maps.Marker({
                    position: new google.maps.LatLng(data3[count].AddressInfo.Latitude, data3[count].AddressInfo.Longitude),
                    map: map2,
                    icon:{url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"},
                    title: ""
                    });
                google.maps.event.addListener(marker, 'click', (function (marker, count) {
                    return function () {
                        infowindow.setContent('');
                        infowindow.open(map, marker);
                    }
                    })(marker, count));
                }
        })
    }