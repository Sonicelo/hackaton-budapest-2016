// Shorthand for $( document ).ready()
$(function () {
    var ipAddress = window.location.origin;
    var line = 0;
    var sound, intervalID, counter, oldImageID;

    var displayImage = function (imageID) {
        $(".image").css('background-image', "url('images/" + imageID + "')");
        oldImageID = imageID;

        $.ajax({
            url: ipAddress + '/markpoint',
            data: {},
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

    // Preload all the images (response slow)
    $.ajax({
        url: ipAddress + '/all_images',
        type: 'GET',
    }).done(function (resp) {
        function preload(images, index) {
            index = index || 0;
            if (images && index < images.length) {
                var img = new Image();
                img.src = 'images/' + resp.images[index];
                img.onload = function () {
                    preload(images, index + 1);
                }
            } else {
              $(".loading").css("display", "none");
            }
        }

        preload(resp.images);
    }).fail(function(resp) {
      console.log("all image loading failed");
    });

    var data = {
        url: ipAddress + '/data.json',
        type: "GET"
    };
    var theLoop = function () {
        $.ajax(data).done(function (json) {
            if (typeof json.done !== 'undefined') {
                $('.image').css('background-image', '');
                $('#start').prop('disabled', false);
                $('#stop').prop('disabled', true);
                clearTimeout(intervalID);
                return false;
            }
            if (typeof json.image !== 'undefined') {
                if(json.image != oldImageID) {
                    displayImage(json.image);
                }
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
    };


    $('#focus').click(function () {
        $('.background').removeClass('relax-gradient').addClass('focus-gradient');
    });

    $('#relax').click(function () {
        $('.background').addClass('relax-gradient').removeClass('focus-gradient');
    });

    $('#start').click(function () {
        intervalID = setTimeout(theLoop, 4000);
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
