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
        playerInputs: document.querySelector("#player-inputs"),
        addPlayerInputBtn: document.querySelector("#add-player-input"),
        backBtn: document.querySelector("#back-to-game-select"),
    }
};

/* 
TODO:
- check local storage for game id
- if it exists in local storage, check on backend side
 */

async function main() {
    // Show game select modal if no gameId
    if(!appState.gameId) {
        await showGameSelect();
    }
    
    // Add two player inputs as default
    addPlayerInput();
    addPlayerInput();
}

function selectGame(e) {
    const gameId = e.target.value;
    elements.gameSelect.continueGameBtn.removeAttribute("disabled");
    elements.gameSelect.gameSelected = gameId;
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

function openGame(gameId) {
    /* 
        TODO:
        - send a request to create a game on server
        - set new game state
    */
    appState.gameId = Number(gameId);
    elements.gameSelect.dialog.close();
    elements.gameCreate.dialog.close();
}

// Event listener functions
// May be used outside of listener functions as well

function switchToGameCreate() {
    elements.gameSelect.dialog.close();
    elements.gameCreate.dialog.showModal();
}

function switchToGameSelect() {
    elements.gameCreate.dialog.close();
    elements.gameSelect.dialog.showModal();
}

function removePlayerInput(e) {
    const num = e.target.dataset.index; // index from data-index attribute
    elements.gameCreate.playerInputs.children[num - 1].remove();

    // update all attributes containing index for each player input wrap
    for(const elementIndex in Array.from(elements.gameCreate.playerInputs.children)) {
        const newIndex = Number(elementIndex) + 1; // array length + 1 (beacuse starting from 0)

        // element, attributes of which we will change
        const element = elements.gameCreate.playerInputs.children[elementIndex];
        element.dataset.index = newIndex;
        const label = element.querySelector(`label`);
        label.setAttribute("for", `player-${newIndex}`);
        label.innerHTML = `Player ${newIndex}:`;
        const input = element.querySelector("input");
        input.setAttribute("id", `player-${newIndex}`);
        const button = element.querySelector("button");
        button.dataset.index = newIndex;
    }
}

function addPlayerInput() {
    const currentIndex = elements.gameCreate.playerInputs.children.length; // current number of inputs for player names
    const newIndex = currentIndex + 1; // added number of inputs for player names
    
    // Create the elements, representing player name input with remove button and a label, wrapped in a couple of divs
    const newWrap = createElement("div", { class: "input-wrap", "data-index": newIndex });
    const newLabel = createElement("label", { for: `player-${newIndex}` });
    newLabel.innerHTML = `Player ${newIndex}:`;

    const newInputWithButtonWrap = createElement("div", { class: "input-with-button-wrap" });
    const newInput = createElement("input", {
        type: "text",
        name: "players",
        id: `player-${newIndex}`,
        placeholder: "Matti",
        required: "true",
    });
    const newButton = createElement("button", {
        type: "button",
        class: "material-icons",
        "data-index": newIndex,
    });
    newButton.innerHTML = "close"; // Material icon name

    // event listener for remove button
    newButton.addEventListener("click", removePlayerInput);

    newInputWithButtonWrap.appendChild(newInput);
    newInputWithButtonWrap.appendChild(newButton);

    newWrap.appendChild(newLabel);
    newWrap.appendChild(newInputWithButtonWrap);

    elements.gameCreate.playerInputs.append(newWrap);
}

async function gameCreateSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formObject = Object.fromEntries(formData.entries());

    // Convert inputs into array of player entered names
    const players = Array.from(e.target.querySelectorAll("input[name=players]")).map(input => input.value);

    // Convert data into endpoint's required format
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
        const res = await req.json();
        // get id of the last element in the games list from the response
        const gameId = res.games.at(-1).id;
        openGame(gameId);
    });
}

// Event listeners
elements.gameSelect.continueGameBtn.addEventListener("click", () => openGame(elements.gameSelect.gameSelected));
elements.gameSelect.createNewBtn.addEventListener("click", switchToGameCreate);
elements.gameCreate.addPlayerInputBtn.addEventListener("click", addPlayerInput);
elements.gameCreate.backBtn.addEventListener("click", switchToGameSelect);
elements.gameCreate.form.addEventListener("submit", gameCreateSubmit);

main();
