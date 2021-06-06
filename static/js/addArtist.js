function uploadSongCover() {
    document.querySelector('#songImg').click();
}

function displayImg(e) {
    if(e.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            // console.log(e.lengthComputable)
            document.querySelector('#songImgDisplay').setAttribute('src', e.target.result);
        }
        reader.readAsDataURL(e.files[0]);
    }
}