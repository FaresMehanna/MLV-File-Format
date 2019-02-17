/* Machine-generated using Migen */
module top(
	input [11:0] pixels_input,
	input [11:0] pixels_input_1,
	input [11:0] pixels_input_2,
	input [11:0] pixels_input_3,
	input [11:0] pixels_input_4,
	input [11:0] pixels_input_5,
	input [11:0] pixels_input_6,
	input [11:0] pixels_input_7,
	input [11:0] pixels_input_8,
	input [11:0] pixels_input_9,
	input [11:0] pixels_input_10,
	input [11:0] pixels_input_11,
	input [11:0] pixels_input_12,
	input [11:0] pixels_input_13,
	input [11:0] pixels_input_14,
	input [11:0] pixels_input_15,
	input input_valid,
	input pause_signal,
	input end_in,
	input multi_row_mode,
	input new_row,
	input [11:0] cached_pixels_input,
	input [11:0] cached_pixels_input_1,
	input [11:0] cached_pixels_input_2,
	input [11:0] cached_pixels_input_3,
	input [11:0] cached_pixels_input_4,
	input [11:0] cached_pixels_input_5,
	input [11:0] cached_pixels_input_6,
	input [11:0] cached_pixels_input_7,
	input [11:0] cached_pixels_input_8,
	input [11:0] cached_pixels_input_9,
	input [11:0] cached_pixels_input_10,
	input [11:0] cached_pixels_input_11,
	input [11:0] cached_pixels_input_12,
	input [11:0] cached_pixels_input_13,
	input [11:0] cached_pixels_input_14,
	input [11:0] cached_pixels_input_15,
	output signed [13:0] diff_output_pixels,
	output signed [13:0] diff_output_pixels_1,
	output signed [13:0] diff_output_pixels_2,
	output signed [13:0] diff_output_pixels_3,
	output signed [13:0] diff_output_pixels_4,
	output signed [13:0] diff_output_pixels_5,
	output signed [13:0] diff_output_pixels_6,
	output signed [13:0] diff_output_pixels_7,
	output signed [13:0] diff_output_pixels_8,
	output signed [13:0] diff_output_pixels_9,
	output signed [13:0] diff_output_pixels_10,
	output signed [13:0] diff_output_pixels_11,
	output signed [13:0] diff_output_pixels_12,
	output signed [13:0] diff_output_pixels_13,
	output signed [13:0] diff_output_pixels_14,
	output signed [13:0] diff_output_pixels_15,
	output output_valid,
	output end_out,
	input sys_clk,
	input sys_rst
);

