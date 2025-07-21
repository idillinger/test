#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

// Simple 2-D “Minecraft” clone for the console.
// Controls:
//   W A S D – move up/left/down/right
//   P       – place a block (#) at current position
//   R       – remove a block at current position
//   Q       – quit the game
// Empty space: '.'  Block: '#', Player: '@'

static const int WIDTH  = 30;
static const int HEIGHT = 15;

struct World {
    std::vector<std::string> grid;
    int playerX, playerY; // X = column, Y = row

    World() : grid(HEIGHT, std::string(WIDTH, '.')) {
        // Generate a flat ground two rows from bottom.
        for (int x = 0; x < WIDTH; ++x) {
            grid[HEIGHT - 2][x] = '#';
            grid[HEIGHT - 1][x] = '#';
        }
        // Place player roughly in the middle.
        playerX = WIDTH / 2;
        playerY = HEIGHT - 3;
    }

    void draw() {
        // Clear screen (ANSI escape; works on most *nix terminals)
        std::cout << "\033[2J\033[H";
        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                if (x == playerX && y == playerY)
                    std::cout << '@';
                else
                    std::cout << grid[y][x];
            }
            std::cout << '\n';
        }
        std::cout << "\nControls: W/A/S/D move  P place  R remove  Q quit\n";
    }

    bool inBounds(int x, int y) const {
        return x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT;
    }

    void placeBlock() {
        if (inBounds(playerX, playerY)) {
            grid[playerY][playerX] = '#';
        }
    }

    void removeBlock() {
        if (inBounds(playerX, playerY)) {
            grid[playerY][playerX] = '.';
        }
    }

    void movePlayer(int dx, int dy) {
        int newX = playerX + dx;
        int newY = playerY + dy;
        if (inBounds(newX, newY) && grid[newY][newX] == '.') {
            playerX = newX;
            playerY = newY;
        }
    }
};

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    World world;
    world.draw();

    char cmd;
    while (std::cin >> cmd) {
        cmd = std::tolower(cmd);
        switch (cmd) {
            case 'w': world.movePlayer(0, -1); break;
            case 'a': world.movePlayer(-1, 0); break;
            case 's': world.movePlayer(0, 1); break;
            case 'd': world.movePlayer(1, 0); break;
            case 'p': world.placeBlock(); break;
            case 'r': world.removeBlock(); break;
            case 'q': std::cout << "Goodbye!\n"; return 0;
            default: break;
        }
        world.draw();
    }
    return 0;
}