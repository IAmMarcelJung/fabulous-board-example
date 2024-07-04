module top(input wire clk, input wire [30:0] io_in, output wire [30:0] io_out, io_oeb);
wire rst = io_in[0];
reg [23:0] ctr;
reg [15:0] prescale;
localparam PRESCALE_LIMIT = 1000;
localparam ENABLE_PRESCALER = 0;

always @(posedge clk) begin
    if (rst)
        ctr <= 0;
    else begin
        if (prescale == PRESCALE_LIMIT && ENABLE_PRESCALER == 1)
        ctr <= ctr + 1'b1;
    end
end

always @(posedge clk) begin
    if (rst)
        prescale <= 0;
    else begin
        if (prescale >= PRESCALE_LIMIT)
            prescale <= 0;
        else
            prescale <= prescale + 1'b1;
    end
end

assign io_out[30:1] = {6'h3F, ctr[23:1]}; // pass thru reset for debugging
assign io_oeb = ~(28'b1);
endmodule
