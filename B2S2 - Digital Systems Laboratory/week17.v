module main(input clr, clk, input [7:0] i, output data, output [2:0] sel);
	wire [3:0] div8;
	wire oclk;
	assign sel = div8[2:0];
	freq_div(clk, oclk);
	four_bit_up_counter(oclk, ~div8[3] & clr, div8);
	eight_to_one_muxer(i, sel, data);
endmodule

module eight_to_one_muxer(input [7:0] i, input [2:0] s, output o);
	wire [3:0] t0;
	wire [1:0] t1;
	two_to_one_muxer(i[1:0], s[0], t0[0]);
	two_to_one_muxer(i[3:2], s[0], t0[1]);
	two_to_one_muxer(i[5:4], s[0], t0[2]);
	two_to_one_muxer(i[7:6], s[0], t0[3]);
	two_to_one_muxer(t0[1:0], s[1], t1[0]);
	two_to_one_muxer(t0[3:2], s[1], t1[1]);
	two_to_one_muxer(t1[1:0], s[2], o);
endmodule

module two_to_one_muxer(input [1:0] i, input s, output reg o);
	always @(i) begin
		if ((s == 0 & i[0] == 1) | (s == 1 & i[1] == 1)) o = 1;
		else o = 0;
	end
endmodule
