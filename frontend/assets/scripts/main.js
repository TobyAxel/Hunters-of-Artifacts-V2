"use strict";

// Map initialization

const map = L.map('map').setView([60.867883, 26.704160], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// State

const appState = {
    gameId: null,
    gameList: [
        {
            id: 0,
            name: "Example game 0",
            created_at: 1763677334,
        },
        {
            id: 1,
            name: "Example game 1",
            created_at: 1763675221,
        },
    ]
};

const elements = {
    gameSelect: {
        dialog: document.querySelector("dialog#game-select-modal"),
        gameListContainer: document.querySelector("#game-list"),
        gameSelected: null,
        continueGameBtn: document.querySelector("#continue-game"),
        createNewBtn: document.querySelector("#create-new"),
    }
};

/* 
TODO:
- check local storage for game id
- if it exists in local storage, check on backend side
 */

function selectGame(e) {
    const gameId = e.target.value;
    elements.gameSelect.continueGameBtn.removeAttribute("disabled");
    elements.gameSelect.gameSelected = gameId;
}

if(!appState.gameId) {
    /* 
        TODO:
        - fetch appState.gameList from server
    */
    for(const n in appState.gameList) {
        const game = appState.gameList[n];
        const newButton = createElement("label", {
            "type": "radio",
            "name": "game-select",
            "value": `${game.id}`,
            "class": "radio-button-label",
        });
        const buttonInput = createElement("input", {
            "type": "radio",
            "name": "game-select",
            "value": `${game.id}`,
            "class": "radio-button",
        });
        newButton.addEventListener("change", selectGame);
        newButton.append(buttonInput);
        newButton.innerHTML += `<h3>${game.name}</h3><span>Date time</span>`;
        elements.gameSelect.gameListContainer.append(newButton);
    }
    elements.gameSelect.dialog.showModal();
}

/* 
TODO:
- fetch game data and add it into state
 */

function openGame() {
    /* 
        TODO:
        - send a request to create a game on server
        - set new game state
    */
    appState.gameId = elements.gameSelect.gameSelected;
    elements.gameSelect.dialog.close();
}

elements.gameSelect.continueGameBtn.addEventListener("click", openGame);
