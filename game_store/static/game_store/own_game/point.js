class Point{
  constructor(ctx, x, y) {
    this._ctx = ctx;
    this._width = 10;
    this._height = 10;
    this._x = x;
    this._y = y;
  }

  draw() { // Draw point
    this._ctx.beginPath();
    this._ctx.fillStyle = 'green';
    this._ctx.fill();
    this._ctx.fillRect(this._x, this._y, this._width, this._height);
  }

  getBorder() {
    return {
      xMin: this._x,
      xMax: this._x + this._width,
      yMin: this._y,
      yMax: this._y + this._height,
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
