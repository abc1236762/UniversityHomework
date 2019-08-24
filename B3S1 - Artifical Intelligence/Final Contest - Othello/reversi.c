#include "reversi.h"

int search_counter;
int com_take;
int winner;
int now_board[BOARD_SIZE][BOARD_SIZE];
// mark the dead stone
// int dead_stone[BOARD_SIZE][BOARD_SIZE];
bool now_board_is_move_legal[BOARD_SIZE][BOARD_SIZE];
int hand_num;
int sequence[100];

int black_count, white_count;
int turn = 0; // 0 is black or 1 is white
const int stones[2] = {1, 2}; // 1: black, 2: white
const int dir_x[8] = {0, 1, 1, 1, 0, -1, -1, -1};
const int dir_y[8] = {-1, -1, 0, 1, 1, 1, 0, -1};

int last_x, last_y;
// int auto_check_dead;

const int search_deep = 6;

const bool alpha_beta_option = true;
int result_x, result_y;
// int search_level_now;

int board_weight[BOARD_SIZE][BOARD_SIZE] = {
	// A~H
	{20, -3, 11, 8, 8, 11, -3, 20}, // 1
	{-3, -7, -4, 1, 1, -4, -7, -3},
	{11, -4, 2, 2, 2, 2, -4, 11},
	{8, 1, 2, -3, -3, 2, 1, 8},
	{8, 1, 2, -3, -3, 2, 1, 8},
	{11, -4, 2, 2, 2, 2, -4, 11},
	{-3, -7, -4, 1, 1, -4, -7, -3},
	{20, -3, 11, 8, 8, 11, -3, 20}, // 8
};

typedef struct { int i, j, g; } loc;

int reversi(void) {
	char com_color = 'W';
	int x, y, n, moves = 0;
	
	init();
	printf(
		"Computer take (\n"
		"\t[B]lack, [W]hite, [A]ll, [L]oad and play,\n"
		"\tFile play at [1]st, File play at [2]nd\n"
		"): "
	);
	scanf("%c", &com_color);
	com_color = (char)toupper(com_color);
	if (com_color == 'F') com_color = '1';
	if (com_color == 'S') com_color = '2';
	if (com_color == '1' || com_color == '2')
		read_weight(com_color - '0');
	else
		read_weight(-1);
		
	show_board_and_set_legal_moves();
	
	if (com_color == 'L') com_color = load_file();
	else if (com_color == 'B') {
		computer_think(&x, &y);
		if (x == -1) printf("Computer pass\n");
		else printf("Computer played %c%d\n", 'A' + x, 1 + y);
		play_a_move(x, y);
		show_board_and_set_legal_moves();
	} else if (com_color == 'A') {
		while (moves++ < 64) {
			computer_think(&x, &y);
			if (!play_a_move(x, y)) {
				printf("Wrong computer moves %c%d\n", 'A' + x, 1 + y);
				scanf("%d", &n);
				break;
			}
			
			if (x == -1) printf("Computer pass\n");
			else printf("Computer played %c%d\n", 'A' + x, 1 + y);
			
			if (is_game_ended()) return 0;
			show_board_and_set_legal_moves();
		}
	} else if (com_color == '1') {
		computer_think(&x, &y);
		play_a_move(x, y);
	}
	
	char input[3];
	while (moves++ < 64) {
		while (true) {
			if (com_color == '1' || com_color == '2') {
				
				FILE *file = fopen("of.txt", "r");
				fscanf(file, "%d", &n);
				fclose(file);
				
				if (com_color == '1') {
					if (n % 2 == 0)
						read_file(input);
					else {
						delay(100);
						continue;
					}
				} else {
					if (n % 2 == 1)
						read_file(input);
					else {
						delay(100);
						continue;
					}
				}
			} else if (com_color == 'B') {
				printf("Input white move: [A-H][1-8], or [P]ass\n");
				scanf("%s", input);
			} else if (com_color == 'W') {
				printf("Input black move: [A-H][1-8], or [P]ass\n");
				scanf("%s", input);
			}
			
			int column_input = -1, row_input = -1;
			input[0] = (char)toupper(input[0]);
			if (input[0] == 'P')
				row_input = column_input = -1;
			else if (input[0] == 'M') {
				computer_think(&x, &y);
				if (!play_a_move(x, y)) {
					printf("Wrong computer moves %c%d\n", 'A' + x, 1 + y);
					scanf("%d", &n);
					break;
				}
				if (x == -1) printf("Computer pass");
				else printf("Computer played %c%d\n", 'A' + x, 1 + y);
				if (is_game_ended()) break;
				show_board_and_set_legal_moves();
			} else {
				row_input = input[0] - 'A';
				column_input = input[1] - '1';
			}
			// printf("%d, %d\n", row_input, column_input);
			
			if (!play_a_move(row_input, column_input))
				printf("%c%d is a wrong move\n", input[0], 1 + column_input);
			else break;
		}
		if (is_game_ended()) return 0;
		show_board_and_set_legal_moves();
		
		computer_think(&x, &y);
		if (x == -1) printf("Computer pass\n");
		else printf("Computer played %c%d\n", 'A' + x, 1 + y);
		play_a_move(x, y);
		if (is_game_ended()) return 0;
		show_board_and_set_legal_moves();
	}
	
	printf("Game is over");
	// scanf("%d", &n);
	
	return 0;
}

