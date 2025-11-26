"use strict";

// Map initialization

const map = L.map('map').setView([60.867883, 26.704160], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// State

const appState = {
    backendBaseUrl: "http://127.0.0.1:3000",
    gameId: null,
    gameList: [],
};

const elements = {
    gameSelect: {
        dialog: document.querySelector("dialog#game-select-modal"),
        gameListContainer: document.querySelector("#game-list"),
        gameSelected: null,
        continueGameBtn: document.querySelector("#continue-game"),
        createNewBtn: document.querySelector("#create-new"),
    },
    gameCreate: {
        dialog: document.querySelector("dialog#game-create-modal"),
        form: document.querySelector("form#game-create-form"),
        backBtn: document.querySelector("#back-to-game-select"),
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

async function main() {
    if(!appState.gameId) {
        await showGameSelect();
    }
}

async function showGameSelect() {
    // set appState.gameList
    await fetch(`${appState.backendBaseUrl}/games`).then(async (req) => {
        appState.gameList = await req.json();
    });

    // display games in modal
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
        const date = new Date(game.created_at);
        const displayDate = `${date.toLocaleDateString("fi-fi")} ${date.toLocaleTimeString("fi-fi", { hour: "2-digit", minute: "2-digit" })}`;
        newButton.addEventListener("change", selectGame);
        newButton.append(buttonInput);
        newButton.innerHTML += `<h3>${game.name}</h3><span>${displayDate}</span>`;
        elements.gameSelect.gameListContainer.append(newButton);
    }

    // show modal (dialog)
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

// Event listener functions

function switchToGameCreate() {
    console.log("hi");
    elements.gameSelect.dialog.close();
    elements.gameCreate.dialog.showModal();
}

function switchToGameSelect() {
    elements.gameCreate.dialog.close();
    elements.gameSelect.dialog.showModal();
}

async function gameCreateSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formObject = Object.fromEntries(formData.entries());
    const players = Array.from(e.target.querySelectorAll("input[name=players]")).map(input => input.value);
    const finalFormObject = {
        players: players,
        config: {
            name: formObject.name,
            max_round: formObject.max_round,
            modifier: formObject.modifier,
            starting_distance: formObject.starting_distance,
            starting_balance: formObject.starting_balance,
            starting_location: formObject.starting_location,
        }
    }

    await fetch(`${appState.backendBaseUrl}/games`, {
        method: "POST",
        body: JSON.stringify(finalFormObject),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }).then(async (req) => {
        appState.gameList = await req.json();
    });
}

// Event listeners
elements.gameSelect.continueGameBtn.addEventListener("click", openGame);
elements.gameSelect.createNewBtn.addEventListener("click", switchToGameCreate);
elements.gameCreate.backBtn.addEventListener("click", switchToGameSelect);
elements.gameCreate.form.addEventListener("submit", gameCreateSubmit);

main();
