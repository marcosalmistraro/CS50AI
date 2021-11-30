# 4. Nim

A game of Nim begins with some number of piles, each with some number of objects. Players take turns: on a player’s turn, any non-negative number of objects are removed from any one non-empty pile. Whoever removes the last object loses.

There’s some simple strategy that can be envisioned: if there’s only one pile and three objects left in it, the best bet is to remove two of those objects, leaving the opponent with the third and final object to remove. However, in case there are more piles the strategy gets considerably more complicated. 
With such premises, an AI is built to learn a game-playing strategy through **reinforcement learning**. By playing against itself repeatedly and learning from experience, the AI eventually learns which actions to take and which others to avoid.

**Q-learning** is employed as an approach. In Q-learning, the AI tries to learn a reward value for every (state, action) pair. An action that loses the game will have a reward of -1, whereas an action that results in the opponent losing the game will have a reward of 1; finally, an action that results in the game continuing has an immediate reward of 0, but will also have a certain future reward.

## Usage

`$ python play.py`
