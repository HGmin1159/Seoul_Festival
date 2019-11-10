let festivals, restaurants;

let menu = document.querySelector("#menu");
let div = document.querySelector("#list");

let search = document.querySelector("input");

let info = document.querySelector("#info");
let back = document.querySelector("#revert");
let name = document.querySelector("h1");
let mapContainer = document.querySelector("#map"); // 지도를 표시할 div 
let container = document.querySelector(".container");
let resList = document.querySelector("ul");

// leaflet map, marker
let map, marker, popup;
let circle = null;
const resIcon = L.icon({
    iconUrl: 'icon.png',
    iconSize: [20, 30], // size of the icon
});

let label = document.querySelector("label");
let distInput = document.querySelector("#dist");
distInput.addEventListener("input", distSearch);

// DIST SEARCH
function distSearch(e) {
    let searchDist = e.target.value;
    setTimeout(() => {
        for (let res of restaurants) {
            res.update(searchDist);
        }
    }, 100)

    if (circle !== null) map.removeLayer(circle);
    circle = L.circle([marker._latlng.lat, marker._latlng.lng], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.1,
        radius: searchDist
    }).addTo(map)
}
// END DIST SEARCH

// SEARCH
function searchHandler(e) {
    setTimeout(() => {
        let word = e.target.value;
        for (let i = 0; i < festivals.length; i++) {
            if (div.children[i].textContent.indexOf(word) == -1) {
                div.children[i].style.display = "none";
            } else {
                div.children[i].style.display = "";
            }
        }
    }, 250)
}
// END SEARCH

class Festival {
    constructor([id, name, x, y]) {
        this.id = id;
        this.name = name;
        this.x = x;
        this.y = y;
    }

    render(parent) {
        let p = document.createElement("p");
        p.textContent = this.name;
        p.id = this.id;
        p.style.cursor = "pointer";
        if (this.x === null) p.style.textDecoration = "line-through";
        p.addEventListener("click", showInfo.bind(this));
        parent.appendChild(p);
    }
}

class Restaurant {
    constructor({ id, place_name, category_name, place_url, x, y, distance }) {
        this.id = id;
        this.place_name = place_name;
        this.category_name = category_name.slice(category_name.indexOf('>')+2);
        this.place_url = place_url;
        this.x = x;
        this.y = y;
        this.distance = distance;
        this.li = document.createElement("li");
        this.marker = null;
    }

    update(searchDist) {
        if (this.distance > searchDist) {
            if (this.marker !== null) {
                map.removeLayer(this.marker);
                this.marker = null;
            }
            this.li.style.display = "none";
        }
        else {
            this.li.style.display = "";
            if (this.marker === null) {
                this.marker = L.marker([this.y, this.x], { icon: resIcon }).bindPopup(
                    `${this.place_name}\n<a href=${this.place_url}>${this.place_url}</a>`
                )
                    .addTo(map);
            }
        }
    }

    render(parent) {
        this.li.innerHTML = `${this.place_name}<br>${this.category_name}
        <br><a href=${this.place_url}>${this.place_url}</a>`;
        this.li.addEventListener("mouseenter", () => {
            this.marker.openPopup();
        });
        parent.appendChild(this.li);
        this.marker = L.marker([this.y, this.x], { icon: resIcon }).bindPopup(
            `${this.place_name}\n<a href=${this.place_url}>${this.place_url}</a>`
        )
            .addTo(map);
    }

    remove() {
        this.li.remove();
    }
}

function show(things, parent) {
    for (let thing of things) {
        thing.render(parent);
    }
}

function showInfo(e) {
    toggleUI();
    name.textContent = e.target.textContent;
    if (this.x !== null) drawMap(this.y, this.x, this.name);
    else mapContainer.textContent = "No coord";
    fetch(`/restaurants/${e.target.id}`)
        .then(rsp => rsp.json()).then(data => {
            restaurants = data.map(d => new Restaurant(d));
            show(restaurants, resList);
        })
}

function drawMap(lat, lng, name) {
    map = L.map('map').setView([lat, lng], 15);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiZG9sbGh5IiwiYSI6ImNrMnNraHRraDBpeGUzbXRqcm9hMTIxNnMifQ.s5z_Pkw604EFu087friCtQ'
    }).addTo(map);

    marker = L.marker([lat, lng]).bindPopup(name)
        .addTo(map).openPopup();
}

function showMenu(e) {
    toggleUI();
    map = null;
    mapContainerOld = mapContainer;
    mapContainer = document.createElement("div");
    mapContainer.id = "map";
    container.insertBefore(mapContainer, null);
    mapContainerOld.remove();

    for (let res of restaurants) {
        res.remove();
        res = null;
    }
}

function toggleUI() {
    let t = menu.style.display;
    menu.style.display = info.style.display;
    info.style.display = t;
}

back.addEventListener("click", showMenu);


fetch("/festival")
    .then(rsp => rsp.json()).then(data => {
        festivals = data.map(d => new Festival(d));
        show(festivals, div);
    }).then(() => {
        search.addEventListener("input", searchHandler);
    })
