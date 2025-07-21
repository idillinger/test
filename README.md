# Simple 2-D “Minecraft” Clone (Console Edition)

This is an extremely lightweight sandbox written in C++. It is **not** a full 3-D voxel engine—just a tiny 2-D toy to demonstrate basic gameplay mechanics (move, place, remove blocks) inside the terminal.

## Controls

```
W  move up
A  move left
S  move down
D  move right
P  place a block (#) at the current position
R  remove a block at the current position
Q  quit the game
```
The player is represented by `@`, blocks by `#`, and empty space by `.`.

## Build

Ensure you have a C++17-capable compiler (e.g., **g++** 7+ or **clang++** 5+).

```bash
# From the project root
 g++ -std=c++17 -O2 main.cpp -o mincraft
```

## Run

```bash
./mincraft
```

Enjoy your miniature mining adventure! 🎮️