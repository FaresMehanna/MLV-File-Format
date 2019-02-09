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

		# I/O pins
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in pixels_output} | \
					{_ for _ in cached_pixels_output} | \
					{input_valid} | \
					{output_valid, multi_row_mode, new_row}

		# data buffers #
		# main buffer
		self.specials.mem = Memory(constants.VIDEO_MAX_BIT_DEPTH*constants.NUM_IO_PIXELS, constants.ROW_STEPS)
		self.mem_write_port = mem_write_port = self.mem.get_port(write_capable=True)
		self.mem_read_port = mem_read_port = self.mem.get_port(async_read=False)
		self.specials += mem_write_port, mem_read_port

		# inner data #
		# counter for input data
		self.input_counter = input_counter = Signal(int(math.log(constants.ROW_STEPS,2)), reset=constants.ROW_STEPS-1)
		self.new_row_helper = new_row_helper = Signal(reset=1)
		self.multi_row_helper = multi_row_helper = Signal(reset=0)

		# handle input data
		# handle pixels_output
		self.sync += If(input_valid, 
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
						#after first data set new_row helper to zero
						new_row_helper.eq(0),
					).Else(
						mem_write_port.we.eq(0),
					)

		# handle multi_row_mode signal
		self.sync += If(input_valid, 
						If(~multi_row_mode,
							If(input_counter == constants.ROW_STEPS-1,
								If(multi_row_helper,
									multi_row_mode.eq(1),
								).Else(
									multi_row_helper.eq(1),
								)
							)
						)
					)

		#handle cached pixels
		self.comb += mem_read_port.adr.eq(input_counter)
		self.comb += Cat(cached_pixels_output).eq(mem_read_port.dat_r)

		#handle new_row signal
		self.sync += If(input_counter == constants.ROW_STEPS-1,
						new_row.eq(1),
					).Elif(~new_row_helper,
						new_row.eq(0),
					)

if __name__ == "__main__":
	module = buffer_stage_sequential()
	print(verilog.convert(module, module.ios))