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
        gameOptionButtons: [], // TODO: instead of buttons, consider using radio
        selectedGameOption: null,
        continueGameBtn: document.querySelector("#continue-game"),
        createNewBtn: document.querySelector("#create-new"),
    }
};

/* 
TODO:
- check local storage for game id
- if it exists in local storage, check on backend side
 */

if(!appState.gameId) {
    /* 
        TODO:
        - fetch appState.gameList from server
    */
    for(const n in appState.gameList) {
        const gameOption = appState.gameList[n];
        const newGameOptionButton = createElement("button", {
           "class": "primary-button", 
        });
        newGameOptionButton.innerHTML = `<h3>${gameOption.name}</h3><span>Date time</span>`;
        elements.gameSelect.gameOptionButtons.push(newGameOptionButton);
        newGameOptionButton.addEventListener("click", () => selectGame(n));
    }
    for(const n in elements.gameSelect.gameOptionButtons) {
        const button = elements.gameSelect.gameOptionButtons[n];
        elements.gameSelect.gameListContainer.append(button);
    }
    elements.gameSelect.dialog.showModal();
}

/* 
TODO:
- fetch game data and add it into state
 */

function selectGame(gameOption) {
    /* 
        TODO:
        - change color of selected game option button
    */
   elements.gameSelect.selectedGameOption = gameOption;
   elements.gameSelect.dialog.close();
}

function createGame() {
    /* 
        TODO:
        - send a request to create a game on server
        - set new game state
    */
}
