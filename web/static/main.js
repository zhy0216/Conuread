var $ = require("jquery");
var _ = require("underscore");
var signal = require('signal').createSignal(); 

var SubChooser = require("page/leftsidebar").SubChooser;
var ContentShower = require("page/contentshower").ContentShower;

require("jquery.routes"); //https://github.com/thorsteinsson/jquery-routes
require("./libs/bootstrap/js/bootstrap.js");

﻿$(function(){
    var subchooser = new SubChooser();
    var contentshower = new ContentShower();
    subchooser.init();
    contentshower.init();
    signal.subscribe('test', function(){
        console.log("test1");
    });

});
