var box = document.getElementById('dvd'),
  win = window,
  ww = win.innerWidth,
  wh = win.innerHeight,
  speed = 7,
  request = null;

const front = document.getElementById('front');

  Array.prototype.random = function () {
    return this[Math.floor((Math.random()*this.length))];
  };

  var names = [ 'frog', 'snoop', 'bigguy'];
  const elems = [];
  for(const name of names) {
    const e = document.getElementById(name);
    elems.push({
      elem: e,
      translateX: Math.floor((Math.random() * ww) + 1),
      translateY: Math.floor((Math.random() * wh) + 1),
      boxWidth: e.offsetWidth,
      boxHeight: e.offsetHeight,
      boxTop: e.offsetTop,
      boxLeft: e.offsetLeft,
      xMin: -e.offsetLeft,
      yMin: -e.offsetTop,
      xMax: win.innerWidth - e.offsetLeft - e.offsetWidth,
      yMax: win.innerHeight - e.offsetTop - e.offsetHeight,
      //request: null,
      direction: ['ne', 'nw', 'se', 'sw'].random(),
      timeout: null,
    });
  }



init();

// reset constraints on resize
window.addEventListener('resize', function(argument) {
  for(const elem of elems) {
    clearTimeout(elem.timeout);
    elem.timeout = setTimeout(update, 100);
  }
}, false);

function init() {
  request = requestAnimationFrame(init);
  //for(const elem of elems) {
  //  elem.request = requestAnimationFrame(init);
  //}
  move();
  // setInterval(function() {
  //   move();
  // }, 16.66);
}

// reset constraints
function update() {
  for(const elem of elems) {
    elem.xMin = -elem.boxLeft;
    elem.yMin = -elem.boxTop;
    elem.xMax = win.innerWidth - elem.boxLeft - elem.boxWidth;
    elem.yMax = win.innerHeight - elem.boxTop - elem.boxHeight;
  }
}

function move() {
  setDirection();
  for(const elem of elems) {
    setStyle(elem.elem, {
      transform: 'translate3d(' + elem.translateX + 'px, ' + elem.translateY + 'px, 0)',
    });
  }
}

function setDirection() {
  for(const elem of elems) {
    switch (elem.direction) {
      case 'ne':
        elem.translateX += speed;
        elem.translateY -= speed;
        break;
      case 'nw':
        elem.translateX -= speed;
        elem.translateY -= speed;
        break;
      case 'se':
        elem.translateX += speed;
        elem.translateY += speed;
        break;
      case 'sw':
        elem.translateX -= speed;
        elem.translateY += speed;
        break;
    }
  }

  setLimits();
}

function setLimits() {
  for(const elem of elems) {
    if (elem.translateY <= elem.yMin) {
      if (elem.direction == 'nw') {
        elem.direction = 'sw';
      } else if (elem.direction == 'ne') {
        elem.direction = 'se';
      }
      //switchColor();
    }
    if (elem.translateY >= elem.yMax) {
      if (elem.direction == 'se') {
        elem.direction = 'ne';
      } else if (elem.direction == 'sw') {
        elem.direction = 'nw';
      }
      //switchColor();
    }
    if (elem.translateX <= elem.xMin) {
      if (elem.direction == 'nw') {
        elem.direction = 'ne';
      } else if (elem.direction == 'sw') {
        elem.direction = 'se';
      }
      //switchColor();
    }
    if (elem.translateX >= elem.xMax) {
      if (elem.direction == 'ne') {
        elem.direction = 'nw';
      } else if (elem.direction == 'se') {
        elem.direction = 'sw';
      }
      //switchColor();
    }
  }
}

function getVendor() {
  var ua = navigator.userAgent.toLowerCase(),
    match = /opera/.exec(ua) || /msie/.exec(ua) || /firefox/.exec(ua) || /(chrome|safari)/.exec(ua) || /trident/.exec(ua),
    vendors = {
      opera: '-o-',
      chrome: '-webkit-',
      safari: '-webkit-',
      firefox: '-moz-',
      trident: '-ms-',
      msie: '-ms-',
    };

  return vendors[match[0]];
}

function setStyle(element, properties) {
  var prefix = getVendor(),
    property, css = '';
  for (property in properties) {
    css += property + ': ' + properties[property] + ';';
    css += prefix + property + ': ' + properties[property] + ';';
  }
  element.style.cssText += css;
}

var hitmarker = function() {
  this.marker = new Image(300,300);
  this.marker.src = 'https://raw.githubusercontent.com/kid-icarus/hitmarker.js/master/hitmaker.png';
  this.marker.style.position = 'absolute';
  this.marker.style.display = 'none';
  this.marker.style.cssText += 'user-drag: none; user-select: none;-moz-user-select: none;-webkit-user-drag: none;-webkit-user-select: none;-ms-user-select: none;';
  this.init();
};

hitmarker.prototype.init = function() {
  var self = this;
  document.body.appendChild(self.marker);
};

const markers = [new hitmarker(), new hitmarker(), new hitmarker()];
const clack = document.createElement('audio');
clack.src = 'https://raw.githubusercontent.com/kid-icarus/hitmarker.js/master/hitmaker.mp3';
var n = 0;

function overLappingPlay(audioNode) {
  var clone = audioNode.cloneNode(true);
  clone.play();
}

var mouseX = 0;
var mouseY = 0;
$('body').mousemove(function( event ) {
  mouseX = event.pageX;
  mouseY = event.pageY;
});

var spreadRadius = 150;

function fire(hm, x, y) {
  hm.marker.style.top = (y - 150) + ((Math.random()-0.5)*spreadRadius) + 'px';
  hm.marker.style.left = (x - 150) + ((Math.random()-0.5)*spreadRadius) + 'px';
  hm.marker.style.display = 'block';
  overLappingPlay(clack);
  window.setTimeout(function() {
    hm.marker.style.display = 'hidden';
  }, 10);
}

function firenext() {
  if(n >= markers.length) n = 0;
  fire(markers[n], mouseX, mouseY);
  n++;
}

var interval = null;
function letsgo() {
  firenext();
  interval = setInterval(firenext, 50);
}

document.body.onmousedown = function() {
  letsgo();
};
document.body.onmouseup = function() {
  clearInterval(interval);
};
document.body.onmouseout = function() {
  clearInterval(interval);
};
