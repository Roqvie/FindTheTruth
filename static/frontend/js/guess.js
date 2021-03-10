function get_photos(type, h, w) {

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
    .then((data) => _display_photos(data, type))
}


function _is_real(photo_id, card) {
    let API_ENDPOINT = `api/isReal/${photo_id}`;
    let response = fetch(API_ENDPOINT, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) {
            return response.json();
    }).then(function(json) {
            is_real = json.is_real;
            back_side = card.querySelector(".card__face--back")
            back_side.classList.remove('bg-success');
            back_side.classList.remove('bg-danger');

            if (is_real === true) {
                back_side.classList.toggle('bg-success');
                back_side.innerHTML = '<p class="text-center card-text fs-2 text-light font-weight-bold">Right!</p>';
            } else if (is_real === false) {
                back_side.classList.toggle('bg-danger');
                back_side.innerHTML = '<p class="text-center card-text fs-2 text-light font-weight-bold">Nope!</p>';
            }
            setTimeout(() => { card.classList.toggle('is-flipped'); }, 200);

    });
}


function _display_answer(photo_id) {
    card = document.querySelector('[data-id=\"' + photo_id + '\"]');
    back_side = card.querySelector(".card__face--back")
    _is_real(photo_id, card);
    setTimeout(() => { card.removeEventListener('click', display); }, 200);
    setTimeout(() => { card.classList.remove('is-flipped'); }, 1000);
}


function display() {
    photo_id = this.getAttribute("data-id")
    _display_answer(photo_id);
    setTimeout(() => { get_choices(); }, 2000);

}


function _display_photos(photos, type) {
    preview = document.getElementById("choices");
    cards = preview.querySelectorAll(".flip-card");
    images = preview.querySelectorAll(`.image-${type}`);

    for (let i = 0; i<images.length; i++) {
        back_side = cards[i].querySelector(".card__face--back")
        back_side.classList.remove('bg-success');
        back_side.classList.remove('bg-danger');
        back_side.innerHTML = '<div class="spinner spinner-grow text-secondary" role="status"><span class="visually-hidden">Loading...</span></div>'
        cards[i].classList.toggle("is-flipped")

        images[i].src = photos[i].photo_url;
        cards[i].setAttribute('data-id', photos[i].id);

        setTimeout(() => { cards[i].classList.remove('is-flipped'); }, 1500);
    }
    for (let i = 0; i<images.length; i++) {
        cards[i].addEventListener('click', display);
    }
}


function get_choices() {
    if(window.location.pathname == '/person' || window.location.pathname == '/person/') {
        get_photos('PS',2,2);
    }
    if(window.location.pathname == '/cat' || window.location.pathname == '/cat/') {
        get_photos('CA',2,2);
    }
}


window.onload = get_choices();