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
    gameInfo: {
        max_round: null,
        current_round: null,
    },
    playerTurn: {
        name: "Some Player",
        money: 500,
        travelled: 0,
        movesLeft: 2,
    }
};

const elements = {
    info: {
        player: document.querySelector("#player-turn-info"),
        moves: document.querySelector("#moves-info"),
        accountBalance: document.querySelector("#account-balance-info"),
        distanceTravelled: document.querySelector("#distance-travelled-info"),
        currentRoundNumber: document.querySelector("#current-round-number"),
        currentRoundList: document.querySelector("#current-round-list")
    },
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
    },
    moveSwitch: {
        dialog: document.querySelector("#move-switch-modal"),
        name: document.querySelector("#switch-modal-name"),
        startMoveBtn: document.querySelector("#start-move")
    },
    screens: {
        explore: document.querySelector("#explore"),
        map: document.querySelector("#map"),
        items: document.querySelector("#items"),
        shop: document.querySelector("#shop"),
    },
    shop: {
        commonItemsContainer: document.querySelector("#common-shelf"),
        rareItemsContainer: document.querySelector("#rare-shelf"),
        epicItemsContainer: document.querySelector("#epic-shelf"),
        legendaryItemsContainer: document.querySelector("#legendary-shelf"),
    },
    actionButtons: {
        exploreBtn: document.querySelector("#explore-action"),
        travelBtn: document.querySelector("#travel-action"),
        itemBtn: document.querySelector("#item-action"),
        shopBtn: document.querySelector("#shop-action"),
        endturnBtn: document.querySelector("#end-turn-action"),
        quitBtn: document.querySelector("#quit-action"),
    }
};

async function main() {
    // Initially insert elements
    // Add two player inputs by default to the game create form
    addPlayerInput();
    addPlayerInput();

    // See if game id exists in localStorage
    const gameId = Number(window.localStorage.getItem("game_id"));
    
    // If game doesn't exist, open modal for game selection/creation
    if(!gameId) {
        await showGameSelect();
        return; // Abrupts this function's execution
    }

    await openGame(gameId);
}

function selectGameInList(e) {
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
    elements.gameSelect.gameListContainer.innerHTML = ""; // clear previous list
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
        newButton.addEventListener("change", selectGameInList);
        newButton.append(buttonInput);
        newButton.innerHTML += `<h3>${game.name}</h3><span>${displayDate}</span>`;
        elements.gameSelect.gameListContainer.append(newButton);
    }

    // show modal (dialog)
    elements.gameSelect.dialog.showModal();
}

async function openGame(gameId) {
    appState.gameId = Number(gameId);
    elements.gameSelect.dialog.close();
    elements.gameCreate.dialog.close();
    window.localStorage.setItem("game_id", gameId);    
    await switchMove(true);
}

