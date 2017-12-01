var field = document.getElementsByClassName('field_box')[0];
var loseBox = document.getElementsByClassName('lose_box')[0];
var scoreCounterBox = document.getElementsByClassName('info_score_counter')[0];
var reloadBtn = document.getElementsByClassName('lose_repeatgame_btn')[0];


reloadBtn.onclick = function() {window.location.reload();};

var reloadBtn = document.getElementsByClassName('lose_repeatgame_btn')[0];

//time counter
var timeCounterBox = document.getElementsByClassName('info_time_counter')[0];

var timeCounter = 0;

var timeCounterInterval = setInterval(function(){
	timeCounterBox.innerHTML = String(timeCounter);
	timeCounter++;
},1000);


function randint(min, max) {
	return Math.round(min + Math.random()*(max-min));
};

// initialization function
function init(cells_amount) {
	// cells initialization
	for (var i=0; i<cells_amount; i++) {
		var newCell = document.createElement('div');
	 	newCell.className = 'cell';
		field.appendChild(newCell);
	};
};

init(1750);

function transformCoordinates(x,y) {
	var result = 50*(y-1)+x; 
	return result-1;
};


function clearField() {
	for (var i = 0; i<field.children.length; i++) {
		field.children[i].className = "cell";
	}
}

var infoAjax = document.getElementsByClassName('info_ajax')[0];

var snakesCount = 0;

function request() {
	var xhr = new XMLHttpRequest();

	xhr.open("POST", '/channel', true)
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
	xhr.onreadystatechange = function() { // (3)
	  if (xhr.readyState != 4) return;

	  if (xhr.status != 200) {
	    alert(xhr.status + ': ' + xhr.statusText);
	  } else {
	  	clearField();
	    var response = JSON.parse(xhr.responseText);
	    if (response['status'] == "OK") {
	    	snakesCount = 0;
	    	var info = response['info'];
	    	var appleCellCoordinates = Number(info['appleCell']);
	    	var appleCell = document.getElementsByClassName('cell')[appleCellCoordinates-1];
	    	appleCell.className = 'cell apple_cell';


	    	var snakes = info['snakesCells'];

	    	for (var i = 0; i < snakes.length; i++) {

	    		var cells = snakes[i][1];

	    		for (var x = 0; x < cells.length; x++) {
	    			var cell = document.getElementsByClassName('cell')[cells[x]-1];

	    			if (snakesCount==3) {
	    				cell.className = 'cell snake4_cell';
	    			}
	    			if (snakesCount==2) {
	    				cell.className = 'cell snake3_cell';
	    			}
	    			if (snakesCount==1) {
	    				cell.className = 'cell snake2_cell';
	    			}
	    			if (snakesCount==0) {
	    				cell.className = 'cell snake1_cell';
	    			}

	    		}

	    	snakesCount++;

	   		}

	    } else {
	    	window.location.replace('/lose');
	    }
	  }

	}

	xhr.send(body+'&action=' + encodeURIComponent('0'));
}

setInterval(request, 60);


function ajaxMove(direction) {
	var xhr = new XMLHttpRequest();

	xhr.open("POST", '/channel', true)
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')

	xhr.onreadystatechange = function() { // (3)
	  if (xhr.readyState != 4) return;

	  if (xhr.status != 200) {
	    alert(xhr.status + ': ' + xhr.statusText);
	  } 
	}
	xhr.send(body+'&action=' + encodeURIComponent(String(direction)));
}

window.onkeydown = function(event) {						// check BUG, for example, bottom, left, top - BUG
	if (event.keyCode == 38) { ajaxMove(1) };
	if (event.keyCode == 39) { ajaxMove(2) };
	if (event.keyCode == 40) { ajaxMove(3) };
	if (event.keyCode == 37) { ajaxMove(4) };
};