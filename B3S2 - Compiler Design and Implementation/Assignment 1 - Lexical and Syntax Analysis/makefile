BUILD_DIR := build
DIST_DIR := dist

start: prepare $(BUILD_DIR)/pascal_parser

prepare:
	mkdir -p $(BUILD_DIR) $(DIST_DIR)

$(BUILD_DIR)/pascal_parser: $(DIST_DIR)/main.o $(DIST_DIR)/pascal_lex.o $(DIST_DIR)/pascal_yacc.o
	gcc -o $@ $?

$(DIST_DIR)/pascal_lex.o: $(DIST_DIR)/pascal_lex.c $(DIST_DIR)/pascal_yacc.h $(DIST_DIR)/pascal_parser.h
	gcc -o $@ -c $<

$(DIST_DIR)/pascal_yacc.o: $(DIST_DIR)/pascal_yacc.c $(DIST_DIR)/pascal_parser.h
	gcc -o $@ -c $<

$(DIST_DIR)/main.o: $(DIST_DIR)/main.c $(DIST_DIR)/pascal_yacc.h $(DIST_DIR)/pascal_parser.h
	gcc -o $@ -c $<

$(DIST_DIR)/pascal_lex.c: pascal_lex.l
	lex -o $@ $<

$(DIST_DIR)/pascal_yacc.h: $(DIST_DIR)/pascal_yacc.c

$(DIST_DIR)/pascal_yacc.c: $(DIST_DIR)/pascal_yacc.y
	yacc -d -o $@ $<

$(DIST_DIR)/pascal_yacc.y: pascal_yacc.y
	go run msg_maker.go $< $@

$(DIST_DIR)/pascal_parser.h: pascal_parser.h
	cp $< $@

$(DIST_DIR)/main.c: main.c
	cp $< $@

clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR)
