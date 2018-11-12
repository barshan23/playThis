var musics, playing;
function playSong(id) {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState === XMLHttpRequest.DONE) {
			if (request.status === 200) {
				console.log(playing);
				console.log(id);
				if (playing)
					document.getElementById(playing).classList.remove("playing");
				document.getElementById(id).classList.add("playing");
				playing = id;
				if (!document.querySelector('button.play').classList.contains('paused'))
					document.querySelector('button.play').classList.add('paused');
			}
		}
	};
	// console.log('/url/'+musics[id]);
	request.open('GET', '/url/'+musics[id]);
	request.send();
}

(function() {
	document.getElementById('play').addEventListener('click',function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function(){
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// show playing
					response = JSON.parse(request.responseText);
					console.log(response);
					console.log(request);
					if (response.done && !document.querySelector('button.play').classList.contains('paused') && !request.responseURL.match(/pp$/))
						document.querySelector('button.play').classList.add('paused');
					if (response.done && request.responseURL.match(/pp$/)){ // mathces urls ending with pp
						document.getElementById('play').classList.toggle('paused');
						// console.log(request.responseURL.match(/pp$/));
					}
					playing = null;
				}
			}
		};
		var url = document.getElementById('url').value;
		// console.log(url);
		if (url.length > 0){
			if (playing){
				document.getElementById(playing).classList.remove("playing");
				stop();
			}
			// stop();
			request.open('POST', '/url');
			request.setRequestHeader("Content-Type", "application/json");
			request.send(JSON.stringify({url:url}));
			document.getElementById('url').value = '';
		}else {
			request.open('GET', '/pp');
			request.send();
		}
	});

	var stop = function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// stopped
					if (playing){
						document.getElementById(playing).classList.remove("playing");
						playing = null;
					}
					if (document.querySelector('button.play').classList.contains('paused'))
						document.querySelector('button.play').classList.remove('paused');
				}
			}
		};
		request.open('GET', '/stop');
		request.send();
	};
	document.getElementById('stop').addEventListener('click',stop);

	document.getElementById('fscreen').addEventListener('click',function() {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 200) {
					// full screen successful
					response = JSON.parse(request.responseText);
					console.log(response);
					if (response.done){
						let but = document.getElementById('fscreen');
						if (but.innerText === 'Fullscreen') {
							but.innerText = 'Exit Fullscreen';
						}else {
							but.innerText = 'Fullscreen';
						}
					}
				}
			}
		};
		request.open('GET', '/fscreen');
		request.send();
		
		// console.log(document.getElementById('pause').innerText);
	});

	var slider = document.getElementById("myRange");
	console.log(slider.value)

	// Update the current slider value (each time you drag the slider handle)
	slider.oninput = function() {
		var request = new XMLHttpRequest();
		request.open('GET', '/vol/'+this.value);
		request.send();
		// output.innerHTML = this.value;
		console.log(this.value)
	}

	// list to put the musics
	var music_list = document.getElementById('musics');


	window.onload = function() {
		get_volume();
		get_list();
	}

	// gets the initial value of sound
	var get_volume = function () {
		var request = new XMLHttpRequest();
		request.open('GET', '/getvol');
		request.onreadystatechange = function() {
			if (request.readyState == XMLHttpRequest.DONE) {
				var sound = request.responseText;	
				console.log(sound);
				slider.value = sound;
			}
		}
		request.send();
	}

	var get_list = function() {
		var request = new XMLHttpRequest();
		request.open('GET', '/musics');
		request.onreadystatechange = function() {
			if (request.readyState == XMLHttpRequest.DONE) {
				musics = JSON.parse(request.responseText);	
				console.log(musics);
				for (const [index, music] of musics.entries()){
					// console.log(index + music);
					var newElement = document.createElement('li');
					newElement.setAttribute('id', index);
					newElement.setAttribute('onClick', "playSong("+index+")");
					newElement.innerHTML = '<a>'+music+'</a>';
					music_list.appendChild(newElement);
				}
			}
		}
		request.send();
	}

})();
