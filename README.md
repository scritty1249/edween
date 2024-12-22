# edween
The overarching goal of this project is to create an automated actor on Discord to access live match data from the Riot API that sends responses tailored to the conditions of the ongoing game.

## Key points
This project should fufill the following criteria:
- Access account connections of Discord profiles (riot account connection)
- Accepts messages on Discord
  - Responds to messages on Discord
- Accesses the Riot API
  - Retrieves data from an ongoing match specified through Discord
    - Retreives identifying information for Riot API from given information on Discord
- Processes the information in a meaningful way
  - Creates a specific Discord response based off of in-game conditions inferred or indicated by the data from Riot API

## Opening Feature Suggestions
These goals are subject to change as the project progresses and are not required:
- Zero money spent on project
- Runs without a local device for hosting
- Composes disparaging or negative messages based on game conditions as they progress in realtime
- Detects areas where players have died the most on the game map
- Detects the following in-game conditions:
  - Lane phase is over
    - is a tower taken already?
    - match duration?
    - other players leaving designated lanes?
  - Gold surplus / deficit
    - compares gold and item count to lane opponent
  - "Inting" / "Feeding"
    - Higher kill to death ratio compared to team
    - Low creep score
    - Bad champion matchup (refers to databsae from third party or in-house)
