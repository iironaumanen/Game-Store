var buttons = {
  37: 'L',
  40: 'U',
  39: 'R',
  38: 'D'
};

class Box {
  constructor(ctx, width, height) {
    this._ctx = ctx;
    this._width = width;
    this._height = height;
    this._x = 0;
    this._y = 0;
    this._speed = 30;
    document.addEventListener('keydown', this.keydown.bind(this)) //
  }

  draw() { // Draw box
    this._ctx.beginPath();
    this._ctx.rect(this._x, this._y, this._width, this._height);
    this._ctx.fillStyle = 'black';
    this._ctx.fill();
  }

  // Get box border locations
  getBorder() {
    return {
      xMin: this._x,
      xMax: this._x + this._width,
      yMin: this._y,
      yMax: this._y + this._height,
    }
  }

  // Check if a position is inside the box
  contains(x, y) {
    let borders = this.getBorder()
    return (borders.xMin <= x &&
        borders.xMax >= x &&
        borders.yMin <= y &&
        borders.yMax >= y );
  }

  // Match a button press with correct movement
  keydown(e) {
    switch(buttons[e.keyCode]) {
      case 'L':
        this._x -= this._speed;
        break;
      case 'R':
        this._x += this._speed;
        break;
      case 'U':
        this._y += this._speed;
        break;
      case 'D':
        this._y -= this._speed;
        break;
      default:
        break;
    }
  }

  getX() {
    return this._x;
  }

  getY() {
    return this._y;
  }

  setPos(x, y) {
    this._x = x;
    this._y = y;
  }
}
