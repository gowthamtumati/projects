$(document).ready(function() {
 
    // Your code here.
    console.log("Tweet Search");

    //Getting input Query
    var inputQuery;
    var indexChoice;

    $( "#searchButton" ).click(function() {
	  	inputQuery = $('#inputQuery').val();
    	console.log(inputQuery);
    	indexChoice = $('#indexChoice').val();
    	console.log(indexChoice);
    	
		
		var url;
		if (indexChoice == "1") {
			url = "http://localhost:8080/InitiateSearch/webapi/search/lucene/";
		} else {
			url = "http://localhost:8080/InitiateSearch/webapi/search/hadoop/";
		}
    	// $('#results').show();
    	// $('#myTable').DataTable().clear().destroy();

    	//Making AJAX request to get the data
		$body = $("body");
		$body.addClass("loading");
		
    	url = url+inputQuery;
    	$.ajax({
		    url : url,
		    type : 'GET',
		    dataType:'json',
		    success : function(data) {   
		    	$body.removeClass("loading");
		    	
				var locations = [];
				for (var i=0; i<data.length; i++) {
					var coord = data[i]["coordinates"].trim();
					locations.push(coord.split(" "));
				}
				
				var first_location = [39.381266, -97.922211];
				var latitude = 39.381266;
				var longitute = -97.922211;
				if (locations.length != 0) {
					latitude = parseFloat(locations[0][0]);
					longitude = parseFloat(locations[0][1]);				
				}
				//Display in Leaflet
				
				$('#outermap').html('<div id="map" style="width: 500px; height: 400px;"></div>');
				var map = L.map('map').setView([latitude, longitude], 100000);
				
		        mapLink = 
		            '<a href="http://openstreetmap.org">OpenStreetMap</a>';
		        L.tileLayer(
		            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		            attribution: '&copy; ' + mapLink + ' Contributors',
		            maxZoom: 5,
		            }).addTo(map);

				for (var i = 0; i < locations.length; i++) {
					marker = new L.marker([locations[i][0],locations[i][1]])
						.addTo(map);
				}
				
				
		        //Display in Map
				/*
		        var locations = [
			      ['Bondi Beach', -33.890542, 151.274856, 4],
			      ['Coogee Beach', -33.923036, 151.259052, 5],
			      ['Cronulla Beach', -34.028249, 151.157507, 3],
			      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
			      ['Maroubra Beach', -33.950198, 151.259302, 1]
			    ];
				*/
				
				
				/*
		        var map = new google.maps.Map(document.getElementById('map'), {
			      zoom: 10,
			      center: new google.maps.LatLng(39.381266, -97.922211),
			      mapTypeId: google.maps.MapTypeId.ROADMAP
			    });

			    var infowindow = new google.maps.InfoWindow();

			    var marker, i;

			    for (i = 0; i < locations.length; i++) {  
			      marker = new google.maps.Marker({
			        position: new google.maps.LatLng(locations[i][0], locations[i][1]),
			        map: map
			      });

			      google.maps.event.addListener(marker, 'click', (function(marker, i) {
			        return function() {
			          //infowindow.setContent(locations[i][0]);
			          infowindow.open(map, marker);
			        }
			      })(marker, i));
			    }
			    */

		        //End of Map



		        $('#results').show();
		        $('#results').DataTable({
		        	"data": data,
		        	"columns": [
		        		{ "data" : "hashTag" },
		        		{ "data" : "tweet" },
		        		{ "data" : "title" },
		        		{ "data" : "URL",
		        			"render": function(data, type, row, meta) {
		        				if (type == 'display') {
		        					data = '<a href="'+data+'">'+data+'</a>';
		        				}
		        				return data;
		        			}
		        			
		        		
		        		},
						{ "data" : "createdAt" },
		        	],
		        	"columnDefs": [{
					    "defaultContent": "-",
					    "targets": "_all"
					}],
					"bDestroy": true,
		        });
		    },
		    error : function(request,error)
		    {
		        console.log("Request: "+JSON.stringify(request));
		    }
		});


	});
 
});