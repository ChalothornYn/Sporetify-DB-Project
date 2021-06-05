var previous = document.getElementById('pre');
var play = document.getElementById('play');
var next = document.getElementById('next');
var title = document.getElementById('title');
var recent_volume = document.getElementById('volume');
var volume_show = document.getElementById('volume_show');
var slider = document.getElementById('duration_slider');
var show_duration = document.getElementById('show_duration');
var track_image = document.getElementById('songimg');
var auto_play = document.getElementById('auto');
var artist = document.getElementById('artist');


var timer;
var autoplay = 0;

var index_no = 0;
var Playing_song = false;

//create a audio Element
var track = document.createElement('audio');


//All songs list
All_song = [{
        name: "FRIENDS",
        path: "http://127.0.0.1:8000/media/uploads/songQuality/normal/FRIENDS.mp3",
        img: "http://127.0.0.1:8000/media/uploads/songImg/friendssong.jpg",
        singer: "lilboi, Wonstein"
    },
    {
        name: "Daydream",
        path: "http://127.0.0.1:8000/media/uploads/songQuality/normal/Daydream.mp3",
        img: "http://127.0.0.1:8000/media/uploads/songImg/daydream.jpg",
        singer: "B.i ft. LeeHi"
    },
    {
        name: "DRIVE",
        path: "http://127.0.0.1:8000/media/uploads/songQuality/normal/DRIVE.mp3",
        img: "http://127.0.0.1:8000/media/uploads/songImg/drive.jpg",
        singer: "Jay park ft. GRAY"
    },
    {
        name: "Late Night",
        path: "http://127.0.0.1:8000/media/uploads/songQuality/normal/LateNight.mp3",
        img: "http://127.0.0.1:8000/media/uploads/songImg/latenight.jpg",
        singer: "GRAY & Loco"
    },
    {
        name: "FLYING HIGH WITH U",
        path: "http://127.0.0.1:8000/media/uploads/songQuality/normal/VINXEN.mp3",
        img: "http://127.0.0.1:8000/media/uploads/songImg/vinxen.jpg",
        singer: "VINXEN"
    }
];

function load_track(index_no) {
    clearInterval(timer);
    reset_slider();

    track.src = All_song[index_no].path;
    title.innerHTML = All_song[index_no].name;
    track_image.src = All_song[index_no].img;
    artist.innerHTML = All_song[index_no].singer;
    track.load();

    timer = setInterval(range_slider, 1000);
    total = All_song.length;
    present = index_no + 1;
}

load_track(index_no);

// checking.. the song is playing or not
function justplay() {
    if (Playing_song == false) {
        playsong();

    } else {
        pausesong();
    }
}

//reset song slider
function reset_slider() {
    slider.value = 0;
}

// play song
function playsong() {
    track.play();
    Playing_song = true;
    play.innerHTML = '<i class="fa fa-pause" aria-hidden="true"></i>';
}

//pause song
function pausesong() {
    track.pause();
    Playing_song = false;
    play.innerHTML = '<i class="fa fa-play" aria-hidden="true"></i>';
}

// next song

function next_song() {
    if (index_no < All_song.length - 1) {
        index_no += 1;
        load_track(index_no);
        playsong();
    } else {
        index_no = 0;
        load_track(index_no);
        playsong();

    }
}


// previous song
function previous_song() {
    if (index_no > 0) {
        index_no -= 1;
        load_track(index_no);
        playsong();

    } else {
        index_no = All_song.length;
        load_track(index_no);
        playsong();
    }
}

// autoplay function
function autoplay_switch() {
    if (autoplay == 1) {
        autoplay = 0;
        auto_play.style.background = "rgba(189, 189, 189, 0.192)";
    } else {
        autoplay = 1;
        auto_play.style.background = "#1FD662";
    }
}


// change slider position 
function change_duration() {
    slider_position = track.duration * (slider.value / 100);
    track.currentTime = slider_position;
}


function range_slider() {
    let position = 0;

    // update slider position
    if (!isNaN(track.duration)) {
        position = track.currentTime * (100 / track.duration);
        slider.value = position;
    }


    // function will run when the song is over
    if (track.ended) {
        play.innerHTML = '<i class="fa fa-play" aria-hidden="true"></i>';
        if (autoplay == 1) {
            index_no += 1;
            load_track(index_no);
            playsong();
        }
    }
}