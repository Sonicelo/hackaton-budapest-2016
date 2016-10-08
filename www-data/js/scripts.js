// Shorthand for $( document ).ready()
$(function () {
    var ipAddress = "http://192.168.0.101:8080";
    var remote = true;
    var line = 0;
    var sound, intervalID, counter;

    var displayImage = function (imageID) {
        $(".image").css('background-image', "url('images/" + imageID + "')");
        $.ajax({
            url: ipAddress + '/markerpoint',
            data: { },
            type: "GET",
            dataType: "json"
        });
    };


    var stopSound = function () {
        if (typeof sound !== 'undefined') {
            sound.stop();
        }
    };

    var playSound = function (soundTrack) {
        sound = new Howl([soundTrack]);
        sound.start();
    };

    var data = {
        url: ipAddress + '/data.json',
        data: {},
        type: "GET",
        dataType: "json"
    };
    var theLoop = function () {

        if (remote) {
            $.ajax(data).done(function (json) {
                if (typeof json.done !== 'undefined') {
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
        } else {
            displayImage(test_case_1[line]);
            $(".preload").css('background-image', "url('images/" + test_case_1[line + 1] + "')");
            line++;
            intervalID = setTimeout(theLoop, 2000);
        }
    };


    $('#focus').click(function () {
        $('.background').removeClass('relax-gradient').addClass('focus-gradient');
    });

    $('#relax').click(function () {
        $('.background').addClass('relax-gradient').removeClass('focus-gradient');
    });

    $('#start').click(function () {
        setTimeout(theLoop, 4000);
        $(this).prop('disabled', true);
        $('#stop').prop('disabled', false);
    });

    $('#stop').click(function () {
        clearTimeout(intervalID);
        $('.image').css('background-image', '');
        $(this).prop('disabled', true);
        $('#start').prop('disabled', false);
        $.ajax({
            url: ipAddress + '/reset.json',
            data: {},
            type: "GET",
            dataType: "json"
        });
    });

    console.log("Neurofeedback Loop Ready!");
});

