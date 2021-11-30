# 0. Degrees

In this problem we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is equal to 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

This can be framed as a search problem where states in the search space are the actors. Actions are movies, which take us from one actor to the other. Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search (therefore implementing a queue-like frontier) we can find the shortest path from one actor to another.

## Usage

`$ python degrees.py large`
