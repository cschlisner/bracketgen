window.addEventListener("load", function(){
  	addEV();
})

function addEV(){
	var form = document.getElementById("playerForm");
  	if (form != null){
		form.addEventListener("submit", function (event) {
			event.preventDefault();
			signup();
		});
	}
}

function declare(m, w, tok){
	var data = {
		form: "declare",
		match: m,
		winner: w,
		csrfmiddlewaretoken: tok
	}
	var FD  = new FormData();
	for(name in data) {
    	FD.append(name, data[name]);
	}
	sendForm(FD)
}

function signup(){
	var FD = new FormData(document.getElementById('playerForm'));
	sendForm(FD);
}

function sendForm(formData){
	var XHR = new XMLHttpRequest();

	XHR.addEventListener('load', function(event) {
		console.log(event);
		if (event.target.status == 404){
			var err = document.getElementById("err");
			err.innerHTML = event.target.response;
		}
		else {
			window.location=window.location
		}
	});

	XHR.addEventListener('error', function(event) {
		alert('Server Error.');
	});

	XHR.open('POST', '');

	XHR.send(formData);
}