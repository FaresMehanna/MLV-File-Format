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
	output reg output_valid,
	output reg end_out,
	input sys_clk,
	input sys_rst
);

reg [5:0] mem_write_port1_adr = 6'd0;
wire [95:0] mem_write_port1_dat_r;
reg mem_write_port1_we = 1'd0;
reg [95:0] mem_write_port1_dat_w = 96'd0;
wire [5:0] mem_read_port1_adr;
wire [95:0] mem_read_port1_dat_r;
reg [5:0] mem_write_port2_adr = 6'd0;
wire [95:0] mem_write_port2_dat_r;
reg mem_write_port2_we = 1'd0;
reg [95:0] mem_write_port2_dat_w = 96'd0;
wire [5:0] mem_read_port2_adr;
wire [95:0] mem_read_port2_dat_r;
reg [6:0] move_mem_write_port1_adr = 7'd0;
wire [5:0] move_mem_write_port1_dat_r;
reg move_mem_write_port1_we = 1'd0;
reg [5:0] move_mem_write_port1_dat_w = 6'd0;
reg [6:0] move_mem_write_port2_adr = 7'd0;
wire [5:0] move_mem_write_port2_dat_r;
reg move_mem_write_port2_we = 1'd0;
reg [5:0] move_mem_write_port2_dat_w = 6'd0;
wire [6:0] move_mem_read_port1_adr;
wire [5:0] move_mem_read_port1_dat_r;
wire [6:0] move_mem_read_port2_adr;
wire [5:0] move_mem_read_port2_dat_r;
reg [6:0] input_counter = 7'd0;
reg first_burst = 1'd1;
reg [4:0] last_buff_counter = 5'd0;
reg [95:0] pixels_output_f_cache = 96'd0;
reg [95:0] pixels_output_s_cache = 96'd0;
reg paused_store = 1'd0;