wire [11:0] pred1_pixels_input0;
wire [11:0] pred1_pixels_input1;
wire [11:0] pred1_pixels_input2;
wire [11:0] pred1_pixels_input3;
wire [11:0] pred1_pixels_input4;
wire [11:0] pred1_pixels_input5;
wire [11:0] pred1_pixels_input6;
wire [11:0] pred1_pixels_input7;
wire [11:0] pred1_pixels_input8;
wire [11:0] pred1_pixels_input9;
wire [11:0] pred1_pixels_input10;
wire [11:0] pred1_pixels_input11;
wire [11:0] pred1_pixels_input12;
wire [11:0] pred1_pixels_input13;
wire [11:0] pred1_pixels_input14;
wire [11:0] pred1_pixels_input15;
wire pred1_input_valid;
wire pred1_pause_signal;
wire pred1_end_in;
wire pred1_multi_row_mode;
wire pred1_new_row;
wire [11:0] pred1_cached_pixels_input0;
wire [11:0] pred1_cached_pixels_input1;
wire [11:0] pred1_cached_pixels_input2;
wire [11:0] pred1_cached_pixels_input3;
wire [11:0] pred1_cached_pixels_input4;
wire [11:0] pred1_cached_pixels_input5;
wire [11:0] pred1_cached_pixels_input6;
wire [11:0] pred1_cached_pixels_input7;
wire [11:0] pred1_cached_pixels_input8;
wire [11:0] pred1_cached_pixels_input9;
wire [11:0] pred1_cached_pixels_input10;
wire [11:0] pred1_cached_pixels_input11;
wire [11:0] pred1_cached_pixels_input12;
wire [11:0] pred1_cached_pixels_input13;
wire [11:0] pred1_cached_pixels_input14;
wire [11:0] pred1_cached_pixels_input15;
reg [11:0] pred1_pixels_output0 = 12'd0;
reg [11:0] pred1_pixels_output1 = 12'd0;
reg [11:0] pred1_pixels_output2 = 12'd0;
reg [11:0] pred1_pixels_output3 = 12'd0;
reg [11:0] pred1_pixels_output4 = 12'd0;
reg [11:0] pred1_pixels_output5 = 12'd0;
reg [11:0] pred1_pixels_output6 = 12'd0;
reg [11:0] pred1_pixels_output7 = 12'd0;
reg [11:0] pred1_pixels_output8 = 12'd0;
reg [11:0] pred1_pixels_output9 = 12'd0;
reg [11:0] pred1_pixels_output10 = 12'd0;
reg [11:0] pred1_pixels_output11 = 12'd0;
reg [11:0] pred1_pixels_output12 = 12'd0;
reg [11:0] pred1_pixels_output13 = 12'd0;
reg [11:0] pred1_pixels_output14 = 12'd0;
reg [11:0] pred1_pixels_output15 = 12'd0;
reg signed [13:0] pred1_pred_output_pixels0 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels1 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels2 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels3 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels4 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels5 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels6 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels7 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels8 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels9 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels10 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels11 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels12 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels13 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels14 = 14'sd0;
reg signed [13:0] pred1_pred_output_pixels15 = 14'sd0;
reg pred1_output_valid = 1'd0;
reg pred1_end_out = 1'd0;
reg pred1_multi_row_mode_out = 1'd0;
reg pred1_new_row_out = 1'd1;
reg [12:0] pred1_cached_left_pixel = 13'd4096;
reg [11:0] pred1_cached_top_left_pixel = 12'd0;
wire [11:0] pred2_pixels_input0;
wire [11:0] pred2_pixels_input1;
wire [11:0] pred2_pixels_input2;
wire [11:0] pred2_pixels_input3;
wire [11:0] pred2_pixels_input4;
wire [11:0] pred2_pixels_input5;
wire [11:0] pred2_pixels_input6;
wire [11:0] pred2_pixels_input7;
wire [11:0] pred2_pixels_input8;
wire [11:0] pred2_pixels_input9;
wire [11:0] pred2_pixels_input10;
wire [11:0] pred2_pixels_input11;
wire [11:0] pred2_pixels_input12;
wire [11:0] pred2_pixels_input13;
wire [11:0] pred2_pixels_input14;
wire [11:0] pred2_pixels_input15;
wire pred2_input_valid;
wire pred2_pause_signal;
wire pred2_end_in;
wire pred2_multi_row_mode;
wire signed [13:0] pred2_pred_input_pixels0;
wire signed [13:0] pred2_pred_input_pixels1;
wire signed [13:0] pred2_pred_input_pixels2;
wire signed [13:0] pred2_pred_input_pixels3;
wire signed [13:0] pred2_pred_input_pixels4;
wire signed [13:0] pred2_pred_input_pixels5;
wire signed [13:0] pred2_pred_input_pixels6;
wire signed [13:0] pred2_pred_input_pixels7;
wire signed [13:0] pred2_pred_input_pixels8;
wire signed [13:0] pred2_pred_input_pixels9;
wire signed [13:0] pred2_pred_input_pixels10;
wire signed [13:0] pred2_pred_input_pixels11;
wire signed [13:0] pred2_pred_input_pixels12;
wire signed [13:0] pred2_pred_input_pixels13;
wire signed [13:0] pred2_pred_input_pixels14;
wire signed [13:0] pred2_pred_input_pixels15;
wire pred2_new_row;
reg [11:0] pred2_pixels_output0 = 12'd0;
reg [11:0] pred2_pixels_output1 = 12'd0;
reg [11:0] pred2_pixels_output2 = 12'd0;
reg [11:0] pred2_pixels_output3 = 12'd0;
reg [11:0] pred2_pixels_output4 = 12'd0;
reg [11:0] pred2_pixels_output5 = 12'd0;
reg [11:0] pred2_pixels_output6 = 12'd0;
reg [11:0] pred2_pixels_output7 = 12'd0;
reg [11:0] pred2_pixels_output8 = 12'd0;
reg [11:0] pred2_pixels_output9 = 12'd0;
reg [11:0] pred2_pixels_output10 = 12'd0;
reg [11:0] pred2_pixels_output11 = 12'd0;
reg [11:0] pred2_pixels_output12 = 12'd0;
reg [11:0] pred2_pixels_output13 = 12'd0;
reg [11:0] pred2_pixels_output14 = 12'd0;
reg [11:0] pred2_pixels_output15 = 12'd0;
reg signed [13:0] pred2_pred_output_pixels0 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels1 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels2 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels3 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels4 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels5 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels6 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels7 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels8 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels9 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels10 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels11 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels12 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels13 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels14 = 14'sd0;
reg signed [13:0] pred2_pred_output_pixels15 = 14'sd0;
reg pred2_output_valid = 1'd0;
reg pred2_end_out = 1'd0;
reg [11:0] pred2_cached_left_pixel = 12'd2048;
wire [11:0] diff_pixels_input0;
wire [11:0] diff_pixels_input1;
wire [11:0] diff_pixels_input2;
wire [11:0] diff_pixels_input3;
wire [11:0] diff_pixels_input4;
wire [11:0] diff_pixels_input5;
wire [11:0] diff_pixels_input6;
wire [11:0] diff_pixels_input7;
wire [11:0] diff_pixels_input8;
wire [11:0] diff_pixels_input9;
wire [11:0] diff_pixels_input10;
wire [11:0] diff_pixels_input11;
wire [11:0] diff_pixels_input12;
wire [11:0] diff_pixels_input13;
wire [11:0] diff_pixels_input14;
wire [11:0] diff_pixels_input15;
wire diff_input_valid;
wire diff_pause_signal;
wire diff_end_in;
wire signed [13:0] diff_pred_input_pixels0;
wire signed [13:0] diff_pred_input_pixels1;
wire signed [13:0] diff_pred_input_pixels2;
wire signed [13:0] diff_pred_input_pixels3;
wire signed [13:0] diff_pred_input_pixels4;
wire signed [13:0] diff_pred_input_pixels5;
wire signed [13:0] diff_pred_input_pixels6;
wire signed [13:0] diff_pred_input_pixels7;
wire signed [13:0] diff_pred_input_pixels8;
wire signed [13:0] diff_pred_input_pixels9;
wire signed [13:0] diff_pred_input_pixels10;
wire signed [13:0] diff_pred_input_pixels11;
wire signed [13:0] diff_pred_input_pixels12;
wire signed [13:0] diff_pred_input_pixels13;
wire signed [13:0] diff_pred_input_pixels14;
wire signed [13:0] diff_pred_input_pixels15;
reg signed [13:0] diff_diff_output_pixels0 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels1 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels2 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels3 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels4 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels5 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels6 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels7 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels8 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels9 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels10 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels11 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels12 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels13 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels14 = 14'sd0;
reg signed [13:0] diff_diff_output_pixels15 = 14'sd0;
reg diff_output_valid = 1'd0;
reg diff_end_out = 1'd0;


