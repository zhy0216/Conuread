! function (definition) {
  if (typeof module == "object" && module.exports) module.exports = definition();
  else if (typeof define == "function") define(definition);
  else this.tz = definition();
} (function () {
  var slice = [].slice, published = {}, subscriptions = {}, samples = {};

  function Signal () {
    function publish (path) {
      var source = published[path];
      if (!source) {
        source = function () {
          var subscribers = subscriptions[path],
              once = samples[path] || [],
              i, I;
          for (i = 0, I = subscribers.length; i < I; i++) 
            subscribers[i].apply(this, arguments);
          for (i = once.length - 1; i != -1; i--)
            subscribers.splice(once[1], 1);
        }
        published[path] = source;
        source.path = path;
        source.count = 0;
      }
      source.count++;
      return source;
    }

    function subscribe (path, sink) {
      if (!subscriptions[path]) subscriptions[path] = [];
      subscriptions[path].push(sink);
    }

    function sample (path, sink) {
      if (!samples[path]) samples[path] = [];
      subscribe(path, sink);
      samples[path].push(subscriptions.length - 1);
    }

    this.publish = publish;
    this.subscribe = subscribe;
    this.sample = sample;
  }

  return { createSignal: function () { return new Signal() } }
});