// Adding a dummy event (using a dummy signal 'dummy_s') to get the simulator
// to run the combinatorial process once at the beginning.
// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign move_mem_read_port1_adr = input_counter;
assign move_mem_read_port2_adr = (input_counter | 1'd1);
assign mem_read_port1_adr = move_mem_read_port1_dat_r;
assign mem_read_port2_adr = move_mem_read_port2_dat_r;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	pixels_output <= 12'd0;
	pixels_output_1 <= 12'd0;
	pixels_output_2 <= 12'd0;
	pixels_output_3 <= 12'd0;
	pixels_output_4 <= 12'd0;
	pixels_output_5 <= 12'd0;
	pixels_output_6 <= 12'd0;
	pixels_output_7 <= 12'd0;
	if ((~paused_store)) begin
		{pixels_output_7, pixels_output_6, pixels_output_5, pixels_output_4, pixels_output_3, pixels_output_2, pixels_output_1, pixels_output} <= mem_read_port1_dat_r;
	end else begin
		{pixels_output_7, pixels_output_6, pixels_output_5, pixels_output_4, pixels_output_3, pixels_output_2, pixels_output_1, pixels_output} <= pixels_output_f_cache;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_1;
// synthesis translate_on
always @(*) begin
	pixels_output_8 <= 12'd0;
	pixels_output_9 <= 12'd0;
	pixels_output_10 <= 12'd0;
	pixels_output_11 <= 12'd0;
	pixels_output_12 <= 12'd0;
	pixels_output_13 <= 12'd0;
	pixels_output_14 <= 12'd0;
	pixels_output_15 <= 12'd0;
	if ((~paused_store)) begin
		{pixels_output_15, pixels_output_14, pixels_output_13, pixels_output_12, pixels_output_11, pixels_output_10, pixels_output_9, pixels_output_8} <= mem_read_port2_dat_r;
	end else begin
		{pixels_output_15, pixels_output_14, pixels_output_13, pixels_output_12, pixels_output_11, pixels_output_10, pixels_output_9, pixels_output_8} <= pixels_output_s_cache;
	end
// synthesis translate_off
	dummy_d_1 <= dummy_s;
// synthesis translate_on
end

always @(posedge sys_clk) begin
	if ((~pause_signal)) begin
		if (input_valid) begin
			input_counter <= (input_counter + 2'd2);
		end
	end
	first_burst <= (first_burst & (input_counter != 6'd60));
	if ((~pause_signal)) begin
		if (input_valid) begin
			mem_write_port1_we <= 1'd1;
			mem_write_port1_dat_w <= {pixels_input_13, pixels_input_12, pixels_input_9, pixels_input_8, pixels_input_5, pixels_input_4, pixels_input_1, pixels_input};
			mem_write_port1_adr <= move_mem_read_port1_dat_r;
			mem_write_port2_we <= 1'd1;
			mem_write_port2_dat_w <= {pixels_input_15, pixels_input_14, pixels_input_11, pixels_input_10, pixels_input_7, pixels_input_6, pixels_input_3, pixels_input_2};
			mem_write_port2_adr <= move_mem_read_port2_dat_r;
			output_valid <= (1'd1 & (~first_burst));
			move_mem_write_port1_we <= 1'd1;
			move_mem_write_port2_we <= 1'd1;
			move_mem_write_port1_dat_w <= move_mem_read_port1_dat_r;
			move_mem_write_port2_dat_w <= move_mem_read_port2_dat_r;
			move_mem_write_port1_adr <= (($signed({1'd0, (input_counter >>> 1'd1)}) & 7'sd95) | $signed({1'd0, ((~input_counter) & 7'd64)}));
			move_mem_write_port2_adr <= (((input_counter >>> 1'd1) | 6'd32) | ((~input_counter) & 7'd64));
		end else begin
			output_valid <= 1'd0;
		end
	end
	if ((~pause_signal)) begin
		if (end_in) begin
			if ((last_buff_counter == 5'd31)) begin
				end_out <= 1'd1;
				output_valid <= 1'd0;
			end else begin
				input_counter <= (input_counter + 2'd2);
				last_buff_counter <= (last_buff_counter + 1'd1);
				output_valid <= 1'd1;
			end
		end
	end
	if (((pause_signal | end_in) | (~input_valid))) begin
		mem_write_port1_we <= 1'd0;
		mem_write_port2_we <= 1'd0;
		move_mem_write_port1_we <= 1'd0;
		move_mem_write_port2_we <= 1'd0;
	end
	if (pause_signal) begin
		paused_store <= 1'd1;
	end else begin
		paused_store <= 1'd0;
	end
	if ((~paused_store)) begin
		pixels_output_f_cache <= mem_read_port1_dat_r;
		pixels_output_s_cache <= mem_read_port2_dat_r;
	end
	if (sys_rst) begin
		output_valid <= 1'd0;
		end_out <= 1'd0;
		mem_write_port1_adr <= 6'd0;
		mem_write_port1_we <= 1'd0;
		mem_write_port1_dat_w <= 96'd0;
		mem_write_port2_adr <= 6'd0;
		mem_write_port2_we <= 1'd0;
		mem_write_port2_dat_w <= 96'd0;
		move_mem_write_port1_adr <= 7'd0;
		move_mem_write_port1_we <= 1'd0;
		move_mem_write_port1_dat_w <= 6'd0;
		move_mem_write_port2_adr <= 7'd0;
		move_mem_write_port2_we <= 1'd0;
		move_mem_write_port2_dat_w <= 6'd0;
		input_counter <= 7'd0;
		first_burst <= 1'd1;
		last_buff_counter <= 5'd0;
		pixels_output_f_cache <= 96'd0;
		pixels_output_s_cache <= 96'd0;
		paused_store <= 1'd0;
	end
end

reg [95:0] mem[0:63];
reg [5:0] memadr;
reg [5:0] memadr_1;
always @(posedge sys_clk) begin
	if (mem_write_port1_we)
		mem[mem_write_port1_adr] <= mem_write_port1_dat_w;
	memadr <= mem_write_port1_adr;
end

always @(posedge sys_clk) begin
end

always @(posedge sys_clk) begin
	if (mem_write_port2_we)
		mem[mem_write_port2_adr] <= mem_write_port2_dat_w;
	memadr_1 <= mem_write_port2_adr;
end

always @(posedge sys_clk) begin
end

assign mem_write_port1_dat_r = mem[memadr];
assign mem_read_port1_dat_r = mem[mem_read_port1_adr];
assign mem_write_port2_dat_r = mem[memadr_1];
assign mem_read_port2_dat_r = mem[mem_read_port2_adr];

reg [5:0] move_mem[0:127];
reg [6:0] memadr_2;
reg [6:0] memadr_3;
always @(posedge sys_clk) begin
	if (move_mem_write_port1_we)
		move_mem[move_mem_write_port1_adr] <= move_mem_write_port1_dat_w;
	memadr_2 <= move_mem_write_port1_adr;
end

always @(posedge sys_clk) begin
	if (move_mem_write_port2_we)
		move_mem[move_mem_write_port2_adr] <= move_mem_write_port2_dat_w;
	memadr_3 <= move_mem_write_port2_adr;
end

always @(posedge sys_clk) begin
end

always @(posedge sys_clk) begin
end

assign move_mem_write_port1_dat_r = move_mem[memadr_2];
assign move_mem_write_port2_dat_r = move_mem[memadr_3];
assign move_mem_read_port1_dat_r = move_mem[move_mem_read_port1_adr];
assign move_mem_read_port2_dat_r = move_mem[move_mem_read_port2_adr];

initial begin
	$readmemh("move_mem.init", move_mem);
end

endmodule

move_mem.init:
0
1
2
3
4
5
6
7
8
9
a
b
c
d
e
f
10
11
12
13
14
15
16
17
18
19
1a
1b
1c
1d
1e
1f
20
21
22
23
24
25
26
27
28
29
2a
2b
2c
2d
2e
2f
30
31
32
33
34
35
36
37
38
39
3a
3b
3c
3d
3e
3f
0
1
2
3
4
5
6
7
8
9
a
b
c
d
e
f
10
11
12
13
14
15
16
17
18
19
1a
1b
1c
1d
1e
1f
20
21
22
23
24
25
26
27
28
29
2a
2b
2c
2d
2e
2f
30
31
32
33
34
35
36
37
38
39
3a
3b
3c
3d
3e
3f

