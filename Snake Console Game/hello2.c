#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <windows.h>
HANDLE hConsole;

#define row 15
#define col 15
int sleep_time = 300; 
char board[row][col];
int snakex = 5, snakey = 5;
int isgamerover = 0;
int foodx, foody;

struct snakepart {
    int x, y;
};

struct snake {
    int length;
    struct snakepart snakebody[256];
} snake;

void filling_board() {
    int i, j;
    for (i = 0; i < row; i++) {
        for (j = 0; j < col; j++) {
            if ((i == 0 && j == 0) || (i == 0 && j == col - 1) ||
                (i == row - 1 && j == 0) || (i == row - 1 && j == col - 1)) {
                board[i][j] = '+';
            } else if (i == 0 || i == row - 1) {
                board[i][j] = '-'; 
            } else if (j == 0 || j == col - 1) {
                board[i][j] = '|'; 
            } else {
                board[i][j] = ' ';
            }
        }
    }
}


void drawsnake() {
     board[foody][foodx] = '$';  
    board[snake.snakebody[0].y][snake.snakebody[0].x] = '@';
    for (int i = 1; i < snake.length; i++) {
        board[snake.snakebody[i].y][snake.snakebody[i].x] = '*';
    }

}
void generate_food() {
    while (1) {
        foodx = rand() % (col - 2) + 1;
        foody = rand() % (row - 2) + 1;
        int is_on_snake = 0;
        for (int i = 0; i < snake.length; i++) {
            if (snake.snakebody[i].x == foodx && snake.snakebody[i].y == foody) {
                is_on_snake = 1;
                break;
            }
        }

        if (!is_on_snake) break;  
    }
}

void move_snake(int x, int y) {
    snakex += x;
    snakey += y;

    for (int i = snake.length; i > 0; i--) {
        snake.snakebody[i] = snake.snakebody[i - 1];
    }

    snake.snakebody[0].x = snakex;
    snake.snakebody[0].y = snakey;

    if (board[snakey][snakex] == '#' || board[snakey][snakex] == '*') {
        isgamerover = 1;
    }
    if (snakex == foodx && snakey == foody) {
    snake.length++;
    generate_food();
    if(sleep_time>50){
        sleep_time -=10;
    }  
}

}

void readkeyboard() {
    char ch = getch();  
    switch (ch) {
        case 'w': move_snake(0, -1); break;
        case 's': move_snake(0, 1); break;
        case 'a': move_snake(-1, 0); break;
        case 'd': move_snake(1, 0); break;
    }
}

void printboard() {
    system("cls");
    printf("Score: %d\n", snake.length - 1);
    SetConsoleTextAttribute(hConsole, BACKGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);

    for (int i = 0; i < row; i++) {
        for (int j = 0; j < col; j++) {
            char ch = board[i][j];
            switch (ch) {
                case '+': case '-': case '|':
                    SetConsoleTextAttribute(hConsole, 8); 
                    break;
                case '@':
                    SetConsoleTextAttribute(hConsole, 10); 
                    break;
                case '*':
                    SetConsoleTextAttribute(hConsole, 2);  
                    break;
                case '$':
                    SetConsoleTextAttribute(hConsole, 12); 
                    break;
                default:
                    SetConsoleTextAttribute(hConsole, 7);  
            }
            putchar(ch);
        }
        putchar('\n');
    }
    SetConsoleTextAttribute(hConsole, 7);
}

int main() {
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    snake.length = 1;
    snake.snakebody[0].x = snakex;
    snake.snakebody[0].y = snakey;
    srand(time(NULL)); 
    while (!isgamerover) {
        filling_board();
        drawsnake();
        printboard();
        readkeyboard();
        Sleep(sleep_time);
    }
    printf("%d\n",snake.length-1);
    printf("Game Over!\n\n");
    return 0;
}
