var cards;
var deck = Array();
var currentcard = 0;
var misses = Array();

function shuffle() {
  deck.sort(function() { return 0.5 - Math.random()} );
}

function tileCards() {
  cards = getElementsByTagAndClassName("div", "cardfront");
  for(var i=0; i<cards.length; i++) {
    connect("card-" + i, "onclick", flip);
    setStyle("card-"+i, {'display':'none'});
    deck.push(cards[i]);
  }

  connect("yes", "onclick", hit);
  connect("no", "onclick", miss);
  connect("reset", "onclick", reset);
  connect("reset2", "onclick", reset);
  connect("redo", "onclick", redo);

  reset(0);
}

// newdeck=0 if you do not want to rebuild the deck
function reset(newdeck) {
  if((newdeck != 0) || (deck.length == 0)) {
    deck = Array();
    forEach(getElementsByTagAndClassName("div", "cardfront"),
      function(card) {
        deck.push(card);
    });
  }

  forEach(getElementsByTagAndClassName("div", "card"),
    function(card) {
      setStyle(card, {'display':'none'});
  });

  $('num-cards').innerHTML = deck.length;
  shuffle();
  currentcard = deck.pop();
  setStyle(currentcard, {'display':'block'});
  setStyle("yesno", {'display':'none'});
  setStyle("endbuttons", {'display':'none'});
  $('hits').innerHTML = 0;
  $('misses').innerHTML = 0;
  $('score').innerHTML = "";
  misses = Array();
  setStyle("redo", {'display':'none'});
}

function redo() {
  deck = Array();
  for(var i=0; i<misses.length; i++) {
    deck.push(misses[i]);
  }
  reset(0);
}

function flip(e) {
  var back = $(e.src().id + "-back");
  setStyle(back, {'z-index':'1000', 'display':'block'});
  //connect(back, "onclick", next);
  setStyle(e.src().id, {'display':'none'});
  setStyle("yesno", {'display':'block'});
}

function hit() {
  $('hits').innerHTML = parseInt($('hits').innerHTML) + 1;
  next();
}

function miss() {
  $('misses').innerHTML = parseInt($('misses').innerHTML) + 1;
  misses.push(currentcard);
  setStyle("redo", {'display':'inline'});
  next();
}

function next() {
  var id = currentcard.id + "-back";
  setStyle(id, {'display':'none'});
  setStyle("yesno", {'display':'none'});
  if(deck.length == 0) {
    setStyle("endbuttons", {'display':'block'});
    var score = parseInt($("hits").innerHTML) / parseInt($("num-cards").innerHTML);
    $("score").innerHTML = Math.round(score * 10000) / 100;
    return;
  }
  currentcard = deck.pop();
  setStyle(currentcard, {'display':'block'});
}


function keyPress(e) {
  var letter = e.key().string;
  if(letter == " ") {
    if(getStyle("endbuttons", "display") == "block") { return; }
    else if(hasElementClass(currentcard, "cardfront")) {
      e.preventDefault();
      signal(currentcard, "onclick", {'src':function(){return currentcard;}});
    }
  }
  else if (getStyle("yesno", "display") == "block") {
    if (letter == 'y') {
      hit();
    }
    else if (letter == 'n') {
      miss();
    }
  }
}

function initKeyListener() {
  connect(document, "onkeypress", keyPress);
}

addLoadEvent(initKeyListener);
addLoadEvent(tileCards);
