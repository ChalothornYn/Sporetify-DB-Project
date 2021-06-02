function uploadProfile() {
    document.querySelector('#profileImg').click();
}

function displayImg(e) {
    if(e.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            // console.log(e.lengthComputable)
            document.querySelector('#profileImgDisplay').setAttribute('src', e.target.result);
        }
        reader.readAsDataURL(e.files[0]);
    }
}