async function switchMove(initial) {
    // Only on game open
    if(!initial) {
        await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/end-turn`, { method: "POST" }).then(async (req) => {
            const res = await req.json();
            console.log(res);
        });
    }
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}`).then(async (req) => {
        const res = await req.json();
        // Save data to app state
        appState.playerTurn.name = res[0].player_turn;
        appState.gameInfo.max_round = res[0].max_round;
        appState.gameInfo.current_round = res[0].round;
        appState.playerTurn.movesLeft = res[0].moves;
    });
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/players`).then(async (req) => {
        const res = await req.json();
        // Save data to app state
        for (let i = 0; i < res.length; i++) {
            res[i].screen_name
        }
    });
    // Display data from app state in the elements
    elements.info.player.innerHTML = appState.playerTurn.name;
    elements.info.moves.innerHTML = `${appState.playerTurn.movesLeft} moves left`;
    elements.info.currentRoundNumber.innerHTML = `${appState.gameInfo.current_round}/${appState.gameInfo.max_round}`

    // Show player turn modal
    elements.moveSwitch.name.innerHTML = appState.playerTurn.name;
    elements.moveSwitch.dialog.showModal();
}

function switchMoveConfirm() {
    elements.moveSwitch.dialog.close();
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
        name: formObject.name,
        config: {
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

function openScreen(screenName) {
    // Close other screens and open selected screen
    for (const screen in elements.screens) {
        elements.screens[screen].style.display = "none";
    }
    elements.screens[screenName].style.display = "flex";
}

async function openExploreScreen() {
    openScreen("explore");

    // get current event
    await fetch(`${appState.backendBaseUrl}/events/${appState.gameId}`, { method:"GET"}).then(async (req) => {
        const res = await req.json();

        if (res.event === "No active event.") {
            elements.screens.explore.innerHTML = `<button class="explore-button" onclick="eventNextState(1)">Explore</button>`;
            return;
        }

        displayEventState(res.event);
    });
}

async function eventNextState(choice) {
    await fetch(`${appState.backendBaseUrl}/events/${appState.gameId}`, {
        method: "POST",
        body: JSON.stringify({ event_option: choice }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }).then(async (req) => {
        const res = await req.json();

        if (res.event === "Not enough moves to explore more.") {
            window.alert("Not enough moves to explore more.");
            return;
        }
        else if (res.event === "final") {
            elements.screens.explore.innerHTML = `<button class="explore-button" onclick="eventNextState(1)">Explore</button>`;
            return;
        }

        if (res.error) {
            window.alert(res.error);
            return;
        }

        displayEventState(res.event);
    });
}

async function displayEventState(eventInfo) {
    console.log(eventInfo);
    // Display event text and choices
    const event_container = document.createElement("div");
    event_container.classList.add("event-container");

    const event_text = document.createElement("p");
    event_text.innerHTML = eventInfo.text;
    event_text.classList.add("event-text");

    const event_choices = document.createElement("div");
    event_choices.classList.add("event-choices");

    for (const i in eventInfo.choices) {
        const choice = document.createElement("button");
        choice.innerHTML = eventInfo.choices[i]
        choice.classList.add("event-button");
        choice.addEventListener("click", () => eventNextState(Number(i)));

        event_choices.appendChild(choice);
    }

    elements.screens.explore.innerHTML = "";
    event_container.appendChild(event_text);
    event_container.appendChild(event_choices);

    elements.screens.explore.appendChild(event_container);
}

async function openTravelScreen() {
    openScreen("map");
}  

async function openItemsScreen() {
    openScreen("items");
}

async function openShopScreen() {
    openScreen("shop");

    // get shop items
    await fetch(`${appState.backendBaseUrl}/shop/${appState.gameId}`, { method:"GET"}).then(async (req) => {
        // parse items by rarity
        const res = await req.json();
        const items = res.shop;

        // add items to respective containers
        elements.shop.commonItemsContainer.innerHTML = "";
        elements.shop.rareItemsContainer.innerHTML = "";
        elements.shop.epicItemsContainer.innerHTML = "";
        elements.shop.legendaryItemsContainer.innerHTML = "";

        for(const i in items) {
            const item = items[i];

            // create item element
            const item_element = createElement("div");
            item_element.classList.add("shop-item");
            item_element.innerHTML = `<img src="./assets/images/items/${item.name}.png" alt="${item.name}">`;
            item_element.setAttribute('title', `Name: ${item.name} \nDescription: ${item.description}`);
            
            item_element.addEventListener("click", () => {
                const confirmPurchase = window.confirm(`Do you want to purchase ${item.name} for ${item.price}€?`);
                if(confirmPurchase) {
                    buyItem(item.id);
                }
            });

            // Create price label
            const price_label = createElement("span");
            price_label.innerHTML = `${item.price}€`;
            price_label.classList.add("item-price-label");
            item_element.appendChild(price_label);

            switch(item.rarity) {
                case "common":
                    elements.shop.commonItemsContainer.appendChild(item_element);
                    break;
                case "rare":
                    elements.shop.rareItemsContainer.appendChild(item_element);
                    break;
                case "epic":
                    elements.shop.epicItemsContainer.appendChild(item_element);
                    break;
                case "legendary":
                    elements.shop.legendaryItemsContainer.appendChild(item_element);
                    break;
            }
        }

        console.log(items);
    });
}

async function buyItem(itemId) {
    await fetch(`${appState.backendBaseUrl}/shop/${appState.gameId}`, {
        method: "POST",
        body: JSON.stringify({ item_id: itemId }),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    }).then(async (req) => {
        const res = await req.json();
        window.alert(res.message);
    });
}

async function endTurn() {
    await switchMove(false);
    openScreen("map");
}

async function exitGame() {
    window.localStorage.setItem("game_id", false);
    openScreen("map");
    await showGameSelect();
}

// Event listeners
elements.gameSelect.continueGameBtn.addEventListener("click", () => openGame(elements.gameSelect.gameSelected));
elements.gameSelect.createNewBtn.addEventListener("click", switchToGameCreate);
elements.gameCreate.addPlayerInputBtn.addEventListener("click", addPlayerInput);
elements.gameCreate.backBtn.addEventListener("click", switchToGameSelect);
elements.gameCreate.form.addEventListener("submit", gameCreateSubmit);
elements.moveSwitch.startMoveBtn.addEventListener("click", switchMoveConfirm);
elements.actionButtons.exploreBtn.addEventListener("click", openExploreScreen);
elements.actionButtons.travelBtn.addEventListener("click", openTravelScreen);
elements.actionButtons.itemBtn.addEventListener("click", openItemsScreen);
elements.actionButtons.shopBtn.addEventListener("click", openShopScreen);
elements.actionButtons.endturnBtn.addEventListener("click", endTurn);
elements.actionButtons.quitBtn.addEventListener("click", exitGame)

// Main/entry function
main();
