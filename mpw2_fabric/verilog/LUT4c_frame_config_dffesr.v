// Copyright 2021 University of Manchester
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

module LUT4c_frame_config (
    I0,
    I1,
    I2,
    I3,
    O,
    Ci,
    Co,
    SR,
    EN,
    UserCLK,
    ConfigBits
);
  parameter NoConfigBits = 19 ; // has to be adjusted manually (we don't use an arithmetic parser for the value)
  // IMPORTANT: this has to be in a dedicated line
  input I0;  // LUT inputs
  input I1;
  input I2;
  input I3;
  output O;  // LUT output (combinatorial or FF)
  input Ci;  // carry chain input
  output Co;  // carry chain output
  input SR;  // SHARED_RESET
  input EN;  // SHARED_ENABLE
  input UserCLK; // EXTERNAL // SHARED_PORT // ## the EXTERNAL keyword will send this sisgnal all the way to top and the //SHARED Allows multiple BELs using the same port (e.g. for exporting a clock to the top)
  // GLOBAL all primitive pins that are connected to the switch matrix have to go before the GLOBAL label
  input [NoConfigBits-1 : 0] ConfigBits;

  localparam LUT_SIZE = 4;
  localparam N_LUT_flops = 2 ** LUT_SIZE;

  wire [N_LUT_flops-1 : 0] LUT_values;
  wire [LUT_SIZE-1 : 0] LUT_index;
  wire LUT_out;
  reg LUT_flop;
  wire I0mux;  // normal input '0', or carry input '1'
  wire c_out_mux, c_I0mux, c_reset_value;  // extra configuration bits

  assign LUT_values = ConfigBits[15:0];
  assign c_out_mux = ConfigBits[16];
  assign c_I0mux = ConfigBits[17];
  assign c_reset_value = ConfigBits[18];


  //assign I0mux = c_I0mux ? Ci : I0;
  my_mux2 my_mux2_I0mux (
      .A0(I0),
      .A1(Ci),
      .S (c_I0mux),
      .X (I0mux)
  );

  assign LUT_index = {I3, I2, I1, I0mux};

  cus_mux161_buf inst_cus_mux161_buf (
      .A0 (LUT_values[0]),
      .A1 (LUT_values[1]),
      .A2 (LUT_values[2]),
      .A3 (LUT_values[3]),
      .A4 (LUT_values[4]),
      .A5 (LUT_values[5]),
      .A6 (LUT_values[6]),
      .A7 (LUT_values[7]),
      .A8 (LUT_values[8]),
      .A9 (LUT_values[9]),
      .A10(LUT_values[10]),
      .A11(LUT_values[11]),
      .A12(LUT_values[12]),
      .A13(LUT_values[13]),
      .A14(LUT_values[14]),
      .A15(LUT_values[15]),
      .S0 (LUT_index[0]),
      .S0N(~LUT_index[0]),
      .S1 (LUT_index[1]),
      .S1N(~LUT_index[1]),
      .S2 (LUT_index[2]),
      .S2N(~LUT_index[2]),
      .S3 (LUT_index[3]),
      .S3N(~LUT_index[3]),
      .X  (LUT_out)
  );

  my_mux2 my_mux2_O (
      .A0(LUT_out),
      .A1(LUT_flop),
      .S (c_out_mux),
      .X (O)
  );

  assign Co = (Ci & I1) | (Ci & I2) | (I1 & I2);// iCE40 like carry chain (as this is supported in Yosys; would normally go for fractured LUT

  always @(posedge UserCLK) begin
    if (EN) begin
      if (SR) LUT_flop <= c_reset_value;
      else LUT_flop <= LUT_out;
    end
  end

endmodule
