#import python libraries
from migen import *
from migen.fhdl import verilog
import math

#import constants 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import constants

def indices(row_steps):
	
	class rggb_order():
		def __init__(self, color, order):
			self.color = color
			self.order = order

	def get_2_small(full_row, pattern):

		#get smallest and next to smallest
		smallest = [float('Inf'),-1]
		smallest_nex = [float('Inf'),-1]

		for ind, cell in enumerate(full_row):
			if cell.color == pattern and cell.order < smallest[0]:
				smallest[0] = cell.order
				smallest[1] = ind
			elif cell.color == pattern and cell.order < smallest_nex[0]:
				smallest_nex[0] = cell.order
				smallest_nex[1] = ind

		return smallest, smallest_nex

	full_row = []
	moves = []
	max_i = 0

	for max_i in range(row_steps):
		full_row.append(rggb_order("RG",max_i))
		full_row.append(rggb_order("GB",max_i))
	max_i += 1

	while True:
		
		end = False

		for i in range(int(row_steps/2)):
			smallest, smallest_nex = get_2_small(full_row, 'RG')
			#add to moves
			moves.append([smallest[1], smallest_nex[1]])
			#replace
			full_row[smallest[1]] = rggb_order("RG",max_i)
			full_row[smallest_nex[1]] = rggb_order("GB",max_i)
			max_i += 1

			#check for an end
			if moves[-1] == moves[0] and len(moves) != 1:
				moves.pop()
				end = True
				break

		if end:
			break

		for i in range(int(row_steps/2)):
			smallest, smallest_nex = get_2_small(full_row, 'GB')
			#add to moves
			moves.append([smallest[1], smallest_nex[1]])
			#replace
			full_row[smallest[1]] = rggb_order("RG",max_i)
			full_row[smallest_nex[1]] = rggb_order("GB",max_i)
			max_i += 1

	moves = [x for y in moves for x in y]
	return moves

def movements(row_steps):
	initial_movements = []
	for i in range(row_steps*2):
		initial_movements.append(i)
	for i in range(row_steps*2):
		initial_movements.append(i)
	return initial_movements

