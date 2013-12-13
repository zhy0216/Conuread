var $ = require("jquery");
var _ = require("underscore");
var signal = require('signal').createSignal(); 

var SubChooser = require("page/leftsidebar").SubChooser;
var ContentShower = require("page/contentshower").ContentShower;

var UserPlugin = require("page/userplugin").UserPlugin;

require("jquery.routes");
require("jquery.ba-outside-events");
require("./libs/bootstrap/js/bootstrap.js");

﻿$(function(){
    var subchooser = new SubChooser();
    var contentShower = new ContentShower();
    var userPlugin = new UserPlugin();
    subchooser.init();
    contentShower.init();
    userPlugin.init();
    signal.subscribe('feed-read', subchooser.feedReadAction);
    signal.subscribe('feedsite-fetch', function(feedsiteid){
        console.log(feedsiteid);
        $.post("/api/feedsite/" + feedsiteid,function(data){
            console.log(data);
            if(data.rcode == 200){
                contentShower.setFeedListData(data.feeds);
                contentShower.scrollTop().cleanTarget().render();
            }
        })
    });

    //define router

    // $.routes.add('/feedsite/{feedsiteid:word}', function() {
    //     console.log('feedsiteid1:' + this.feedsiteid);
    //     
    // });


});
