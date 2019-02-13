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
	output reg [11:0] pixels_output,
	output reg [11:0] pixels_output_1,
	output reg [11:0] pixels_output_2,
	output reg [11:0] pixels_output_3,
	output reg [11:0] pixels_output_4,
	output reg [11:0] pixels_output_5,
	output reg [11:0] pixels_output_6,
	output reg [11:0] pixels_output_7,
	output reg [11:0] pixels_output_8,
	output reg [11:0] pixels_output_9,
	output reg [11:0] pixels_output_10,
	output reg [11:0] pixels_output_11,
	output reg [11:0] pixels_output_12,
	output reg [11:0] pixels_output_13,
	output reg [11:0] pixels_output_14,
	output reg [11:0] pixels_output_15,
	output reg [11:0] cached_pixels_output,
	output reg [11:0] cached_pixels_output_1,
	output reg [11:0] cached_pixels_output_2,
	output reg [11:0] cached_pixels_output_3,
	output reg [11:0] cached_pixels_output_4,
	output reg [11:0] cached_pixels_output_5,
	output reg [11:0] cached_pixels_output_6,
	output reg [11:0] cached_pixels_output_7,
	output reg [11:0] cached_pixels_output_8,
	output reg [11:0] cached_pixels_output_9,
	output reg [11:0] cached_pixels_output_10,
	output reg [11:0] cached_pixels_output_11,
	output reg [11:0] cached_pixels_output_12,
	output reg [11:0] cached_pixels_output_13,
	output reg [11:0] cached_pixels_output_14,
	output reg [11:0] cached_pixels_output_15,
	output reg output_valid,
	output reg multi_row_mode,
	output reg new_row,
	output reg end_out,
	input sys_clk,
	input sys_rst
);

reg [4:0] mem_write_port_adr = 5'd0;
wire [191:0] mem_write_port_dat_r;
reg mem_write_port_we = 1'd0;
reg [191:0] mem_write_port_dat_w = 192'd0;
reg [4:0] mem_read_port_adr = 5'd0;
wire [191:0] mem_read_port_dat_r;
reg [4:0] input_counter = 5'd0;
reg multi_row_helper = 1'd0;
reg [191:0] cached_pixels_cache = 192'd0;
reg paused_store = 1'd0;


// Adding a dummy event (using a dummy signal 'dummy_s') to get the simulator
// to run the combinatorial process once at the beginning.
// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on


// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	cached_pixels_output <= 12'd0;
	cached_pixels_output_1 <= 12'd0;
	cached_pixels_output_2 <= 12'd0;
	cached_pixels_output_3 <= 12'd0;
	cached_pixels_output_4 <= 12'd0;
	cached_pixels_output_5 <= 12'd0;
	cached_pixels_output_6 <= 12'd0;
	cached_pixels_output_7 <= 12'd0;
	cached_pixels_output_8 <= 12'd0;
	cached_pixels_output_9 <= 12'd0;
	cached_pixels_output_10 <= 12'd0;
	cached_pixels_output_11 <= 12'd0;
	cached_pixels_output_12 <= 12'd0;
	cached_pixels_output_13 <= 12'd0;
	cached_pixels_output_14 <= 12'd0;
	cached_pixels_output_15 <= 12'd0;
	if ((~paused_store)) begin
		{cached_pixels_output_15, cached_pixels_output_14, cached_pixels_output_13, cached_pixels_output_12, cached_pixels_output_11, cached_pixels_output_10, cached_pixels_output_9, cached_pixels_output_8, cached_pixels_output_7, cached_pixels_output_6, cached_pixels_output_5, cached_pixels_output_4, cached_pixels_output_3, cached_pixels_output_2, cached_pixels_output_1, cached_pixels_output} <= mem_read_port_dat_r;
	end else begin
		{cached_pixels_output_15, cached_pixels_output_14, cached_pixels_output_13, cached_pixels_output_12, cached_pixels_output_11, cached_pixels_output_10, cached_pixels_output_9, cached_pixels_output_8, cached_pixels_output_7, cached_pixels_output_6, cached_pixels_output_5, cached_pixels_output_4, cached_pixels_output_3, cached_pixels_output_2, cached_pixels_output_1, cached_pixels_output} <= cached_pixels_cache;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

