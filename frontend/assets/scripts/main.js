"use strict";

// State

const appState = {
    backendBaseUrl: "http://127.0.0.1:3000",
    gameId: null,
    gameList: [],
    gameInfo: {
        max_round: null,
        current_round: null,
        artifacts: []
    },
    playerTurn: {
        id: 0,
        name: "Some Player",
        money: 500,
        travelled: 0,
        movesLeft: 2,
        location: null,
        effects: []
    },
    airports: [],
    selectedAirport: {
        ident: null,
        name: null,
        flightDistance: null,
        flightPrice: null,
    },
};

const elements = {
    info: {
        player: document.querySelector("#player-turn-info"),
        moves: document.querySelector("#moves-info"),
        accountBalance: document.querySelector("#account-balance-info"),
        distanceTravelled: document.querySelector("#distance-travelled-info"),
        currentRoundNumber: document.querySelector("#current-round-number"),
        currentRoundList: document.querySelector("#current-round-list"),
        activeEffectList: document.querySelector('#active-effects-list'),
        artifactsList: document.querySelector('#artifacts-list')
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
        map: document.querySelector("#map-outer"),
        items: document.querySelector("#items"),
        shop: document.querySelector("#shop"),
    },
    shop: {
        commonItemsContainer: document.querySelector("#common-shelf"),
        rareItemsContainer: document.querySelector("#rare-shelf"),
        epicItemsContainer: document.querySelector("#epic-shelf"),
        legendaryItemsContainer: document.querySelector("#legendary-shelf"),
    },
    items: {
        itemsContainer: document.querySelector("#item-grid")
    },
    actionButtons: {
        exploreBtn: document.querySelector("#explore-action"),
        travelBtn: document.querySelector("#travel-action"),
        itemBtn: document.querySelector("#item-action"),
        shopBtn: document.querySelector("#shop-action"),
        endturnBtn: document.querySelector("#end-turn-action"),
        quitBtn: document.querySelector("#quit-action"),
    },
    map: {
        map: L.map('map').setView([60.867883, 26.704160], 13),
        airportsLayer: L.layerGroup([]),
        airportMarkers: [],
        airportMarker: (isSelected) => L.divIcon({
            className: 'custom-icon',
            iconSize: [25, 25],
            html: `
            <svg width="25" height="25" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
                <path fill="${isSelected ? "var(--target-hover-bg)" : "var(--primary-hover-bg)"}" d="
                    M25 6
                    A19 19 0 1 1 25 44
                    A19 19 0 1 1 25 6
                    Z

                    M1 21 H9 V29 H1 Z
                    M41 21 H49 V29 H41 Z
                    M21 1 H29 V9 H21 Z
                    M21 41 H29 V49 H21 Z
                "/>
            </svg>
            `
        }),
        locationMarker: (isSelected) => L.divIcon({
            className: 'custom-icon',
            iconSize: [60, 60],
            html: `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
                <!--!Font Awesome Free v7.1.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.-->
                <path fill="${isSelected ? "var(--target-hover-bg)" : "var(--primary-hover-bg)"}"
                    d="M376 88C376 57.1 350.9 32 320 32C289.1 32 264 57.1 264 88C264 118.9 289.1 144 320 144C350.9 144 376 118.9 376 88zM400 300.7L446.3 363.1C456.8 377.3 476.9 380.3 491.1 369.7C505.3 359.1 508.3 339.1 497.7 324.9L427.2 229.9C402 196 362.3 176 320 176C277.7 176 238 196 212.8 229.9L142.3 324.9C131.8 339.1 134.7 359.1 148.9 369.7C163.1 380.3 183.1 377.3 193.7 363.1L240 300.7L240 576C240 593.7 254.3 608 272 608C289.7 608 304 593.7 304 576L304 416C304 407.2 311.2 400 320 400C328.8 400 336 407.2 336 416L336 576C336 593.7 350.3 608 368 608C385.7 608 400 593.7 400 576L400 300.7z" />
            </svg>
            `
        }),
        routeLayer: L.layerGroup([]),
        route: null,
    },
    selectedAirport: {
        container: document.querySelector("#selected-airport-information"),
        ident: document.querySelector("#selected-airport-ident"),
        name: document.querySelector("#selected-airport-name"),
        flightDistance: document.querySelector("#selected-airport-flight-distance"),
        flightPrice: document.querySelector("#selected-airport-flight-price"),
        travelBtn: document.querySelector("#selected-airport-travel"),
        noTravel: document.querySelector("#selected-airport-no-travel"),
    }
};

// Main functions

