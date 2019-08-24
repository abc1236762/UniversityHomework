module myProject(sw, hex, led);
	input [3:0] sw;
	output [6:0] hex, led;
	myDecoder dec1(sw, hex);
	myDecoder dec2(sw, led);
endmodule

module myDecoder(intVal, outSeg);
	input [3:0] intVal;
	output reg [6:0] outSeg;
	always @(intVal)
	begin
		case (intVal)
			4'b0000: outSeg = 7'b1000000;
			4'b0001: outSeg = 7'b1111001;
			4'b0010: outSeg = 7'b0100100;
			4'b0011: outSeg = 7'b0110000;
			4'b0100: outSeg = 7'b0011001;
			4'b0101: outSeg = 7'b0010010;
			4'b0110: outSeg = 7'b0000010;
			4'b0111: outSeg = 7'b1111000;
			4'b1000: outSeg = 7'b0000000;
			4'b1001: outSeg = 7'b0011000;
			4'b1010: outSeg = 7'b0001000;
			4'b1011: outSeg = 7'b0000011;
			4'b1100: outSeg = 7'b1000110;
			4'b1101: outSeg = 7'b0100001;
			4'b1110: outSeg = 7'b0000110;
			4'b1111: outSeg = 7'b0001110;
		endcase
	end
endmodule