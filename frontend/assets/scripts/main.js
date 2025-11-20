"use strict";

const map = L.map('map').setView([60.867883, 26.704160], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const dialog = document.querySelector("dialog#game-select-modal");

const appState = {
    gameId: null,
    gameList: []
}

/* 
TODO:
- check local storage for game id
- if it exists in local storage, check on backend side
 */

if(!appState.gameId) {
    /* 
        TODO:
        - fetch appState.gameList
    */
    dialog.showModal();
}

/* 
TODO:
- fetch game data and add it into state
 */
