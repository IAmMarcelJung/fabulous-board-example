module top(input wire clk, input wire [30:0] io_in, output wire [30:0] io_out, io_oeb);
	wire rst = io_in[0];
	reg [15:0] out;

    /*
	always @(posedge clk)
		if (rst)
			ctr <= 0;
		else
			ctr <= ctr + 1'b1;
    */

    always @(posedge clk)
		if (rst)
            out <= 0;
        else
            out = {22{io_in[1]}};

	assign io_out = out;
	assign io_oeb = ~(28'b1);
endmodule