// Main entry function
async function main() {
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 10,
        minZoom: 5,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(elements.map.map);
    elements.map.airportsLayer.addTo(elements.map.map);
    elements.map.routeLayer.addTo(elements.map.map);

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

async function fetchAirports() {
    // set appState.airports
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/airports`).then(async (req) => {
        appState.airports = await req.json();
        console.log(appState.airports);
    });
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
    let game_ended = false;
    if(!initial) {
        await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/end-turn`, { method: "POST" }).then(async (req) => {
            const res = await req.json();
            if (res.game_ended) {
                console.log(res);
                for (const i in res.categories) {
                    const data = res.categories[i];
                    window.alert(`${data.category}\n${data.text}`)
                }
                await exitGame();
                game_ended = true;
            }
        });
    }
    if (game_ended) return;

    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}`).then(async (req) => {
        const res = await req.json();
        // Save data to app state
        appState.gameInfo.max_round = res[0].max_round;
        appState.gameInfo.current_round = res[0].round;
        appState.playerTurn.id = res[0].player_turn;
    });
    // Deselect airport
    appState.selectedAirport.ident = null;
    appState.selectedAirport.name = null;
    appState.selectedAirport.travelDistance = null;
    appState.selectedAirport.travelPrice = null;

    // Fetch airports for the appState.airports
    await fetchAirports();

    // Display data from app state in the elements
    await updateData();
    elements.info.moves.innerHTML = `${appState.playerTurn.movesLeft} moves left`;
    elements.info.currentRoundNumber.innerHTML = `${appState.gameInfo.current_round}/${appState.gameInfo.max_round}`;

    // Show player turn modal
    elements.moveSwitch.name.innerHTML = appState.playerTurn.name;
    elements.moveSwitch.dialog.showModal();
}

async function updateData() {
    // Fetch and store user data
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/players`).then(async (req) => {
        const res = await req.json();

        for (let i in res) {
            const player = res[i];

            if (player.id !== appState.playerTurn.id) continue

            appState.playerTurn.name = player.screen_name;
            appState.playerTurn.money = player.balance;
            appState.playerTurn.travelled = player.distance_travelled;
            appState.playerTurn.location = player.location;
        }
    });
    // Fetch and store player's active effects
    await fetch(`${appState.backendBaseUrl}/player/active-effects/${appState.playerTurn.id}`).then(async (req) => {
        // Save data to app state
        appState.playerTurn.effects = await req.json();
    });
    // Fetch and store game data
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}`).then(async (req) => {
        const res = await req.json();
        // Save data to app state
        appState.playerTurn.movesLeft = res[0].moves;
    });
    // Fetch and store all artifacts
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/artifacts`).then(async (req) => {
        // Save data to app state
        appState.gameInfo.artifacts = await req.json();
    });

    // Update html elements
    elements.info.player.innerHTML = appState.playerTurn.name;
    elements.info.accountBalance.innerHTML = appState.playerTurn.money + '€';
    elements.info.distanceTravelled.innerHTML = appState.playerTurn.travelled + 'km travelled';
    elements.info.moves.innerHTML = appState.playerTurn.movesLeft + ' moves left';

    // Show active effects
    elements.info.activeEffectList.innerHTML = "";
    for (let i in appState.playerTurn.effects) {
        const effect = appState.playerTurn.effects[i];
        if (effect.duration === 0) continue;
        elements.info.activeEffectList.innerHTML += `<div>${effect.effect_name} - ${effect.duration > 1 ? effect.duration + ' turns left' : 'Ends this turn'}</div>`
    }

    // Show artifacts
    elements.info.artifactsList.innerHTML = "";
    if (Object.keys(appState.gameInfo.artifacts).length == 0) elements.info.artifactsList.innerHTML = 'Nobody owns any artifacts yet.';
    for (let i in appState.gameInfo.artifacts) {
        const player = appState.gameInfo.artifacts[i];
        elements.info.artifactsList.innerHTML += `<div>${i}</div>`;
        for (const j in appState.gameInfo.artifacts[i]) {
            elements.info.artifactsList.innerHTML += `<div>- ${appState.gameInfo.artifacts[i][j]}</div>`
        }
    }

    // Remove the existing route line
    if(elements.map.route) {
        elements.map.routeLayer.removeLayer(elements.map.route);
        elements.map.route = null;
    }

    // Update chosen airport data
    if(appState.selectedAirport.ident) {
        elements.selectedAirport.container.style.display = "flex";
        elements.selectedAirport.ident.innerHTML = appState.selectedAirport.ident;
        elements.selectedAirport.name.innerHTML = appState.selectedAirport.name;
        elements.selectedAirport.flightDistance.innerHTML = appState.selectedAirport.flightDistance;
        elements.selectedAirport.flightPrice.innerHTML = appState.selectedAirport.flightPrice;
        // Display travel button only if player can travel there
        if(
            appState.playerTurn.money >= appState.selectedAirport.flightPrice &&
            appState.playerTurn.location != appState.selectedAirport.ident &&
            appState.playerTurn.movesLeft > 0
        ) {
            elements.selectedAirport.travelBtn.style.display = "block";
            elements.selectedAirport.noTravel.style.display = "none";
        } else {
            elements.selectedAirport.travelBtn.style.display = "none";
            elements.selectedAirport.noTravel.style.display = "block";
        }
        // Draw the route line if chosen airport is not the same as the player's location
        if(appState.playerTurn.location != appState.selectedAirport.ident) {
            // Get full airport data to later know the location
            const startPoint = appState.airports.find((airport) => airport.ident == appState.playerTurn.location);
            const endPoint = appState.airports.find((airport) => airport.ident == appState.selectedAirport.ident);

            // Draw a line between two airport points
            elements.map.route = new L.Geodesic([[startPoint.latitude_deg, startPoint.longitude_deg], [endPoint.latitude_deg, endPoint.longitude_deg]], {color: "#0000b4ff"});
            elements.map.route.addTo(elements.map.routeLayer);
        }
    } else {
        elements.selectedAirport.container.style.display = "none";
    }

    // Update markers on the map
    updateMarkers();
}

