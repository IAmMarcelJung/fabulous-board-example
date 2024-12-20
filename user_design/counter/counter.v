module top (
    input wire clk,
    input wire [23:0] io_in,
    output wire [23:0] io_out,
    io_oeb
);

    localparam COUNTER_WIDTH = 24;
    localparam PRESCALE_WIDTH = 16;
    wire rst;
    wire use_prescaler;
    reg [COUNTER_WIDTH-1:0] ctr;
    reg [PRESCALE_WIDTH-1:0] prescale;
    localparam PRESCALE_LIMIT = 10;

    always @(posedge clk) begin
        if (rst) ctr <= 0;
        else begin
            if (use_prescaler) begin
                if (prescale == PRESCALE_LIMIT) ctr <= ctr + 1'b1;
            end else begin
                ctr <= ctr + 1'b1;
            end
        end
    end

    always @(posedge clk) begin
        if (rst) prescale <= 0;
        else begin
            if (prescale == PRESCALE_LIMIT) prescale <= 0;
            else prescale <= prescale + 1'b1;
        end
    end

    // assign io_out[19:6] = {7{ctr[21], ctr[20]}};
    assign io_out[19:6] = {7{ctr[19], ctr[18]}};
    assign io_out[3:0] = {2{ctr[19], ctr[18]}};

    // Route the rst through for debugging
    assign io_out[20] = rst;

    assign use_prescaler = io_in[21];

    // use io_in (IO[37] for the Nucleo reset and io_in[22] as a reset which can
    // be connected to e.g. a button
    assign rst = io_in[23] | io_in[22];

    // Disable the output for the pins mapped to IO 18 and 19, since their configuration will be
    // random
    // IO 37 to 35 are configured as input only, therefore also disable the
    // output
    assign io_oeb = ~(24'b111000000010000000110000);
endmodule
