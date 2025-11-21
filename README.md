## Endpoints

### GET
- /games
  - Gets all games in database
- /games/id
  - Gets game by id which is in form int
- /games/id/players
  - Gets all players in specified game

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

## Backend endpoint requirements
- Loading data
- Get/Update stats
- Get/Update location
- Get/Update items
- Get event
- Manage game state
- Handle travel

## NOTE
- Haven't updated dump yet, run this in mariadb
- ALTER TABLE game
    -> ADD archived bool;