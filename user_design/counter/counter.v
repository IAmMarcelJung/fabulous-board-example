module top(input wire clk, input wire [23:0] io_in, output wire [23:0] io_out, io_oeb);
wire rst = io_in[0];
reg [23:0] ctr;
reg [15:0] prescale;
localparam PRESCALE_LIMIT = 1000;

always @(posedge clk) begin
    if (rst)
        ctr <= 0;
    else begin
        //if (prescale == PRESCALE_LIMIT)
        ctr <= ctr + 1'b1;
    end
end

always @(posedge clk) begin
    if (rst)
        prescale <= 0;
    else begin
        if (prescale == PRESCALE_LIMIT)
            prescale <= 0;
        else
            prescale <= prescale + 1'b1;
    end
end

assign io_out[23:1] = ctr[23:1]; // pass thru reset for debugging
assign io_oeb = ~(24'b1);
endmodule