// Adding a dummy event (using a dummy signal 'dummy_s') to get the simulator
// to run the combinatorial process once at the beginning.
// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign {pred1_pixels_input15, pred1_pixels_input14, pred1_pixels_input13, pred1_pixels_input12, pred1_pixels_input11, pred1_pixels_input10, pred1_pixels_input9, pred1_pixels_input8, pred1_pixels_input7, pred1_pixels_input6, pred1_pixels_input5, pred1_pixels_input4, pred1_pixels_input3, pred1_pixels_input2, pred1_pixels_input1, pred1_pixels_input0} = {pixels_input_15, pixels_input_14, pixels_input_13, pixels_input_12, pixels_input_11, pixels_input_10, pixels_input_9, pixels_input_8, pixels_input_7, pixels_input_6, pixels_input_5, pixels_input_4, pixels_input_3, pixels_input_2, pixels_input_1, pixels_input};
assign pred1_input_valid = input_valid;
assign pred1_pause_signal = pause_signal;
assign pred1_end_in = end_in;
assign pred1_multi_row_mode = multi_row_mode;
assign pred1_new_row = new_row;
assign {pred1_cached_pixels_input15, pred1_cached_pixels_input14, pred1_cached_pixels_input13, pred1_cached_pixels_input12, pred1_cached_pixels_input11, pred1_cached_pixels_input10, pred1_cached_pixels_input9, pred1_cached_pixels_input8, pred1_cached_pixels_input7, pred1_cached_pixels_input6, pred1_cached_pixels_input5, pred1_cached_pixels_input4, pred1_cached_pixels_input3, pred1_cached_pixels_input2, pred1_cached_pixels_input1, pred1_cached_pixels_input0} = {cached_pixels_input_15, cached_pixels_input_14, cached_pixels_input_13, cached_pixels_input_12, cached_pixels_input_11, cached_pixels_input_10, cached_pixels_input_9, cached_pixels_input_8, cached_pixels_input_7, cached_pixels_input_6, cached_pixels_input_5, cached_pixels_input_4, cached_pixels_input_3, cached_pixels_input_2, cached_pixels_input_1, cached_pixels_input};
assign {pred2_pixels_input15, pred2_pixels_input14, pred2_pixels_input13, pred2_pixels_input12, pred2_pixels_input11, pred2_pixels_input10, pred2_pixels_input9, pred2_pixels_input8, pred2_pixels_input7, pred2_pixels_input6, pred2_pixels_input5, pred2_pixels_input4, pred2_pixels_input3, pred2_pixels_input2, pred2_pixels_input1, pred2_pixels_input0} = {pred1_pixels_output15, pred1_pixels_output14, pred1_pixels_output13, pred1_pixels_output12, pred1_pixels_output11, pred1_pixels_output10, pred1_pixels_output9, pred1_pixels_output8, pred1_pixels_output7, pred1_pixels_output6, pred1_pixels_output5, pred1_pixels_output4, pred1_pixels_output3, pred1_pixels_output2, pred1_pixels_output1, pred1_pixels_output0};
assign pred2_new_row = pred1_new_row_out;
assign pred2_input_valid = pred1_output_valid;
assign pred2_pause_signal = pause_signal;
assign pred2_end_in = pred1_end_out;
assign pred2_multi_row_mode = pred1_multi_row_mode_out;
assign {pred2_pred_input_pixels15, pred2_pred_input_pixels14, pred2_pred_input_pixels13, pred2_pred_input_pixels12, pred2_pred_input_pixels11, pred2_pred_input_pixels10, pred2_pred_input_pixels9, pred2_pred_input_pixels8, pred2_pred_input_pixels7, pred2_pred_input_pixels6, pred2_pred_input_pixels5, pred2_pred_input_pixels4, pred2_pred_input_pixels3, pred2_pred_input_pixels2, pred2_pred_input_pixels1, pred2_pred_input_pixels0} = {pred1_pred_output_pixels15, pred1_pred_output_pixels14, pred1_pred_output_pixels13, pred1_pred_output_pixels12, pred1_pred_output_pixels11, pred1_pred_output_pixels10, pred1_pred_output_pixels9, pred1_pred_output_pixels8, pred1_pred_output_pixels7, pred1_pred_output_pixels6, pred1_pred_output_pixels5, pred1_pred_output_pixels4, pred1_pred_output_pixels3, pred1_pred_output_pixels2, pred1_pred_output_pixels1, pred1_pred_output_pixels0};
assign {diff_pixels_input15, diff_pixels_input14, diff_pixels_input13, diff_pixels_input12, diff_pixels_input11, diff_pixels_input10, diff_pixels_input9, diff_pixels_input8, diff_pixels_input7, diff_pixels_input6, diff_pixels_input5, diff_pixels_input4, diff_pixels_input3, diff_pixels_input2, diff_pixels_input1, diff_pixels_input0} = {pred2_pixels_output15, pred2_pixels_output14, pred2_pixels_output13, pred2_pixels_output12, pred2_pixels_output11, pred2_pixels_output10, pred2_pixels_output9, pred2_pixels_output8, pred2_pixels_output7, pred2_pixels_output6, pred2_pixels_output5, pred2_pixels_output4, pred2_pixels_output3, pred2_pixels_output2, pred2_pixels_output1, pred2_pixels_output0};
assign diff_input_valid = pred2_output_valid;
assign diff_pause_signal = pause_signal;
assign diff_end_in = pred2_end_out;
assign {diff_pred_input_pixels15, diff_pred_input_pixels14, diff_pred_input_pixels13, diff_pred_input_pixels12, diff_pred_input_pixels11, diff_pred_input_pixels10, diff_pred_input_pixels9, diff_pred_input_pixels8, diff_pred_input_pixels7, diff_pred_input_pixels6, diff_pred_input_pixels5, diff_pred_input_pixels4, diff_pred_input_pixels3, diff_pred_input_pixels2, diff_pred_input_pixels1, diff_pred_input_pixels0} = {pred2_pred_output_pixels15, pred2_pred_output_pixels14, pred2_pred_output_pixels13, pred2_pred_output_pixels12, pred2_pred_output_pixels11, pred2_pred_output_pixels10, pred2_pred_output_pixels9, pred2_pred_output_pixels8, pred2_pred_output_pixels7, pred2_pred_output_pixels6, pred2_pred_output_pixels5, pred2_pred_output_pixels4, pred2_pred_output_pixels3, pred2_pred_output_pixels2, pred2_pred_output_pixels1, pred2_pred_output_pixels0};
assign {diff_output_pixels_15, diff_output_pixels_14, diff_output_pixels_13, diff_output_pixels_12, diff_output_pixels_11, diff_output_pixels_10, diff_output_pixels_9, diff_output_pixels_8, diff_output_pixels_7, diff_output_pixels_6, diff_output_pixels_5, diff_output_pixels_4, diff_output_pixels_3, diff_output_pixels_2, diff_output_pixels_1, diff_output_pixels} = {diff_diff_output_pixels15, diff_diff_output_pixels14, diff_diff_output_pixels13, diff_diff_output_pixels12, diff_diff_output_pixels11, diff_diff_output_pixels10, diff_diff_output_pixels9, diff_diff_output_pixels8, diff_diff_output_pixels7, diff_diff_output_pixels6, diff_diff_output_pixels5, diff_diff_output_pixels4, diff_diff_output_pixels3, diff_diff_output_pixels2, diff_diff_output_pixels1, diff_diff_output_pixels0};
assign output_valid = diff_output_valid;
assign end_out = diff_end_out;

