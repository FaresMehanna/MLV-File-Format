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

class buffer_stage_sequential(Module):

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
		# current pixels to be compressed
		self.pixels_output = pixels_output = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))
		# cached pixels from prev row
		self.cached_pixels_output = cached_pixels_output = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))
		# is output valid for this cycle?
		self.output_valid = output_valid = Signal(reset=0)
		# is cached_pixels_output valid or not, aka are we on multi row mode
		self.multi_row_mode = multi_row_mode = Signal(reset=0)
		# are these pixels are the first in a new row?
		self.new_row = new_row = Signal(reset=1)
		# end_out_signal, is there is no data to output?
		# end_in must be high and no data in the buffers to set end_out to 1
		self.end_out = end_out = Signal(reset=0) 
		self.end_out_helper = end_out_helper = Signal(reset=0) 

		# I/O pins
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in pixels_output} | \
					{_ for _ in cached_pixels_output} | \
					{pause_signal, input_valid, end_in} | \
					{output_valid, multi_row_mode, new_row, end_out}

		# data buffers #
		# main buffer
		self.specials.mem = Memory(constants.VIDEO_MAX_BIT_DEPTH*constants.NUM_IO_PIXELS, constants.ROW_STEPS)
		self.mem_write_port = mem_write_port = self.mem.get_port(write_capable=True)
		self.mem_read_port = mem_read_port = self.mem.get_port(async_read=True)
		self.specials += mem_write_port, mem_read_port

		# inner data #
		# counter for input data
		self.input_counter = input_counter = Signal(int(math.log(constants.ROW_STEPS,2)), reset=0)
		self.multi_row_helper = multi_row_helper = Signal(reset=0)
		self.cached_pixels_cache = cached_pixels_cache = Signal(constants.VIDEO_MAX_BIT_DEPTH*constants.NUM_IO_PIXELS, reset=0)
		self.paused_store = paused_store = Signal(1, reset=0)

		# handle input data
		# handle pixels_output
		self.sync += If(~pause_signal, 
						If(input_valid, 
							#write new data to memory
							mem_write_port.we.eq(1),
							mem_write_port.dat_w.eq(Cat(pixels_input)),
							mem_write_port.adr.eq(input_counter),
							#output new data with in pixels_output
							Cat(pixels_output).eq(Cat(pixels_input)),
							#increase counter
							input_counter.eq(input_counter + 1),
							#set output data as valid
							output_valid.eq(1),
							#handle cached pixels
							mem_read_port.adr.eq(input_counter),
						).Else(
							output_valid.eq(0),
						)
					)

		# handle multi_row_mode signal
		self.sync += If(~pause_signal, 
						If(input_valid, 
							If(~multi_row_mode,
								If(input_counter == 0,
									If(multi_row_helper,
										multi_row_mode.eq(1),
									).Else(
										multi_row_helper.eq(1),
									)
								)
							)
						)
					)

		#handle cached pixels
		self.comb += If(~paused_store,
						Cat(cached_pixels_output).eq(mem_read_port.dat_r),
					).Else(
						Cat(cached_pixels_output).eq(cached_pixels_cache),
					)


		#handle new_row signal
		self.sync += If(~pause_signal, 
						If(input_counter == 0,
							new_row.eq(1),
						).Else(
							new_row.eq(0),
						)
					)

		#handle memory
		self.sync += If(pause_signal | end_in | ~input_valid,
						#turn off writing to memories
						mem_write_port.we.eq(0),
					)

		#handle end_in & end_out
		self.sync += If(~pause_signal,
						If(end_in,
							end_out.eq(1),
						)
					)

		#handle paused store
		self.sync += If(pause_signal,
						paused_store.eq(1),
					).Else(
						paused_store.eq(0),
					)
					
		self.sync += If(~paused_store,
						cached_pixels_cache.eq(mem_read_port.dat_r),
					)

if __name__ == "__main__":
	module = buffer_stage_sequential()
	print(verilog.convert(module, module.ios))