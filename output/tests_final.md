```markdown
# testsMahjong.feature

## Feature: Initialize Mahjong Game

### Scenario: Basic Game Initialization
  Given a new game of Mahjong is created
  When the game starts
  Then the total number of tiles should be 136
  And the flower and chow mein cards should be included
  And the game should have at least one AI opponent
  And the UI interface should display properly

## Feature: Tile Management

### Scenario: Drawing Tiles
  Given a game is in progress
  When a player draws a tile
  Then the total number of remaining tiles should decrease by 1
  And the drawn tile should be added to the player's hand
  And the UI should update with the new tile

### Scenario: Using Tiles for Calls
  Given a player has tiles in their hand matching a call pattern
  When they use three tiles to make a chi, pong, or kwat call
  Then those three tiles should be removed from their hand
  And the game state should reflect the completed set
  And proper animations for tile transitions should occur

## Feature: AI Opp