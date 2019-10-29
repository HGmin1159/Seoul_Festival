let festivals;

let menu = document.querySelector("#menu");
let div = document.querySelector("#list");
let tab = document.querySelector("#tag-tab");
let tagList = document.querySelector("#tag-list");
let search = document.querySelector("input");

let info = document.querySelector("#info");
let back = document.querySelector("#revert");
let mapContainer = document.querySelector("#map"); // 지도를 표시할 div 

let map;
// 마커를 클릭하면 장소명을 표출할 인포윈도우 입니다
var infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();

// SEARCH GOES HERE
function searchHandler(e) {
    setTimeout(() => {
        let word = e.target.value;
        console.log(div)
        // let filtered = festivals.filter(obj => obj["축제명"].indexOf(word) == -1);
        for (let i = 0; i < festivals.length; i++) {
            if (div.children[i].textContent.indexOf(word) == -1) {
                div.children[i].style.display = "none";
            } else {
                div.children[i].style.display = "";
            }
        }
    }, 250)
}


function show(festivals) {
    for (let festival of Array.from(festivals)) {
        let p = document.createElement("p");
        p.textContent = festival["축제명"];
        p.style.cursor = "pointer";
        p.addEventListener("click", showInfo);
        div.appendChild(p);
    }
}

function makeTagList(festivals) {
    let total = document.createElement("button");
    total.textContent = "전체보기";
    total.addEventListener("click", showAll);
    tagList.appendChild(total);
    for (let tag of Object.keys(festivals[0]).slice(1)) {
        let b = document.createElement("button");
        b.textContent = tag;
        b.addEventListener("click", showSorted);
        tagList.appendChild(b);
    }
}

function showTab(e) {
    for (let i = 0; i < festivals.length; i++) {
        div.children[i].style.display = "none";
    }
    tagList.style.display = "";
}

function showSorted(e) {
    tagList.style.display = "none";
    for (let i = 0; i < festivals.length; i++) {
        if (festivals[i][e.target.textContent] == '1') {
            div.children[i].style.display = "";
        }
    }
}

function showAll(e) {
    tagList.style.display = "none";
    for (let i = 0; i < festivals.length; i++) {
        div.children[i].style.display = "";
    }
}

function showInfo(e) {
    toggleUI();
    showMap(e.target.textContent);
}

function showMap(keyword) {
    // 키워드로 장소를 검색합니다
    ps.keywordSearch(keyword, placesSearchCB); // async
}

// 키워드 검색 완료 시 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        var bounds = new kakao.maps.LatLngBounds();

        map = drawMap(data[0].y, data[0].x);

        for (var i = 0; i < data.length; i++) {
            displayMarker(data[i]);
            bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
        }

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
        map.setBounds(bounds);
        console.log(status, data);
    } else {
        console.log(status, data);
    }
}

// 지도에 마커를 표시하는 함수입니다
function displayMarker(place) {

    // 마커를 생성하고 지도에 표시합니다
    var marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(place.y, place.x)
    });

    // 마커에 클릭이벤트를 등록합니다
    kakao.maps.event.addListener(marker, 'click', function () {
        // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
        infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
        infowindow.open(map, marker);
    });
}

function drawMap(lat, long) {
    var options = { //지도를 생성할 때 필요한 기본 옵션
        center: new kakao.maps.LatLng(lat, long), //지도의 중심좌표.
        level: 3 //지도의 레벨(확대, 축소 정도)
    };

    return new kakao.maps.Map(mapContainer, options); //지도 생성 및 객체 리턴    
}

function showMenu(e) {
    toggleUI();
    infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    map = Object.create(null);
    ps = new kakao.maps.services.Places();
}

function toggleUI() {
    let t = menu.style.display;
    menu.style.display = info.style.display;
    info.style.display = t;
}

back.addEventListener("click", showMenu);
tab.addEventListener("click", showTab);


fetch("./festag162.json")
    .then(rsp => rsp.json()).then(data => {
        festivals = data;
        // show(data);
        // makeTagList(data);
        console.log(Object.keys(data[0]).length);
    }).then(() => {

        fetch("./festag19.json")
            .then(rsp => rsp.json()).then(data => {
                festivals = festivals.concat(data);
                show(festivals);
                makeTagList(festivals);
                console.log(Object.keys(festivals[0]).length);
            });
    }).then(() => {
        search.addEventListener("input", searchHandler);
    })