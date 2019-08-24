module main(input is_johnson, clk, rst, ld, input [4:0] in, output [4:0] out);
	johnson_or_ring_counter_5bit (is_johnson, clk, rst, ld, in, out);
endmodule

module d_flip_flop(input clk, rst, d, output reg q, nq);
	always @(posedge(clk) or negedge(rst))
	begin
		if (~rst)
			q = 0;
		else
			q = d;
		nq = ~q;
	end
endmodule

module johnson_or_ring_counter_5bit(input is_johnson, clk, rst, ld, input [4:0] in, output [4:0] q);
	wire [4:0] nq;
	reg [4:0] prev;
	always @(negedge(clk))
	begin
		prev = q;
		if (is_johnson == 1)
			prev[4] = nq[4];
		if (ld == 1)
			prev = { in[0], in[4:1] };
	end
	d_flip_flop (clk, rst, prev[4], q[0], nq[0]),
		(clk, rst, prev[0], q[1], nq[1]),
		(clk, rst, prev[1], q[2], nq[2]),
		(clk, rst, prev[2], q[3], nq[3]),
		(clk, rst, prev[3], q[4], nq[4]);
endmodule