always @(posedge sys_clk) begin
	if ((~pred1_pause_signal)) begin
		pred1_multi_row_mode_out <= pred1_multi_row_mode;
		pred1_new_row_out <= pred1_new_row;
		pred1_end_out <= pred1_end_in;
		pred1_output_valid <= pred1_input_valid;
		{pred1_pixels_output15, pred1_pixels_output14, pred1_pixels_output13, pred1_pixels_output12, pred1_pixels_output11, pred1_pixels_output10, pred1_pixels_output9, pred1_pixels_output8, pred1_pixels_output7, pred1_pixels_output6, pred1_pixels_output5, pred1_pixels_output4, pred1_pixels_output3, pred1_pixels_output2, pred1_pixels_output1, pred1_pixels_output0} <= {pred1_pixels_input15, pred1_pixels_input14, pred1_pixels_input13, pred1_pixels_input12, pred1_pixels_input11, pred1_pixels_input10, pred1_pixels_input9, pred1_pixels_input8, pred1_pixels_input7, pred1_pixels_input6, pred1_pixels_input5, pred1_pixels_input4, pred1_pixels_input3, pred1_pixels_input2, pred1_pixels_input1, pred1_pixels_input0};
		if (pred1_input_valid) begin
			pred1_cached_left_pixel <= pred1_pixels_input15;
			pred1_cached_top_left_pixel <= pred1_cached_pixels_input15;
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels0 <= (pred1_cached_left_pixel >>> 1'd1);
		end else begin
			if (pred1_new_row) begin
				pred1_pred_output_pixels0 <= pred1_cached_pixels_input0;
			end else begin
				pred1_pred_output_pixels0 <= (pred1_cached_pixels_input0 - (pred1_cached_top_left_pixel >>> 1'd1));
			end
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels1 <= (pred1_pixels_input0 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels1 <= (pred1_cached_pixels_input1 - (pred1_cached_pixels_input0 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels2 <= (pred1_pixels_input1 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels2 <= (pred1_cached_pixels_input2 - (pred1_cached_pixels_input1 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels3 <= (pred1_pixels_input2 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels3 <= (pred1_cached_pixels_input3 - (pred1_cached_pixels_input2 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels4 <= (pred1_pixels_input3 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels4 <= (pred1_cached_pixels_input4 - (pred1_cached_pixels_input3 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels5 <= (pred1_pixels_input4 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels5 <= (pred1_cached_pixels_input5 - (pred1_cached_pixels_input4 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels6 <= (pred1_pixels_input5 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels6 <= (pred1_cached_pixels_input6 - (pred1_cached_pixels_input5 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels7 <= (pred1_pixels_input6 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels7 <= (pred1_cached_pixels_input7 - (pred1_cached_pixels_input6 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels8 <= (pred1_pixels_input7 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels8 <= (pred1_cached_pixels_input8 - (pred1_cached_pixels_input7 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels9 <= (pred1_pixels_input8 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels9 <= (pred1_cached_pixels_input9 - (pred1_cached_pixels_input8 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels10 <= (pred1_pixels_input9 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels10 <= (pred1_cached_pixels_input10 - (pred1_cached_pixels_input9 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels11 <= (pred1_pixels_input10 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels11 <= (pred1_cached_pixels_input11 - (pred1_cached_pixels_input10 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels12 <= (pred1_pixels_input11 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels12 <= (pred1_cached_pixels_input12 - (pred1_cached_pixels_input11 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels13 <= (pred1_pixels_input12 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels13 <= (pred1_cached_pixels_input13 - (pred1_cached_pixels_input12 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels14 <= (pred1_pixels_input13 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels14 <= (pred1_cached_pixels_input14 - (pred1_cached_pixels_input13 >>> 1'd1));
		end
	end
	if ((~pred1_pause_signal)) begin
		if ((~pred1_multi_row_mode)) begin
			pred1_pred_output_pixels15 <= (pred1_pixels_input14 >>> 1'd1);
		end else begin
			pred1_pred_output_pixels15 <= (pred1_cached_pixels_input15 - (pred1_cached_pixels_input14 >>> 1'd1));
		end
	end
	if ((~pred2_pause_signal)) begin
		pred2_end_out <= pred2_end_in;
		pred2_output_valid <= pred2_input_valid;
		{pred2_pixels_output15, pred2_pixels_output14, pred2_pixels_output13, pred2_pixels_output12, pred2_pixels_output11, pred2_pixels_output10, pred2_pixels_output9, pred2_pixels_output8, pred2_pixels_output7, pred2_pixels_output6, pred2_pixels_output5, pred2_pixels_output4, pred2_pixels_output3, pred2_pixels_output2, pred2_pixels_output1, pred2_pixels_output0} <= {pred2_pixels_input15, pred2_pixels_input14, pred2_pixels_input13, pred2_pixels_input12, pred2_pixels_input11, pred2_pixels_input10, pred2_pixels_input9, pred2_pixels_input8, pred2_pixels_input7, pred2_pixels_input6, pred2_pixels_input5, pred2_pixels_input4, pred2_pixels_input3, pred2_pixels_input2, pred2_pixels_input1, pred2_pixels_input0};
		if (pred2_input_valid) begin
			pred2_cached_left_pixel <= pred2_pixels_input15;
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels0 <= pred2_pred_input_pixels0;
		end else begin
			if (pred2_new_row) begin
				pred2_pred_output_pixels0 <= pred2_pred_input_pixels0;
			end else begin
				pred2_pred_output_pixels0 <= (pred2_pred_input_pixels0 + $signed({1'd0, (pred2_cached_left_pixel >>> 1'd1)}));
			end
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels1 <= pred2_pred_input_pixels1;
		end else begin
			pred2_pred_output_pixels1 <= (pred2_pred_input_pixels1 + $signed({1'd0, (pred2_pixels_input0 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels2 <= pred2_pred_input_pixels2;
		end else begin
			pred2_pred_output_pixels2 <= (pred2_pred_input_pixels2 + $signed({1'd0, (pred2_pixels_input1 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels3 <= pred2_pred_input_pixels3;
		end else begin
			pred2_pred_output_pixels3 <= (pred2_pred_input_pixels3 + $signed({1'd0, (pred2_pixels_input2 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels4 <= pred2_pred_input_pixels4;
		end else begin
			pred2_pred_output_pixels4 <= (pred2_pred_input_pixels4 + $signed({1'd0, (pred2_pixels_input3 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels5 <= pred2_pred_input_pixels5;
		end else begin
			pred2_pred_output_pixels5 <= (pred2_pred_input_pixels5 + $signed({1'd0, (pred2_pixels_input4 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels6 <= pred2_pred_input_pixels6;
		end else begin
			pred2_pred_output_pixels6 <= (pred2_pred_input_pixels6 + $signed({1'd0, (pred2_pixels_input5 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels7 <= pred2_pred_input_pixels7;
		end else begin
			pred2_pred_output_pixels7 <= (pred2_pred_input_pixels7 + $signed({1'd0, (pred2_pixels_input6 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels8 <= pred2_pred_input_pixels8;
		end else begin
			pred2_pred_output_pixels8 <= (pred2_pred_input_pixels8 + $signed({1'd0, (pred2_pixels_input7 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels9 <= pred2_pred_input_pixels9;
		end else begin
			pred2_pred_output_pixels9 <= (pred2_pred_input_pixels9 + $signed({1'd0, (pred2_pixels_input8 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels10 <= pred2_pred_input_pixels10;
		end else begin
			pred2_pred_output_pixels10 <= (pred2_pred_input_pixels10 + $signed({1'd0, (pred2_pixels_input9 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels11 <= pred2_pred_input_pixels11;
		end else begin
			pred2_pred_output_pixels11 <= (pred2_pred_input_pixels11 + $signed({1'd0, (pred2_pixels_input10 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels12 <= pred2_pred_input_pixels12;
		end else begin
			pred2_pred_output_pixels12 <= (pred2_pred_input_pixels12 + $signed({1'd0, (pred2_pixels_input11 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels13 <= pred2_pred_input_pixels13;
		end else begin
			pred2_pred_output_pixels13 <= (pred2_pred_input_pixels13 + $signed({1'd0, (pred2_pixels_input12 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels14 <= pred2_pred_input_pixels14;
		end else begin
			pred2_pred_output_pixels14 <= (pred2_pred_input_pixels14 + $signed({1'd0, (pred2_pixels_input13 >>> 1'd1)}));
		end
	end
	if ((~pred2_pause_signal)) begin
		if ((~pred2_multi_row_mode)) begin
			pred2_pred_output_pixels15 <= pred2_pred_input_pixels15;
		end else begin
			pred2_pred_output_pixels15 <= (pred2_pred_input_pixels15 + $signed({1'd0, (pred2_pixels_input14 >>> 1'd1)}));
		end
	end
	if ((~diff_pause_signal)) begin
		diff_end_out <= diff_end_in;
		diff_output_valid <= diff_input_valid;
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels0 <= ($signed({1'd0, diff_pixels_input0}) - diff_pred_input_pixels0);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels1 <= ($signed({1'd0, diff_pixels_input1}) - diff_pred_input_pixels1);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels2 <= ($signed({1'd0, diff_pixels_input2}) - diff_pred_input_pixels2);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels3 <= ($signed({1'd0, diff_pixels_input3}) - diff_pred_input_pixels3);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels4 <= ($signed({1'd0, diff_pixels_input4}) - diff_pred_input_pixels4);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels5 <= ($signed({1'd0, diff_pixels_input5}) - diff_pred_input_pixels5);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels6 <= ($signed({1'd0, diff_pixels_input6}) - diff_pred_input_pixels6);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels7 <= ($signed({1'd0, diff_pixels_input7}) - diff_pred_input_pixels7);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels8 <= ($signed({1'd0, diff_pixels_input8}) - diff_pred_input_pixels8);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels9 <= ($signed({1'd0, diff_pixels_input9}) - diff_pred_input_pixels9);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels10 <= ($signed({1'd0, diff_pixels_input10}) - diff_pred_input_pixels10);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels11 <= ($signed({1'd0, diff_pixels_input11}) - diff_pred_input_pixels11);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels12 <= ($signed({1'd0, diff_pixels_input12}) - diff_pred_input_pixels12);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels13 <= ($signed({1'd0, diff_pixels_input13}) - diff_pred_input_pixels13);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels14 <= ($signed({1'd0, diff_pixels_input14}) - diff_pred_input_pixels14);
	end
	if ((~diff_pause_signal)) begin
		diff_diff_output_pixels15 <= ($signed({1'd0, diff_pixels_input15}) - diff_pred_input_pixels15);
	end
	if (sys_rst) begin
		pred1_pixels_output0 <= 12'd0;
		pred1_pixels_output1 <= 12'd0;
		pred1_pixels_output2 <= 12'd0;
		pred1_pixels_output3 <= 12'd0;
		pred1_pixels_output4 <= 12'd0;
		pred1_pixels_output5 <= 12'd0;
		pred1_pixels_output6 <= 12'd0;
		pred1_pixels_output7 <= 12'd0;
		pred1_pixels_output8 <= 12'd0;
		pred1_pixels_output9 <= 12'd0;
		pred1_pixels_output10 <= 12'd0;
		pred1_pixels_output11 <= 12'd0;
		pred1_pixels_output12 <= 12'd0;
		pred1_pixels_output13 <= 12'd0;
		pred1_pixels_output14 <= 12'd0;
		pred1_pixels_output15 <= 12'd0;
		pred1_pred_output_pixels0 <= 14'sd0;
		pred1_pred_output_pixels1 <= 14'sd0;
		pred1_pred_output_pixels2 <= 14'sd0;
		pred1_pred_output_pixels3 <= 14'sd0;
		pred1_pred_output_pixels4 <= 14'sd0;
		pred1_pred_output_pixels5 <= 14'sd0;
		pred1_pred_output_pixels6 <= 14'sd0;
		pred1_pred_output_pixels7 <= 14'sd0;
		pred1_pred_output_pixels8 <= 14'sd0;
		pred1_pred_output_pixels9 <= 14'sd0;
		pred1_pred_output_pixels10 <= 14'sd0;
		pred1_pred_output_pixels11 <= 14'sd0;
		pred1_pred_output_pixels12 <= 14'sd0;
		pred1_pred_output_pixels13 <= 14'sd0;
		pred1_pred_output_pixels14 <= 14'sd0;
		pred1_pred_output_pixels15 <= 14'sd0;
		pred1_output_valid <= 1'd0;
		pred1_end_out <= 1'd0;
		pred1_multi_row_mode_out <= 1'd0;
		pred1_new_row_out <= 1'd1;
		pred1_cached_left_pixel <= 13'd4096;
		pred1_cached_top_left_pixel <= 12'd0;
		pred2_pixels_output0 <= 12'd0;
		pred2_pixels_output1 <= 12'd0;
		pred2_pixels_output2 <= 12'd0;
		pred2_pixels_output3 <= 12'd0;
		pred2_pixels_output4 <= 12'd0;
		pred2_pixels_output5 <= 12'd0;
		pred2_pixels_output6 <= 12'd0;
		pred2_pixels_output7 <= 12'd0;
		pred2_pixels_output8 <= 12'd0;
		pred2_pixels_output9 <= 12'd0;
		pred2_pixels_output10 <= 12'd0;
		pred2_pixels_output11 <= 12'd0;
		pred2_pixels_output12 <= 12'd0;
		pred2_pixels_output13 <= 12'd0;
		pred2_pixels_output14 <= 12'd0;
		pred2_pixels_output15 <= 12'd0;
		pred2_pred_output_pixels0 <= 14'sd0;
		pred2_pred_output_pixels1 <= 14'sd0;
		pred2_pred_output_pixels2 <= 14'sd0;
		pred2_pred_output_pixels3 <= 14'sd0;
		pred2_pred_output_pixels4 <= 14'sd0;
		pred2_pred_output_pixels5 <= 14'sd0;
		pred2_pred_output_pixels6 <= 14'sd0;
		pred2_pred_output_pixels7 <= 14'sd0;
		pred2_pred_output_pixels8 <= 14'sd0;
		pred2_pred_output_pixels9 <= 14'sd0;
		pred2_pred_output_pixels10 <= 14'sd0;
		pred2_pred_output_pixels11 <= 14'sd0;
		pred2_pred_output_pixels12 <= 14'sd0;
		pred2_pred_output_pixels13 <= 14'sd0;
		pred2_pred_output_pixels14 <= 14'sd0;
		pred2_pred_output_pixels15 <= 14'sd0;
		pred2_output_valid <= 1'd0;
		pred2_end_out <= 1'd0;
		pred2_cached_left_pixel <= 12'd2048;
		diff_diff_output_pixels0 <= 14'sd0;
		diff_diff_output_pixels1 <= 14'sd0;
		diff_diff_output_pixels2 <= 14'sd0;
		diff_diff_output_pixels3 <= 14'sd0;
		diff_diff_output_pixels4 <= 14'sd0;
		diff_diff_output_pixels5 <= 14'sd0;
		diff_diff_output_pixels6 <= 14'sd0;
		diff_diff_output_pixels7 <= 14'sd0;
		diff_diff_output_pixels8 <= 14'sd0;
		diff_diff_output_pixels9 <= 14'sd0;
		diff_diff_output_pixels10 <= 14'sd0;
		diff_diff_output_pixels11 <= 14'sd0;
		diff_diff_output_pixels12 <= 14'sd0;
		diff_diff_output_pixels13 <= 14'sd0;
		diff_diff_output_pixels14 <= 14'sd0;
		diff_diff_output_pixels15 <= 14'sd0;
		diff_output_valid <= 1'd0;
		diff_end_out <= 1'd0;
	end
end

endmodule


