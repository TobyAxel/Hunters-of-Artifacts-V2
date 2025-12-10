# Game API Endpoints

## Base URL
`http://127.0.0.1:3000`

## Endpoints

### Games

#### Get All Games
```
GET /games
```
Returns all non-archived games.

#### Create New Game
```
POST /games
```
**Request Body:**
```json
{
  "name": "Game Name",
  "players": ["Player1", "Player2", "Player3"],
  "config": {
    "max_round": 10,
    "modifier": 1.0,
    "starting_distance": 0,
    "starting_balance": 5000,
    "starting_location": "EFHK"
  }
}
```

#### Get Specific Game
```
GET /games/<game_id>
```
Returns game details by ID.

---

### Players

#### Get Players in Game
```
GET /games/<game_id>/players
```
Returns all players in the specified game.

#### Get Player's Items
```
GET /games/<game_id>/player/items
```
Returns current player's inventory with item descriptions.

#### Use Item
```
POST /games/<game_id>/player/items/<item_name>/use-item
```
Uses an item from current player's inventory. Item must be usable.

#### Get Active Effects
```
GET /games/<game_id>/player/active-effects
```
Returns current player's active effects.

---

### Events

#### Get Current Event
```
GET /games/<game_id>/event
```
Returns current event text and available choices. If no event is active, returns "No active event."

#### Create/Update Event
```
POST /games/<game_id>/event
```
**Request Body:**
```json
{
  "event_option": 1
}
```
- If no active event: Creates new event (costs 1 move)
- If active event: Selects the specified option and progresses event
- Returns next event state or "final" when event completes

---

### Shop

#### Get Shop Items
```
GET /games/<game_id>/shop
```
Returns available shop items based on current round progress:
- Round ≤25%: Common items only
- Round ≤50%: Common + Rare items
- Round ≤75%: Common + Rare + Epic items
- Round >75%: All items (including Legendary)

#### Buy Item
```
POST /games/<game_id>/shop
```
**Request Body:**
```json
{
  "item_id": 0
}
```
Purchases item at specified index from shop. Deducts price from player balance.

---

### Travel

#### Get Airports
```
GET /games/<game_id>/airports?max_distance_km=<number>
```
**Query Parameters:**
- `max_distance_km` (optional): Filter airports within this distance

Returns list of available airports.

#### Get Travel Info
```
GET /games/<game_id>/travel?arr_ident=<code>
```
**Query Parameters:**
- `arr_ident` (required): Airport identifier code (e.g., "EFHK")

Returns travel details including price and distance.

#### Travel to Airport
```
POST /games/<game_id>/travel?arr_ident=<code>
```
**Query Parameters:**
- `arr_ident` (required): Airport identifier code

Moves player to specified airport. Deducts travel price and 1 move.

---

### Game Actions

#### End Turn
```
POST /games/<game_id>/end-turn
```
Ends current player's turn and:
- Lowers active effect durations
- Moves to next player
- Increments round if all players completed turn
- Resets moves (base 2, modified by items/effects)
- Clears event state
- Ends game if max rounds reached

Returns updated game state or end game results.

#### Get Artifacts
```
GET /games/<game_id>/artifacts
```
Returns all artifact items grouped by player screen name.