## Endpoints

### GET
- /games/game_id
  - Gets games by id, or all games if no id is given
- /games/game_id/players
  - Gets all players in specified game
- /events/game_id
  - Gets current event's state, or creates and returns new random event
  - Disallows starting an event if no moves are left
- /shop/game_id
  - Get all items in current game's shop

### POST
- /games
  - Creates new game with provided info, which is to be provided in JSON format, below is example of body content
    ```
    {
        "players": ["Player 1", "Player 2", "Player 3"],
        "config": {
            "max_round": int,
            "modifier": int,
            "starting_distance": int,
            "starting_balance": int,
            "starting_location": string (in form of ident)
        }
    }
    ```
- /games/game_id/end-turn
    - Ends player's turn, and returns next turn's relevant info
- /events/game_id
  - Updates event by running users option
  - Returns new event state
    ```
    {
        "event_option": int
    }
    ```
- /shop/game_id
  - Attempts to purchase the item
  - Returns whether or not purchase succeeded
    ```
    {
        "item_id": int
    }
    ```

## Backend endpoint TODO
- Handle items
- Handle scoring
- Get player whose turn it is

## NOTE
- Haven't updated dump yet, run this in mariadb
```
ALTER TABLE game ADD archived bool;
ALTER TABLE game ADD name varchar(255) NOT NULL;
ALTER TABLE game ADD created_at DATETIME NOT NULL DEFAULT NOW();
alter table game add column event_id int;
alter table game add column event_state int;
```