# 4. Nim

In a game of Nim we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses.

There’s some simple strategy you might imagine for this game: if there’s only one pile and three objects left in it, and it’s your turn, the best bet is to remove two of those objects, leaving your opponent with the third and final object to remove. However, in case there are more piles the strategy gets considerably more complicated. 
In this problem, an AI is built to learn a game-playing strategy through **reinforcement learning**. By playing against itself repeatedly and learning from experience, eventually the AI learns which actions to take and which actions to avoid.

**Q-learning** is employed as an approach. In Q-learning, we try to learn a reward value for every (state, action) pair. An action that loses the game will have a reward of -1, whereas an action that results in the other player losing the game will have a reward of 1; finally, an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.

## Usage

`$ python play.py`