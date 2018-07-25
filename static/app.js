(function() {


	document.getElementById('play').addEventListener('click',function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// show playing
				}
			}
		};
		var url = document.getElementById('url').value;
		console.log(url);
		request.open('GET', '/url/'+url);
		request.send();
	});


	document.getElementById('stop').addEventListener('click',function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// stopped
				}
			}
		};
		request.open('GET', '/stop');
		request.send();
	});

})();