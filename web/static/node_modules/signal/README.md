# Signal [![Build Status](https://secure.travis-ci.org/bigeasy/signal.png?branch=master)](http://travis-ci.org/bigeasy/signal)

A minimalist event library for web applications.

```javascript
var signal = require('signal').createConduit(),
    equal = require('assert').equal;

var source = signal.publish('namespace.name');
signal.subscribe('namespace.name', sink);

source(1);

function sink (number) {
  equal(number, 1, 'got a number');
}
```

## Change Log

Changes for each release.

### Version 0.0.1

*Released: Mon Nov  5 03:38:32 UTC 2012*

 * Fix description and links in package.json. #10.
 * Add MIT license. #11.

### Version 0.0.0

*Released: Wed Aug  8 02:08:47 UTC 2012*

 * Create facility to subscribe to only one event. #6.
 * Create publish and subscribe. #5.
 * Build on Travis CI. #3.
