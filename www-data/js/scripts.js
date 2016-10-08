// Shorthand for $( document ).ready()
$(function() {
    var ipAddress = "http://192.168.0.101:8080";
    var remote = false;
    var line = 0;
    var sound, intervalID, counter;

    var displayImage = function(imageID){
         $(".image").css('background-image', "url('images/" + decodeURI(imageID) + "')");
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

    var data = {
        url: ipAddress + '/data.json' ,
        data: {},
        type: "GET",
        dataType: "json"
    };
    var theLoop = function(){

        if(remote) {
            $.ajax(data).done(function (json) {
                if(typeof json.done !== 'undefined'){
                    clearTimeout(intervalID);
                    return false;
                }
                if (typeof json.image !== 'undefined') {
                    displayImage(json.image);
                }
                if (typeof json.sound !== 'undefined') {
                    stopSound();
                    playSound(json.sound);
                }

            }).fail(function (xhr, status, errorThrown) {
                alert('An Error occoured (sad face).');
                clearTimeout(intervalID);
            });
            intervalID = setTimeout(theLoop, 100);
        }else{
            displayImage(test_case_1[line]);
            $(".preload").css('background-image', "url('images/" + test_case_1[line + 1] + "')");
            line++;
            intervalID = setTimeout(theLoop, 2000);
        }
    };

        console.log( "Neurofeedback Loop Ready!" );
        theLoop();
});

var test_case_1 = ['Epic - Calm/Calm/0000001.jpg',
    'Epic - Calm/Calm/0000002.jpg',
    'Epic - Calm/Calm/0000003.jpg',
    'Nature - Urban/Nature/0000004.jpg',
    'Nature - Urban/Nature/0000016.jpg',
    'Epic - Calm/Epic/0000063.jpg',
    'Epic - Calm/Epic/0000091.jpg',
    'Epic - Calm/Epic/0000043.jpg',
    'Epic - Calm/Epic/0000102.jpg',
    'Epic - Calm/Epic/0000098.jpg',
    'Light - Dark/Dark/0000019.jpg',
    'Light - Dark/Dark/0000062.jpg',
    'Light - Dark/Dark/0000077.jpg',
    'Light - Dark/Dark/0000069.jpg',
    'Light - Dark/Dark/0000045.png',
    'Nature - Urban/Nature/0000005.jpg',
    'Nature - Urban/Nature/0000022.jpg',
    'Nature - Urban/Nature/0000027.jpg',
    'Nature - Urban/Nature/0000029.jpg',
    'Nature - Urban/Nature/0000015.jpg',
    'Nature - Urban/Urban/0000004.jpg',
    'Nature - Urban/Urban/0000011.jpg',
    'Nature - Urban/Urban/0000002.jpg',
    'Nature - Urban/Urban/0000001.jpg',
    'Nature - Urban/Urban/0000006.jpg',
    'Winter/0000022.jpg',
    'Winter/0000065.jpg',
    'Winter/0000107.jpg',
    'Winter/0000102.jpg',
    'Winter/0000099.jpg',
    'Horror/0000008.jpg',
    'Horror/0000006.jpg',
    'Horror/0000012.jpg',
    'Horror/0000003.jpg',
    'Horror/0000016.jpeg',
    'Melancholy/0000007.jpg',
    'Melancholy/0000038.jpg',
    'Melancholy/0000035.jpg',
    'Melancholy/0000030.jpg',
    'Melancholy/0000029.jpg',
    'Natural art - Modern art/Modern art/0000001.jpg',
    'Natural art - Modern art/Modern art/0000002.jpg',
    'Natural art - Modern art/Modern art/0000003.jpg',
    'Natural art - Modern art/Modern art/0000004.jpg',
    'Natural art - Modern art/Modern art/0000005.jpg',
    'Vivid/0000050.png',
    'Vivid/0000073.jpg',
    'Vivid/0000072.jpg',
    'Vivid/0000086.jpg',
    'Vivid/0000123.jpg',
    'Epic - Calm/Epic/0000093.jpg',
    'Epic - Calm/Epic/0000094.jpg',
    'Epic - Calm/Epic/0000026.png',
    'Epic - Calm/Epic/0000001.jpg',
    'Epic - Calm/Epic/0000083.jpg',
    'Light - Dark/Dark/0000064.jpg',
    'Light - Dark/Dark/0000065.jpg',
    'Light - Dark/Dark/0000058.jpg',
    'Light - Dark/Dark/0000023.jpg',
    'Light - Dark/Dark/0000010.png'];