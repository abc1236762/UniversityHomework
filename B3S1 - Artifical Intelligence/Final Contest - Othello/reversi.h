#include <stdio.h>
#include <memory.h>
#include <time.h>
#include <assert.h>
#include <ctype.h>
#include <stdbool.h>
#include <limits.h>

#define BOARD_SIZE 8

int reversi(void);

void delay(clock_t ms);

void read_weight(int id);

void read_file(char *input);

char load_file(void);

void init(void);

bool play_a_move(int x, int y);

bool put_a_stone(int x, int y);

void show_board_and_set_legal_moves(void);

int find_legal_moves(int color);

bool is_crossed(int x, int y, int update);

int check_straight_army(int x, int y, int d, int update);

bool is_in_board(int x, int y);

int compute_grades(int flag);

bool is_game_ended(void);

void computer_think(int *x, int *y);

bool search(int my_turn, int my_level);

int search_next(int x, int y, int my_turn, int my_level, int alpha, int beta);