void delay(clock_t ms) {
	clock_t goal = ms + clock();
	while (goal > clock());
}

void read_weight(int id) {
	if (id < 0) {
		printf("Input weight's file ID: ");
		scanf("%d", &id);
		getchar();
	}
	char filename[32];
	sprintf(filename, "weight%d.txt", id);
	FILE *file = fopen(filename, "r");
	if (!file) return;
	for (int i = 0; i < BOARD_SIZE; i++) {
		for (int j = 0; j < BOARD_SIZE; j++) {
			int val;
			fscanf(file, "%d", &val);
			board_weight[i][j] = val;
		}
	}
	fclose(file);
}

// open a file and get the next move, for play by file
void read_file(char *input) {
	FILE *file = fopen("of.txt", "r");
	char str[3];
	while ((fscanf(file, "%s", str)) != EOF) {
		input[0] = (char)toupper(str[0]);
		input[1] = str[1];
	}
	// fclose(file);
}

// load a file and start a game
char load_file(void) {
	char input[10];
	int row_input, column_input, n;
	
	FILE *file = fopen("of.txt", "r");
	assert(file != NULL);
	
	fscanf(file, "%d", &n);
	while ((fscanf(file, "%s", input)) != EOF) {
		row_input = toupper(input[0]) - 'A';
		column_input = input[1] - '0';
		if (!play_a_move(row_input, column_input))
			printf("%c%d is a wrong move\n", input[0], 1 + column_input);
		
		show_board_and_set_legal_moves();
	}
	// fclose(file);
	return (n % 2) ? (char)'B' : (char)'W';
}

