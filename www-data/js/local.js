// Shorthand for $( document ).ready()
$(function () {
    var ipAddress = window.location.origin;
    var line = 0;
    var sound, intervalID, counter, oldImageID, files;
    jQuery.getJSON("http://localhost:49652/budapest-2016/www-data/array.json", function(data){
        files = [];
        $.each( data, function( key, val ) {
            var file = val.replace("\\", "/");
            files.push( file);
        });
    });

    var displayImage = function (imageID) {
        $(".image").css('background-image', "url('images/" + imageID + "')");
        oldImageID = imageID;
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

    var weights = [512, 256, 128, 64, 32, 16, 8,6,4,2, 1, 0];
    var categories = [
        "Vivid - Gloomy/Gloomy",
        "Light - Dark/Dark",
        "Joy - Horror/Horror",
        "Nature - Urban/Urban",
        "Landscape - Not landscape/Not landscape",
        "Landscape - Not landscape/Landscape",
        "Epic - Calm/Epic",
        "Nature - Urban/Nature",
        "Joy - Horror/Joy",
        "Light - Dark/Light",
        "Epic - Calm/Calm"
    ];


    var getWeightedRandomCategory = function(categories, weights){
        var total = 0;
        var ranges = weights.slice(0);
        for(var i = 0, len = weights.length; i < len; i++) {
            ranges[i] = [total, total += ranges[i]];
        }
        var randomNumber = parseInt(Math.random() * total);
        for(;randomNumber < ranges[--i][0];);
        return categories[i];
    };

    var getRandomImage = function(category){

    };
     var index = 0;
    var theLoop = function () {
        if(index >= test_case_1.length){
            index = 0;
        }
        displayImage(test_case_1[index]);

        index ++;
        intervalID = setTimeout(theLoop, 2000);
    };

    function preload(images, index) {
        index = index || 0;
        if (images && index < images.length) {
            var img = new Image();
            img.src = 'images/' + images[index];
            img.onload = function () {
                preload(images, index + 1);
            }
        } else {
            $(".loading").css("display", "none");
        }
    }
    preload(test_case_1, 0);



    $('#start').click(function () {
        intervalID = setTimeout(theLoop, 2000);
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


var test_case_1 = [
    'Vivid - Gloomy/Gloomy/0000017.jpg',
    'Vivid - Gloomy/Gloomy/0000049.png',
    'Vivid - Gloomy/Gloomy/0000061.png',
    'Vivid - Gloomy/Gloomy/0000020.jpg',
    'Vivid - Gloomy/Gloomy/0000011.jpg',
    'Light - Dark/Dark/0000019.jpg',
    'Light - Dark/Dark/0000081.jpg',
    'Light - Dark/Dark/0000077.jpg',
    'Light - Dark/Dark/0000069.jpg',
    'Light - Dark/Dark/0000078.jpg',
    'Joy - Horror/Horror/0000008.jpg',
    'Joy - Horror/Horror/0000005.jpg',
    'Joy - Horror/Horror/0000014.jpg',
    'Joy - Horror/Horror/0000003.jpg',
    'Joy - Horror/Horror/0000016.jpeg',
    'Nature - Urban/Urban/chongqing-urban-jungle-china-3820.jpg',
    'Nature - Urban/Urban/0000011.jpg',
    'Nature - Urban/Urban/0000002.jpg',
    'Nature - Urban/Urban/0000001.jpg',
    'Nature - Urban/Urban/0000007.jpg',
    'Nature - Urban/Nature/0000005.jpg',
    'Nature - Urban/Nature/0000022.jpg',
    'Nature - Urban/Nature/0000029.jpg',
    'Nature - Urban/Nature/0000015.jpg',
    'Epic - Calm/Calm/0000002.jpg',
    'Epic - Calm/Calm/15026842-Young-woman-meditating-outdoors-Stock-Photo-yoga-meditation-nature.jpg',
    'Epic - Calm/Calm/maxresdefault (1).jpg',
    'Epic - Calm/Calm/calm-wallpapers-007.jpg',
    'Epic - Calm/Calm/animals,fox,photography,cute,nature,strech-c30fa02f37560976c3fd8dfcfc87991c_h.jpg',
    'Epic - Calm/Epic/0000063.jpg',
    'Epic - Calm/Epic/0000091.jpg',
    'Epic - Calm/Epic/0000043.jpg',
    'Epic - Calm/Epic/0000101.jpg',
    'Epic - Calm/Epic/0000098.jpg',
    'Joy - Horror/Joy/impossibly-cute-puppy-30.jpg',
    'Joy - Horror/Joy/shutterstock_51111274.jpg',
    'Joy - Horror/Joy/Uber-Puppies.jpg',
    'Joy - Horror/Joy/Red-Panda-7.jpg',
    'Joy - Horror/Joy/impossibly-cute-puppy-8.jpg',
    'Vivid - Gloomy/Vivid/0000123.jpg',
    'Vivid - Gloomy/Vivid/0000073.jpg',
    'Vivid - Gloomy/Vivid/0000072.jpg',
    'Vivid - Gloomy/Vivid/0000086.jpg',
    'Vivid - Gloomy/Vivid/0000123.jpg'
];