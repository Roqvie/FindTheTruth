function get_preview(type, h, w) {

    if(w>4 || h>4) {
        throw Error("Size must be under 4x4");
    }

    let API_ENDPOINT = `api/getPhotos/${type}/${w}x${h}`;
    let response = fetch(API_ENDPOINT, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then( data => data.json())
    .then( data => _display_preview_photos(data, type))
}


function _display_preview_photos(photos, type) {
    preview = document.getElementById(`preview-${type}`);
    images = preview.querySelectorAll(`.preview-image-${type}`);
    for (let i = 0; i<images.length; i++) {
        images[i].src = photos[i].photo_url;
    }
}

function display_previews() {
    get_preview('PS',2,2);
    get_preview('CA',2,2);
}

window.onload = display_previews();