module main(input [3:0] i1, i2, output c, output [6:0] seg);
	wire [3:0] o;
	four_bit_suber(i1, i2, c, o);
	seven_seg(o, seg);
endmodule

module four_bit_suber(input [3:0] i1, i2, output c, output [3:0] o);
	wire [3:0] o1;
	wire nc, unuse_c;
	four_bit_ripple_adder(i1, { i2[3] ^ 1'b1, i2[2] ^ 1'b1, i2[1] ^ 1'b1, i2[0] ^ 1'b1 }, 1'b1, o1, nc);
	assign c = ~nc;
	four_bit_ripple_adder(4'b0000, { o1[3] ^ c, o1[2] ^ c, o1[1] ^ c, o1[0] ^ c }, c, o, unuse_c);
endmodule