class bayer_to_sequence(Module):

	def __init__(self):
	
		# input #
		# pixels input
		self.pixels_input = pixels_input = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))
		# is input valid?
		self.input_valid = input_valid = Signal()
		# pause signal will make all the logic stall for this cycle
		self.pause_signal = pause_signal = Signal()
		# end_in_signal, is there is no data in this frame?
		self.end_in = end_in = Signal()

		# output
		# pixels input
		self.pixels_output = pixels_output = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))
		# is output valid?
		self.output_valid = output_valid = Signal(reset=0)
		# end_out_signal, is there is no data to output?
		# end_in must be high and no data in the buffers to set end_out to 1
		self.end_out = end_out = Signal(reset=0) 

		# I/O pins
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in pixels_output} | \
					{pause_signal, input_valid, end_in} | \
					{output_valid, end_out}

		# separate inputs and outputs pixels
		# pixels_input[0:int(constants.NUM_IO_PIXELS/2)]
		self.pixels_input_f = pixels_input_f = [pixels_input[j+i*4] for i in range(0, int(constants.NUM_IO_PIXELS/4)) for j in range(2) ]
		self.pixels_input_s = pixels_input_s = [pixels_input[j+i*4+2] for i in range(0, int(constants.NUM_IO_PIXELS/4)) for j in range(2) ]
		self.pixels_output_f = pixels_output_f = pixels_output[0:int(constants.NUM_IO_PIXELS/2)]
		self.pixels_output_s = pixels_output_s = pixels_output[int(constants.NUM_IO_PIXELS/2):constants.NUM_IO_PIXELS]

		# data buffers #
		# main buffer
		self.specials.mem = Memory(int(constants.VIDEO_MAX_BIT_DEPTH*constants.NUM_IO_PIXELS/2), constants.ROW_STEPS*2)
		self.mem_rw_port1 = mem_rw_port1 = self.mem.get_port(write_capable=True, async_read=True)
		self.mem_rw_port2 = mem_rw_port2 = self.mem.get_port(write_capable=True, async_read=True)
		self.specials += mem_rw_port1, mem_rw_port2


		'''
		This was the original way, it was cleaner but take more memory when
		constants.ROW_STEPS increases. it was replaced with a dynamic method
		that is guaranteed to take 4 x constants.ROW_STEPS memory with 
		(lg(constants.ROW_STEPS,2)+1) bits in each slot.
		'''
		# data movement buffer
		# self.specials.move_mem = Memory(int(math.log(constants.ROW_STEPS,2)) + 1, len(indices(constants.ROW_STEPS)), init=indices(constants.ROW_STEPS))
		# self.move_mem_read_port1 = move_mem_read_port1 = self.move_mem.get_port(async_read=True)
		# self.move_mem_read_port2 = move_mem_read_port2 = self.move_mem.get_port(async_read=True)
		# self.specials += move_mem_read_port1, move_mem_read_port2

		# data movement buffer
		self.specials.move_mem = Memory(int(math.log(constants.ROW_STEPS,2)) + 1, constants.ROW_STEPS*4, init=movements(constants.ROW_STEPS))
		self.move_mem_write_port1 = move_mem_write_port1 = self.move_mem.get_port(write_capable=True)
		self.move_mem_write_port2 = move_mem_write_port2 = self.move_mem.get_port(write_capable=True)
		self.move_mem_read_port1 = move_mem_read_port1 = self.move_mem.get_port(async_read=True)
		self.move_mem_read_port2 = move_mem_read_port2 = self.move_mem.get_port(async_read=True)
		self.specials += move_mem_read_port1, move_mem_read_port2, move_mem_write_port1, move_mem_write_port2

		# inner data #
		self.input_counter = input_counter = Signal(int(math.log(constants.ROW_STEPS,2))+2, reset=0)

		#first burst
		self.first_burst = first_burst = Signal(reset=1)

		#last buffer counter
		self.last_buff_counter = last_buff_counter = Signal(int(math.log(constants.ROW_STEPS,2)+1), reset=0)

		#pause signal handling
		self.pixels_output_f_cache = pixels_output_f_cache = Signal(int(constants.VIDEO_MAX_BIT_DEPTH*constants.NUM_IO_PIXELS/2))
		self.pixels_output_s_cache = pixels_output_s_cache = Signal(int(constants.VIDEO_MAX_BIT_DEPTH*constants.NUM_IO_PIXELS/2))
		self.paused_store = paused_store = Signal(1, reset=0)

		#handle the counter
		self.sync += If(~pause_signal,
						If(input_valid | end_in,
							input_counter.eq(input_counter + 2),
						)
					)

		#handle first burst when data output is invalid
		self.sync += first_burst.eq(first_burst & (input_counter != ((constants.ROW_STEPS*2)-2)))

		#handle the data
		self.sync += If(~pause_signal,
						# get the input
						If(input_valid,
							mem_rw_port1.we.eq(1),
							mem_rw_port1.dat_w.eq(Cat(pixels_input_f)),
							mem_rw_port1.adr.eq(move_mem_read_port1.dat_r),
							#write second half of the data to higher memory
							mem_rw_port2.we.eq(1),
							mem_rw_port2.dat_w.eq(Cat(pixels_input_s)),
							mem_rw_port2.adr.eq(move_mem_read_port2.dat_r),
							#output is valid
							output_valid.eq(1 & (~first_burst)),
							#write movement data
							move_mem_write_port1.we.eq(1),
							move_mem_write_port2.we.eq(1),
							move_mem_write_port1.dat_w.eq(move_mem_read_port1.dat_r),
							move_mem_write_port2.dat_w.eq(move_mem_read_port2.dat_r),
							move_mem_write_port1.adr.eq(((input_counter>>1)&(~constants.ROW_STEPS))|((~input_counter)&(constants.ROW_STEPS*2))),
							move_mem_write_port2.adr.eq(((input_counter>>1)|constants.ROW_STEPS|((~input_counter)&(constants.ROW_STEPS*2)))),
						).Else(
							# output is not valid
							output_valid.eq(0),
						)
					)

		#handle end_in & end_out
		self.sync += If(~pause_signal,
						If(end_in,
							#if no more data in internal buffer, signal end_out
							If(last_buff_counter == constants.ROW_STEPS,
								end_out.eq(1),
								output_valid.eq(0),
							).Else(
								#increase last_buff counter
								last_buff_counter.eq(last_buff_counter + 1),
								#output the data
								output_valid.eq(1),
								#read from read-write ports
								mem_rw_port1.adr.eq(move_mem_read_port1.dat_r),
								mem_rw_port2.adr.eq(move_mem_read_port2.dat_r),
							)
						)
					)

		#handle memories
		self.sync += If(pause_signal | end_in | ~input_valid,
						#turn off writing to memories
						mem_rw_port1.we.eq(0),
						mem_rw_port2.we.eq(0),
						move_mem_write_port1.we.eq(0),
						move_mem_write_port2.we.eq(0),
					)

		#data output
		self.comb += move_mem_read_port1.adr.eq(input_counter)
		self.comb += move_mem_read_port2.adr.eq(input_counter|1)
		self.comb += If(~paused_store,
						Cat(pixels_output_f).eq(mem_rw_port1.dat_r),
						Cat(pixels_output_s).eq(mem_rw_port2.dat_r)
					).Else(
						Cat(pixels_output_f).eq(pixels_output_f_cache),
						Cat(pixels_output_s).eq(pixels_output_s_cache),
					)

		#handle paused store
		self.sync += If(pause_signal,
						paused_store.eq(1),
					).Else(
						paused_store.eq(0),
					)
		self.sync += If(~paused_store,
						pixels_output_f_cache.eq(mem_rw_port1.dat_r),
						pixels_output_s_cache.eq(mem_rw_port2.dat_r),
					)

if __name__ == "__main__":
	module = bayer_to_sequence()
	print(verilog.convert(module, module.ios))