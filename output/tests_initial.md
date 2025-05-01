Here is a comprehensive set of unit tests in BDD style using `pytest-bdd` for the Single-Player Cantonese Mahjong Game. These tests cover key features and functionality as per the specification document.

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

### Scenario: Using Tiles
  Given a player has tiles in their hand
  When they use a tile to make a call (chi, pong, kwat)
  Then the tile should be removed from their hand
  And the game state should update accordingly
  And proper animations for tile transitions should occur

## Feature: AI Opponent System

### Scenario: Basic AI Behavior
  Given an AI opponent is created at novice level
  When the AI makes a move
  Then the move should be valid according to Mahjong rules
  And the AI's skill level should affect its decision-making process