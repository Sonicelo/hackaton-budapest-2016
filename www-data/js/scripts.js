// Shorthand for $( document ).ready()
$(function() {
    var ipAddress = "192.168.1.101:8080";
    var sound;

    var displayImage = function(imageID){
         $(".image").css('background-image', "url('images/" + imageID + "')")
    };


    var stopSound = function(){
        if(typeof sound !== 'undefined'){
            sound.stop();
        }
    };

    var playSound = function(soundTrack){
        sound = new Howl([soundTrack]);
        sound.start();
    };

    var theLoop = function(){
        var data = {
            url: ipAddress + 'data.json' ,
            data: {},
            type: "POST",
            dataType: "json"
        };

        $.ajax(data).done(function (json){
            if(typeof json.image !== 'undefined'){
                displayImage(json.image);
            }
            if(typeof json.sound !== 'undefined'){
                stopSound();
                playSound(json.sound);
            }

        }).fail(function (xhr, status, errorThrown){
            alert('An Error occoured (sad face).');
        });

        setTimeout(theLoop, 100);
    };

    theLoop();
    console.log( "Neurofeedback Loop Ready!" );
});