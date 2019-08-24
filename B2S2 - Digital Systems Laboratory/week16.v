module main(input clr, pause, clk, output [6:0] seg1, seg2);
	wire [3:0] div6, div10;
	wire clr6, clr10;
	assign clr6= ~((~div6[3]) & div6[2] & div6[1] & (~div6[0]));
	assign clr10= ~(div10[3] & (~div10[2]) & div10[1] & (~div10[0]));
	wire oclk;
	freq_div(clk, oclk);
	four_bit_up_counter(clr10, clr6 & clr, div6);
	four_bit_up_counter(oclk & pause, clr10 & clr, div10);
	seven_seg(div10, seg1);
	seven_seg(div6, seg2);
endmodule

module four_bit_up_counter(input clk, clr, output [3:0] out);
	jk_flip_flop(clk, clr, 1'b1, 1'b1, out[0]);
	jk_flip_flop(out[0], clr, 1'b1, 1'b1, out[1]);
	jk_flip_flop(out[1], clr, 1'b1, 1'b1, out[2]);
	jk_flip_flop(out[2], clr, 1'b1, 1'b1, out[3]);
endmodule

module freq_div(input iclk, output reg oclk);
	integer count;
	initial count = 0;
	always @(posedge iclk) begin
		if(count < 6000 / 2) oclk = 1;
		else oclk = 0;
		count = (count + 1) % 6000;
	end
endmodule

module jk_flip_flop(input clk, clr, j, k, output reg q);
	always @(negedge clk or negedge clr) begin
		if(~clr) q = 0;
		else begin
			case({ j, k })
				2'b00: q = q;
				2'b01: q = 0;
				2'b10: q = 1;
				2'b11: q = ~q;
			endcase
		end
	end
endmodule
