# Single-Player Cantonese Mahjong Game Architecture Design

## 1. Modular Architecture Overview

The game is designed using a layered architecture with clear separation of concerns, allowing for scalability and extensibility.

```

## 2. Core Modules

### 2.1. Data Layer

- **Tile Management**
  - Handles the initialization, shuffling, and distribution of tiles.
  - Supports flower and chow mein cards integration.

- **Player Stats & Achievements**
  - Manages player progress, skill levels, and milestones tracking.
  - Implements reward system for achievements.

- **Configuration**
  - Stores game settings, including rules variants and UI preferences.

```

### 2.2. Business Logic Layer

- **Rule Implementation**
  - Enforces Cantonese Mahjong rules during gameplay.
  - Validates moves according to "chi, pong, kwat" calls.

- **Scoring System**
  - Calculates scores based on traditional Cantonese mechanics.
  - Handles bonuses from flower and chow mein cards.

```

### 2.3. Game Engine

- **Game Mechanics**
  - Manages tile drawing, discarding, and melding operations.
  - Implements game phases and transitions between them.

- **AI Opponent System**
  - Provides multiple skill levels (novice to expert).
  - Includes a learning algorithm for AI improvement through player interactions.

```

### 2.4. User Interface Layer

- **UI/UX Design**
  - Implements intuitive interface with clean layout.
  - Supports accessibility features like colorblind modes and font size adjustments.

- **Tile Design & Animations**
  - Renders traditional Cantonese tile designs.
  - Provides smooth animations for gameplay fluidity.

```

### 2.5. Platform Services

- **Cross-Platform Compatibility**
  - Supports PC/Mac, iOS, and Android platforms through a platform-agnostic layer.
  - Ensures seamless experience across devices with cloud saves and sync capabilities.

```

### 2.6. Additional Features

- **Customization Options**
  - Offers multiple tile themes (traditional, modern).
  - Allows customization of music, sound effects, and background visuals.

- **Tutorial System & Rulebook**
  - Provides in-game tutorials for gameplay mechanics.
  - Includes comprehensive rule explanations and