// Event listener functions
// May be called by functions outside of listeners too

function switchToGameCreate() {
    elements.gameSelect.dialog.close();
    elements.gameCreate.dialog.showModal();
}

function switchToGameSelect() {
    elements.gameCreate.dialog.close();
    elements.gameSelect.dialog.showModal();
}

function switchMoveConfirm() {
    elements.moveSwitch.dialog.close();
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
    // get current event
    await fetch(`${appState.backendBaseUrl}/events/${appState.gameId}`, { method:"GET"}).then(async (req) => {
        const res = await req.json();

        if (res.event === "No active event.") {
            elements.screens.explore.innerHTML = `<button class="action-button" onclick="eventNextState(1)">Explore</button>`;
            return;
        }

        displayEventState(res.event);
    });

    openScreen("explore");
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
            elements.screens.explore.innerHTML = `<button class="action-button" onclick="eventNextState(1)">Explore</button>`;
            return;
        }

        if (res.error) {
            window.alert(res.error);
            return;
        }

        updateData()
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
        choice.classList.add("action-button-sm");
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
    await fetch(`${appState.backendBaseUrl}/player/items/${appState.playerTurn.id}`, { method:"GET"}).then(async (req) => {
        const res = await req.json();

        console.log(res);
        
        elements.items.itemsContainer.innerHTML = "";
        for (let i in res) {
            const item = res[i];
            const item_element = document.createElement("div");
            item_element.classList.add("item");
            item_element.innerHTML = `<img src="./assets/images/items/${item.name}.png" alt="${item.name}">`;
            item_element.setAttribute('title', `Name: ${item.name} \nDescription: ${item.description}`)

            item_element.addEventListener('click', function() {useItem(item, item_element)});

            elements.items.itemsContainer.appendChild(item_element);
        }
    });
    
    openScreen("items");
}

async function useItem(item, element) {
    const confirmUse = window.confirm(`Do you want to use ${item.name}?`);
    if(confirmUse) {
        await fetch(`${appState.backendBaseUrl}/items/${appState.gameId}`, {
            method: "POST",
            body: JSON.stringify({item_name: item.name}),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        }).then(async (req) => {
            const res = await req.json();
            console.log(res)
            if (res.message !== "Item is not usable.") {
                // Deselect airport
                appState.selectedAirport.ident = null;
                appState.selectedAirport.name = null;
                appState.selectedAirport.travelDistance = null;
                appState.selectedAirport.travelPrice = null;
                await fetchAirports();
                updateData();
                element.parentNode.removeChild(element);
            }
            window.alert(res.message);
        });
    }
}

async function openShopScreen() {
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
            item_element.classList.add("item");
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

    openScreen("shop");
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
        updateData();
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

// Updates markers whenever a map is moved or the data changed
function updateMarkers() {
    // Get map position
    const bounds = elements.map.map.getBounds();

    // Delete previous airport markers and route
    elements.map.airportMarkers.forEach((marker) => elements.map.airportsLayer.removeLayer(marker));
    elements.map.airportMarkers = [];

    // Iterate through array of airports fetched in main
    appState.airports.forEach((airport) => {
        const latlng = [airport.latitude_deg, airport.longitude_deg];
        // Only add markers of airports visible inside boundary
        if (!bounds.contains(latlng)) return;

        // Marker style
        const icon = airport.ident == appState.playerTurn.location ? elements.map.locationMarker(appState.selectedAirport.ident == airport.ident) : elements.map.airportMarker(appState.selectedAirport.ident == airport.ident);

        // Add airport markers to the elements.map.airportsLayer
        const marker = L.marker(latlng, { icon }).on('click', (e) => {
            // Update selected airport data on click
            appState.selectedAirport = {
                ident: airport.ident,
                name: airport.name,
                flightDistance: airport.distance_km,
                flightPrice: airport.travel_price,
            };
            updateData();
        });
        marker.addTo(elements.map.airportsLayer);
        elements.map.airportMarkers.push(marker);
    })
}

// On selected airport travel button click
async function travel() {
    // Send travel request
    await fetch(`${appState.backendBaseUrl}/games/${appState.gameId}/travel?arr_ident=${appState.selectedAirport.ident}`, { method: "POST"});

    // Deselect airport
    appState.selectedAirport.ident = null;
    appState.selectedAirport.name = null;
    appState.selectedAirport.travelDistance = null;
    appState.selectedAirport.travelPrice = null;

    // Update airport list to also fetch new correct travel prices
    await fetchAirports();

    // Update the elements
    updateData();
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
elements.actionButtons.quitBtn.addEventListener("click", exitGame);
elements.map.map.on('moveend', updateMarkers);
elements.selectedAirport.travelBtn.addEventListener("click", travel);

// Main/entry function
main();
