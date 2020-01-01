import React, { useState, useEffect } from 'react';
import L from 'leaflet';
import mun from '../seoul_municipalities_geo_simple.json';
import queryStringify from '../lib/queryStringify.js';
import ReactDOMServer from "react-dom/server";
import Link from "next/link";

const getLink = (festival) => {
    return (
        <>
            {festival.name} < br />
            <Link href="/p/[id]" as={`/p/${
                queryStringify(festival)
                }`}>
                <a>
                    <picture>
                        <source type="image/webp" srcSet={require(`../public/img/${festival.id}.jpg?webp`)} />
                        <img src={require(`../public/img/${festival.id}.jpg`)} />
                    </picture>
                </a>
            </Link>
        </>
    )
}

let map, markerLayer, marker, layer;

function isInside(marker, poly) {
    // console.log(poly[0])
    const polyPoints = poly[0];    
    const x = marker.y, y = marker.x;

    let inside = false;
    for (let i = 0, j = polyPoints.length - 1; i < polyPoints.length; j = i++) {
        let xi = polyPoints[i][1], yi = polyPoints[i][0];
        let xj = polyPoints[j][1], yj = polyPoints[j][0];

        let intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
};

let restaurantMarkers = {};

const LeafMap = ({ fes, res, full, invalidate, preventSwipe, open, height}) => {
    const [init, setInit] = useState(true);

    const Icon = L.icon({
        iconUrl: '/icon.png',
        iconSize: [20, 30]
    });

    let style;
    
    if (full) {
        style = <style jsx>{`
                            #map {
                                height: ${height - 48}px;
                                width: 100vw;
                                z-index: 1;
                            }
                            .mapContainer {
                            }
                            img {
                                width: 40vmin;
                                max-width: 300px;
                            }
                            .leaflet-control-zoom{
                                display: none;
                            }
                        `}</style>;
    } else {
        style = <style jsx>{`
                            #map {
                                width: 100%;
                                height: 100%;
                                min-height: 256px;
                                margin: auto;
                            }
                            .mapContainer {
                                position: sticky;
                                top: 10px;
                            }
                        `}</style>;
    }

    const colorScheme = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928'];
    // const colorScheme = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f'];

    const layers = [];

    const municipalHandler = (feature, layer) => {
        const colorCode = colorScheme[[22,15].includes(feature.properties.ESRI_PK)? 1 : feature.properties.ESRI_PK % colorScheme.length];
        // console.log(layer.getBounds())
        const festLayer = L.layerGroup();

        for (let f of fes) {
            if (isInside(f, feature.geometry.coordinates)) {
                L.marker(
                    [f.y, f.x],
                ).bindPopup(
                    ReactDOMServer.renderToString(getLink(f))
                ).addTo(festLayer);
            }
        }
        layers.push([layer, festLayer]);

        const zoomOutHandler = () => {
            map.fitBounds([
                [37.413294, 126.734086], 
                [37.715133, 127.269311]
            ]);
            map.removeLayer(layer);
            map.removeLayer(festLayer);
            for (let l of layers) {
                map.addLayer(l[0]);
            }

            map.removeEventListener("click", zoomOutHandler);
            layer.addEventListener("click", zoomInHandler);
        };

        const zoomInHandler = () => {
            map.fitBounds(layer.getBounds());
            for (let l of layers) {
                map.removeLayer(l[0]);
                map.removeLayer(l[1]);
            }
            map.addLayer(layer);
            map.addLayer(festLayer);

            layer.removeEventListener("click", zoomInHandler);
            map.addEventListener("click", zoomOutHandler);
        }
        
        layer.addEventListener("click", zoomInHandler);
        
        layer.setStyle({
            color: colorCode,
            fillColor: colorCode,
            fillOpacity: 0.5
        });
    }

    useEffect(()=>{
        if (!full) return;
        if (map) {
            map.remove();
        }
        map = L.map('map').fitBounds([
            [37.413294, 126.734086], 
            [37.715133, 127.269311]
        ]);
        L.geoJSON(mun, {
            onEachFeature: municipalHandler
        }).addTo(map);
        
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    });

    useEffect(() => {
        if (invalidate) {
            // console.log("invalidate");
            if (!init) {
                map.remove();
                restaurantMarkers = {};
            }
            map = L.map('map').setView([fes.y, fes.x], 15);
            marker = L.marker([fes.y, fes.x]).bindPopup(fes.name)
                .addTo(map).openPopup();
            
            for (let r of res) {
                restaurantMarkers[r.id] = L.marker(
                    [r.y, r.x],
                    { icon: Icon }
                ).bindPopup(
                    `${r.place_name}\n<a href=${r.place_url}>${r.place_url}</a>`
                ).addTo(map);
            }
            setInit(false);
            // L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            //     maxZoom: 18,
            //     id: 'mapbox.streets',
            //     accessToken: 'pk.eyJ1IjoiZG9sbGh5IiwiYSI6ImNrMnNraHRraDBpeGUzbXRqcm9hMTIxNnMifQ.s5z_Pkw604EFu087friCtQ'
            // }).addTo(map);
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            layer = L.layerGroup().addTo(map);
        }
    }, [fes, invalidate])

    useEffect(()=>{
        if (open) {
            restaurantMarkers[open].openPopup();
        }
    }, [open])

    return (
        <div className="mapContainer"
            onTouchStart={
                (preventSwipe)
                &&
                (e => {
                    preventSwipe(true);
                    function unregisterSwipe() {
                        preventSwipe(false);
                        window.removeEventListener('touchend', unregisterSwipe);
                    }
                    window.addEventListener('touchend', unregisterSwipe)
                })}
        >
            <div id='map'></div>

            {style}
        </div>
    );
}

export default LeafMap;