var $ = require("jquery");
var _ = require("underscore");
var signal = require('signal').createSignal(); 

var SubChooser = require("page/leftsidebar").SubChooser;
var ContentShower = require("page/contentshower").ContentShower;

require("jquery.routes");
require("./libs/bootstrap/js/bootstrap.js");

﻿$(function(){
    var subchooser = new SubChooser();
    var contentShower = new ContentShower();
    subchooser.init();
    contentShower.init();
    signal.subscribe('feed-read', subchooser.feedReadAction);


    //define router

    // $.routes.add('/feedsite/{feedsiteid:word}', function() {
    //     console.log('feedsiteid1:' + this.feedsiteid);
    //     $.post("/api/feedsite/"+this.feedsiteid,function(data){
    //         console.log(data);
    //         if(data.rcode == 200){
    //             contentShower.setFeedListData(data.feeds);
    //             contentShower.scrollTop().cleanTarget().render();
    //         }
    //     })
    // });


});
