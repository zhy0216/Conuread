#!/usr/bin/env node

require('proof')(2, function (equal) {
  var signal = require('../..').createSignal(),
      source = signal.publish('namespace.name'),
      count = 0;

  signal.subscribe('namespace.name', sink);

  source(1);
  source(2);

  function sink (number) {
    count++;
    equal(number, count, 'message sent: ' + count);
  }
});
