
// Shorthand for $( document ).ready()
$(function() {
    var ipAddress = window.location.origin;
    var sound, intervalID;

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
            url: ipAddress + '/data.json' ,
            data: {},
            type: "GET",
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
            clearTimeout(intervalID);
        });

        intervalID = setTimeout(theLoop, 100);
    };

    theLoop();
    console.log( "Neurofeedback Loop Ready!" );
});