void init(void) {
	com_take = 0;
	memset(now_board, 0, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
	
	now_board[3][3] = now_board[4][4] = 2; // white, dark
	now_board[3][4] = now_board[4][3] = 1; // black, light
	
	hand_num = 0;
	memset(sequence, -1, sizeof(int) * 100);
	turn = 0;
	
	last_x = last_y = -1;
	black_count = white_count = 0;
	
	// is_comp_thinking = false;
	// debug_value = 0;
	search_counter = 0;
	
	// com_take = 0;
	winner = 0;
}

bool play_a_move(int x, int y) {
	
	if (x == -1 && y == -1) {
		FILE *file = fopen("of.txt", "r+");
		fprintf(file, "%2d\n", hand_num + 1);
		fclose(file);
		
		file = fopen("of.txt", "a");
		fprintf(file, "p9\n");
		fclose(file);
		
		sequence[hand_num] = -1;
		hand_num++;
		turn = 1 - turn;
		return true;
	}
	
	if (!is_in_board(x, y)) return false;
	find_legal_moves(stones[turn]);
	if (!now_board_is_move_legal[x][y])
		return false;
	
	if (put_a_stone(x, y)) {
		is_crossed(x, y, 1);
		compute_grades(true);
		// show_board_and_set_legal_moves();
		// printf("Play %c%d\n", 'A' + x, 1 + y);
		return true;
	}
	return false;
}

bool put_a_stone(int x, int y) {
	if (now_board[x][y] == 0) {
		FILE *file;
		sequence[hand_num] = turn;
		if (hand_num == 0) file = fopen("of.txt", "w");
		else file = fopen("of.txt", "r+");
		fprintf(file, "%2d\n", hand_num + 1);
		hand_num++;
		fclose(file);
		
		now_board[x][y] = stones[turn];
		file = fopen("of.txt", "a");
		fprintf(file, "%c%d\n", 'a' + x, 1 + y);
		fclose(file);
		
		last_x = x;
		last_y = y;
		
		turn = 1 - turn;
		
		return true;
	}
	return false;
}

void show_board_and_set_legal_moves(void) {
	find_legal_moves(stones[turn]);
	printf("A B C D E F G H\n");
	for (int i = 0; i < BOARD_SIZE; i++) {
		for (int j = 0; j < BOARD_SIZE; j++) {
			if (now_board[j][i] > 0) {
				if (now_board[j][i] == 2) printf("O "); // white
				else printf("X "); // black
			}
			
			if (now_board[j][i] == 0) {
				if (now_board_is_move_legal[j][i]) printf("? ");
				else printf(". ");
			}
		}
		printf("%d\n", i + 1);
	}
	printf("\n");
}

int find_legal_moves(int color) {
	int i, j;
	int me = color;
	int legal_count = 0;
	
	for (i = 0; i < BOARD_SIZE; i++)
		for (j = 0; j < BOARD_SIZE; j++)
			now_board_is_move_legal[i][j] = false;
	
	for (i = 0; i < BOARD_SIZE; i++) {
		for (j = 0; j < BOARD_SIZE; j++) {
			if (now_board[i][j] == 0) {
				now_board[i][j] = me;
				if (is_crossed(i, j, false)) {
					now_board_is_move_legal[i][j] = true;
					legal_count++;
				}
				now_board[i][j] = 0;
			}
		}
	}
	return legal_count;
}

bool is_crossed(int x, int y, int update) {
	
	if (!is_in_board(x, y) || now_board[x][y] == 0) return false;
	
	int army = 3 - now_board[x][y], army_count = 0;
	// printf("%d, %d, %d, %d\n", x, y, now_board[x][y], army);
	for (int i = 0; i < 8; i++) {
		int dx = x + dir_x[i], dy = y + dir_y[i];
		if (is_in_board(dx, dy) && now_board[dx][dy] == army) {
			army_count += check_straight_army(x, y, i, update);
			// printf("%d, ", army_count);
		}
	}
	
	return army_count > 0;
}

int check_straight_army(int x, int y, int d, int update) {
	int me = now_board[x][y];
	int army = 3 - me;
	int army_count = 0;
	bool found_flag = false;
	int flag[BOARD_SIZE][BOARD_SIZE] = {{0}};
	
	int tx = x, ty = y;
	for (int i = 0; i < BOARD_SIZE; i++) {
		tx += dir_x[d];
		ty += dir_y[d];
		
		if (is_in_board(tx, ty)) {
			if (now_board[tx][ty] == army) {
				army_count++;
				flag[tx][ty] = true;
			} else if (now_board[tx][ty] == me) {
				found_flag = true;
				break;
			} else break;
		} else break;
	}
	
	if ((found_flag) && (army_count > 0) && update) {
		for (int i = 0; i < BOARD_SIZE; i++) {
			for (int j = 0; j < BOARD_SIZE; j++) {
				if (flag[i][j]) {
					// dead_stone[i][j] = true;
					if (now_board[i][j] != 0)
						now_board[i][j] = 3 - now_board[i][j];
				}
			}
		}
	}
	if ((found_flag) && (army_count > 0)) return army_count;
	else return 0;
}

bool is_in_board(int x, int y) {
	return (x >= 0 && x < BOARD_SIZE) && (y >= 0 && y < BOARD_SIZE);
}

int compute_grades(int flag) {
	int black = 0, white = 0, black_weight = 0, white_weight = 0;
	for (int i = 0; i < BOARD_SIZE; i++) {
		for (int j = 0; j < BOARD_SIZE; j++) {
			if (now_board[i][j] == 1) {
				black++;
				black_weight = black_weight + board_weight[i][j];
			} else if (now_board[i][j] == 2) {
				white++;
				white_weight = white_weight + board_weight[i][j];
			}
		}
	}
	if (flag) {
		black_count = black;
		white_count = white;
		printf("Grade: black %d, white %d\n", black, white);
	}
	
	return black_weight - white_weight;
}

bool is_game_ended(void) {
	int legal_count_2 = find_legal_moves(stones[1 - turn]);
	int legal_count_1 = find_legal_moves(stones[turn]);
	
	if (legal_count_1 == 0 && legal_count_2 == 0) {
		if (black_count > white_count) {
			printf("Black win!\n");
			if (winner == 0) winner = 1;
		} else if (black_count < white_count) {
			printf("White win!\n");
			if (winner == 0) winner = 2;
		} else {
			printf("Draw\n");
			winner = 0;
		}
		show_board_and_set_legal_moves();
		printf("Game is over");
		// scanf("%d", &legal_count_1);
		return true;
	}
	
	return false;
}

void computer_think(int *x, int *y) {
	static int think_time = 0;
	
	time_t clock_start = clock(), clock_end;
	
	result_x = result_y = -1;
	search_counter = 0;
	
	int flag = search(turn, 0);
	
	clock_end = clock();
	think_time += clock_end - clock_start;
	printf(
		"Used thinking time %d min %d.%d sec.\n",
		think_time / 60000,
		(think_time % 60000) / 1000,
		(think_time % 60000) % 1000
	);
	
	if (flag) {
		*x = result_x;
		*y = result_y;
	} else *x = *y = -1;
}

// minimax search
bool search(int my_turn, int my_level) {
	loc min, max;
	
	min.i = min.j = -1;
	min.g = INT_MAX;
	
	max.i = max.j = -1;
	max.g = INT_MIN;
	
	int board[BOARD_SIZE][BOARD_SIZE];
	bool board_is_move_legal[BOARD_SIZE][BOARD_SIZE];
	
	memcpy(board, now_board, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
	// search_level_now = 0;
	
	int c = find_legal_moves(stones[my_turn]);
	if (c <= 0) return false;
	
	memcpy(
		board_is_move_legal, now_board_is_move_legal,
		sizeof(bool) * BOARD_SIZE * BOARD_SIZE
	);
	
	int alpha = INT_MIN, beta = INT_MAX, g;
	for (int i = 0; i < BOARD_SIZE; i++)
		for (int j = 0; j < BOARD_SIZE; j++)
			if (board_is_move_legal[i][j]) { // you could add move ordering
				memcpy(now_board, board, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
				now_board[i][j] = stones[my_turn];
				is_crossed(i, j, true);
				
				g = search_next(i, j, 1 - my_turn, my_level + 1, alpha, beta);
				
				if (my_turn == 0)  // max level
					if (g > max.g) {
						max.g = g;
						max.i = i;
						max.j = j;
					}
				
				if (my_turn == 1) {
					if (g < min.g) {
						min.g = g;
						min.i = i;
						min.j = j;
					}
				}
				/* if(alpha_beta_option) {
					if(alpha >= beta) {
						i = BOARD_SIZE;
						j = BOARD_SIZE;
					}
				} */
			}
	
	memcpy(now_board, board, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
	
	if (my_turn == 0) {
		result_x = max.i;
		result_y = max.j;
		return true;
	} else if (my_turn == 1) {
		result_x = min.i;
		result_y = min.j;
		return true;
	}
	return false;
}

int search_next(int x, int y, int my_turn, int my_level, int alpha, int beta) {
	search_counter++;
	
	int g;
	if (my_level >= search_deep) {
		g = compute_grades(false);
		return g;
	} else {
		/// int my_alpha = alpha; int my_beta = beta;
		// loc min; min.i = -1; min.j = -1; min.g = INT_MAX;
		// loc max; max.i = -1; max.i = -1; max.g = INT_MIN;
		
		int board[BOARD_SIZE][BOARD_SIZE];
		bool board_is_move_legal[BOARD_SIZE][BOARD_SIZE];
		
		int c = find_legal_moves(stones[my_turn]);
		if (c <= 0) {
			g = compute_grades(false);
			return g;
		}
		
		memcpy(board, now_board, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
		memcpy(
			board_is_move_legal, now_board_is_move_legal,
			sizeof(bool) * BOARD_SIZE * BOARD_SIZE
		);
		
		for (int i = 0; i < BOARD_SIZE; i++)
			for (int j = 0; j < BOARD_SIZE; j++)
				if (board_is_move_legal[i][j]) { // you could add move ordering
					memcpy(
						now_board, board,
						sizeof(int) * BOARD_SIZE * BOARD_SIZE
					);
					now_board[i][j] = stones[my_turn];
					is_crossed(i, j, true);
					
					g = search_next(
						i, j, 1 - my_turn, my_level + 1, alpha, beta
					); // could use transposition table
					
					if (my_turn == 0) { // max ply
						if (g > alpha) alpha = g;
					} else if (my_turn == 1) { // min ply
						if (g < beta) beta = g;
					}
					
					if (alpha_beta_option) {
						if (alpha >= beta) { // cutoff
							i = BOARD_SIZE;
							j = BOARD_SIZE;
							break;
						}
					}
				}
		
		memcpy(now_board, board, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
		
		if (my_turn == 0) /* max level */ return alpha; //max.g;
		else return beta; //min.g;
	}
}
