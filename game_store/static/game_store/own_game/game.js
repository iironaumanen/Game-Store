class Game {
  constructor(canvas, w, h) {
    this._width = w;
    canvas.width = w;
    this._height = h;
    canvas.height = h;
    this._ctx = canvas.getContext('2d');
    this.box = new Box(this._ctx, this._width/10, this._width/10); // create a simple player
    this._point = this.newPoint();
    this._score = 0;
    this._pointsPer = 10;
    this._start = true;
  }

  run() {
    this.nuke(); // Clear everything
    this._ctx.beginPath();
    this._ctx.rect(0, 0, this._width, this._height); // Draw borders
    this._ctx.stroke();
    this.box.draw(); // Draw player box

    this._point.draw();
    this.drawScore()

    if (this.notLosing()) { // Resume as normal if we are still within the borders
      if(this.box.contains(this._point.getX(), this._point.getY())) {
        this._score += this._pointsPer;
        this._point = this.newPoint();
      }
      requestAnimationFrame(this.run.bind(this));
    } else { // Display loss message
      this.theEnd();
    }
  }

  // Create a new point somewhere outside the player box
  newPoint() {
    let x = Math.floor(Math.random() * (this._width + 1)); // A random integer from 0 to 9
    let y = Math.floor(Math.random() * (this._height + 1)); // A random integer from 0 to 9
    while(this.box.contains(x,y)) {
      x = Math.floor(Math.random() * (this._width + 1)); // A random integer from 0 to 9
      y = Math.floor(Math.random() * (this._height + 1)); // A random integer from 0 to 9
    }
    return new Point(this._ctx, x, y);
  }

  notLosing() {
    let borders = this.box.getBorder();
    return (borders.xMin >= 0 &&
      borders.xMax <= this._width &&
      borders.yMin >= 0 &&
      borders.yMax <= this._height);
  }

  theEnd() { // Draw loss message
    this._ctx.beginPath();
    this._ctx.font = '48px serif';
    this._ctx.fillStyle = 'red';
    this._ctx.fillText("YOU LOSE", this._width/2, this._height/2);
  }

  drawScore() { // Draw loss message
    this._ctx.beginPath();
    this._ctx.font = '20px serif';
    this._ctx.fillStyle = 'green';
    this._ctx.fillText("SCORE: "+this._score , this._width/2-50, this._height-5);
  }

  nuke() { // Clear out eveything
    this._ctx.clearRect(0, 0, this._width, this._height);
  }

  getState() {
    return {
      posX: this.box.getX(),
      posY: this.box.getY(),
      score: this._score,
      pointX: this._point.getX(),
      pointY: this._point.getY(),
    };
  }

  getScore() {
    return this._score;
  }

  setState(state) {
    this._score = state['score'];
    this.box.setPos(state['posX'], state['posY']);
    this._point.setPos(state['pointX'], state['pointY']);
  }

  getWidth() {
    return this._width+ 20;
  }

  getHeight() {
    return this._height + 80;
  }
}

// Create a game
var game = new Game(document.getElementsByTagName('canvas')[0], 700, 400);

$(function() {
  parent.postMessage({
    messageType: 'SETTING',
    options: {
      'width': game.getWidth(),
      'height': game.getHeight(),
    }});

  function save() {
    const save = {
      messageType: "SAVE",
      gameState: game.getState(),
    };
    parent.postMessage(save, "*");
  }
  function load(state) {
    game.setState(state);
  }
  function handlemsg(e) {
    if(e.data.messageType === 'LOAD') {
      load(e.data.gameState);
    }
  }
  function requestLoad(e) {
    const msg = { messageType:  'LOAD_REQUEST', };
    parent.postMessage(msg , "*");
  }
  function submit(e) {
    const msg = { messageType: 'SCORE', score: game.getScore(), };
    parent.postMessage(msg, "*");
  }

  if (!window.addEventListener) { // <= IE8
    window.attachEvent("onmessage", handlemsg);
  } else { // > IE8
    window.addEventListener('message', handlemsg, false);
  }
  document.getElementById('load').addEventListener('click', requestLoad)
  document.getElementById('save').addEventListener('click', save)
  document.getElementById('submit').addEventListener('click', submit)
})

// Start the game up
requestAnimationFrame(game.run.bind(game));
