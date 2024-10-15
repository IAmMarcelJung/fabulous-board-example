module top (
    input wire clk,
    input wire [23:0] io_in,
    output wire [23:0] io_out,
    io_oeb
);
    wire rst;

    reg [23:0] ctr;
    reg [15:0] prescale;
    localparam PRESCALE_LIMIT = 6;

    always @(posedge clk) begin
        if (rst) ctr <= 0;
        else begin
            if (prescale == PRESCALE_LIMIT) ctr <= ctr + 1'b1;
        end
    end

    always @(posedge clk) begin
        if (rst) prescale <= 0;
        else begin
            if (prescale == PRESCALE_LIMIT) prescale <= 0;
            else prescale <= prescale + 1'b1;
        end
    end

    assign io_out[21:0] = ctr[21:0];
    assign io_out[22] = rst;
    assign rst = io_in[23];
    assign io_oeb = ~(24'b100000000000000000000000);
endmodule