always @(posedge sys_clk) begin
	if ((~pause_signal)) begin
		if (input_valid) begin
			mem_write_port_we <= 1'd1;
			mem_write_port_dat_w <= {pixels_input_15, pixels_input_14, pixels_input_13, pixels_input_12, pixels_input_11, pixels_input_10, pixels_input_9, pixels_input_8, pixels_input_7, pixels_input_6, pixels_input_5, pixels_input_4, pixels_input_3, pixels_input_2, pixels_input_1, pixels_input};
			mem_write_port_adr <= input_counter;
			{pixels_output_15, pixels_output_14, pixels_output_13, pixels_output_12, pixels_output_11, pixels_output_10, pixels_output_9, pixels_output_8, pixels_output_7, pixels_output_6, pixels_output_5, pixels_output_4, pixels_output_3, pixels_output_2, pixels_output_1, pixels_output} <= {pixels_input_15, pixels_input_14, pixels_input_13, pixels_input_12, pixels_input_11, pixels_input_10, pixels_input_9, pixels_input_8, pixels_input_7, pixels_input_6, pixels_input_5, pixels_input_4, pixels_input_3, pixels_input_2, pixels_input_1, pixels_input};
			input_counter <= (input_counter + 1'd1);
			output_valid <= 1'd1;
			mem_read_port_adr <= input_counter;
		end else begin
			output_valid <= 1'd0;
		end
	end
	if ((~pause_signal)) begin
		if (input_valid) begin
			if ((~multi_row_mode)) begin
				if ((input_counter == 1'd0)) begin
					if (multi_row_helper) begin
						multi_row_mode <= 1'd1;
					end else begin
						multi_row_helper <= 1'd1;
					end
				end
			end
		end
	end
	if ((~pause_signal)) begin
		if ((input_counter == 1'd0)) begin
			new_row <= 1'd1;
		end else begin
			new_row <= 1'd0;
		end
	end
	if (((pause_signal | end_in) | (~input_valid))) begin
		mem_write_port_we <= 1'd0;
	end
	if ((~pause_signal)) begin
		if (end_in) begin
			end_out <= 1'd1;
		end
	end
	if (pause_signal) begin
		paused_store <= 1'd1;
	end else begin
		paused_store <= 1'd0;
	end
	if ((~paused_store)) begin
		cached_pixels_cache <= mem_read_port_dat_r;
	end
	if (sys_rst) begin
		pixels_output <= 12'd0;
		pixels_output_1 <= 12'd0;
		pixels_output_2 <= 12'd0;
		pixels_output_3 <= 12'd0;
		pixels_output_4 <= 12'd0;
		pixels_output_5 <= 12'd0;
		pixels_output_6 <= 12'd0;
		pixels_output_7 <= 12'd0;
		pixels_output_8 <= 12'd0;
		pixels_output_9 <= 12'd0;
		pixels_output_10 <= 12'd0;
		pixels_output_11 <= 12'd0;
		pixels_output_12 <= 12'd0;
		pixels_output_13 <= 12'd0;
		pixels_output_14 <= 12'd0;
		pixels_output_15 <= 12'd0;
		output_valid <= 1'd0;
		multi_row_mode <= 1'd0;
		new_row <= 1'd1;
		end_out <= 1'd0;
		mem_write_port_adr <= 5'd0;
		mem_write_port_we <= 1'd0;
		mem_write_port_dat_w <= 192'd0;
		mem_read_port_adr <= 5'd0;
		input_counter <= 5'd0;
		multi_row_helper <= 1'd0;
		cached_pixels_cache <= 192'd0;
		paused_store <= 1'd0;
	end
end

reg [191:0] mem[0:31];
reg [4:0] memadr;
always @(posedge sys_clk) begin
	if (mem_write_port_we)
		mem[mem_write_port_adr] <= mem_write_port_dat_w;
	memadr <= mem_write_port_adr;
end

always @(posedge sys_clk) begin
end

assign mem_write_port_dat_r = mem[memadr];
assign mem_read_port_dat_r = mem[mem_read_port_adr];

endmodule


