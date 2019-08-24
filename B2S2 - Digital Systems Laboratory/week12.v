module half_adder(input i1, i2, output s, co);
	assign s = i1 ^ i2;
	assign co = i1 & i2;
endmodule

module full_adder(input i1, i2, ci, output s, co);
	wire [1:0] c;
	wire s1;
	half_adder ha1(i1, i2, s1, c[0]);
	half_adder ha2(ci, s1, s, c[1]);
	assign co = c[0] | c[1];
endmodule

module four_bit_ripple_adder(input [3:0] i1, i2, input ci, output [3:0] s, output co);
	wire [2:0] c;
	full_adder fa1(i1[0], i2[0], ci, s[0], c[0]);
	full_adder fa2(i1[1], i2[1], c[0], s[1], c[1]);
	full_adder fa3(i1[2], i2[2], c[1], s[2], c[2]);
	full_adder fa4(i1[3], i2[3], c[2], s[3], co);
endmodule

module main(input [3:0] i1, i2, input ci, output [6:0] seg, output co);
	wire [3:0] s;
	four_bit_ripple_adder fra(i1, i2, ci, s, co);
	seven_seg sseg(s, seg);
endmodule
