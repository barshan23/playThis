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
		request.open('POST', '/url');
		request.setRequestHeader("Content-Type", "application/json");
		request.send(JSON.stringify({url:url}));
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

	document.getElementById('pause').addEventListener('click',function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// stopped
				}
			}
		};
		request.open('GET', '/pp');
		request.send();
		let but = document.getElementById('pause');
		if (but.innerText === 'Pause') {
			but.innerText = 'Play'
		}else {
			but.innerText = 'Pause'
		}
		// console.log(document.getElementById('pause').innerText);
	});

	document.getElementById('fscreen').addEventListener('click',function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// stopped
				}
			}
		};
		request.open('GET', '/fscreen');
		request.send();
		let but = document.getElementById('fscreen');
		if (but.innerText === 'Fullscreen') {
			but.innerText = 'Exit Fullscreen'
		}else {
			but.innerText = 'Fullscreen'
		}
		// console.log(document.getElementById('pause').innerText);
	});

})();