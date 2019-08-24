module main(input [8:0] dec_in, input [2:0] three_in, input [3:0] four_in,
		output [6:0] seg_out, output three_or_out, output [15:0] four_out);
	wire [3:0] dec_out;
	wire [7:0] three_out;
	dec_to_bcd(dec_in, dec_out);
	seven_seg(dec_out, seg_out);
	three_to_eight(1, three_in, three_out);
	assign three_or_out = three_out[0] | three_out[2] | three_out[4] | three_out[6];
	four_to_sixteen(1, four_in, four_out);
endmodule

module dec_to_bcd(input [8:0] in, output reg [3:0] out);
	always @(in) begin
		case (in)
			9'b000000000: out = 4'b0000;
			9'b000000001: out = 4'b0001;
			9'b000000010: out = 4'b0010;
			9'b000000100: out = 4'b0011;
			9'b000001000: out = 4'b0100;
			9'b000010000: out = 4'b0101;
			9'b000100000: out = 4'b0110;
			9'b001000000: out = 4'b0111;
			9'b010000000: out = 4'b1000;
			9'b100000000: out = 4'b1001;
			default: out = 4'b1111;
		endcase
	end
endmodule

module three_to_eight(input en, input [2:0] in, output reg [7:0] out);
	always @(in) begin
		if (en) begin
			case (in)
				3'b000: out = 8'b00000001;
				3'b001: out = 8'b00000010;
				3'b010: out = 8'b00000100;
				3'b011: out = 8'b00001000;
				3'b100: out = 8'b00010000;
				3'b101: out = 8'b00100000;
				3'b110: out = 8'b01000000;
				3'b111: out = 8'b10000000;
			endcase
		end else out = 8'b00000000;
	end
endmodule

module four_to_sixteen(input en, input [3:0] in, output [15:0] out);
	three_to_eight tte1(en & ~in[3], in[2:0], out[7:0]);
	three_to_eight tte2(en & in[3], in[2:0], out[15:8]);
endmodule
