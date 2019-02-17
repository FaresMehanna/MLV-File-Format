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

class predictor_1(Module):

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
		# is cached_pixels_input valid or not, aka are we on multi row mode
		self.multi_row_mode = multi_row_mode = Signal()
		# are these pixels are the first in a new row?
		self.new_row = new_row = Signal()
		# cached pixels from prev row
		self.cached_pixels_input = cached_pixels_input = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))

		# output
		# pixels output
		self.pixels_output = pixels_output = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))
		# pred_output_pixels output
		self.pred_output_pixels = pred_output_pixels = Array(Signal((constants.VIDEO_MAX_BIT_DEPTH+2,True)) for _ in range(constants.NUM_IO_PIXELS))
		# is output valid?
		self.output_valid = output_valid = Signal(reset=0)
		# end_out_signal, is there is no data to output?
		# end_in must be high and no data in the buffers to set end_out to 1
		self.end_out = end_out = Signal(reset=0) 
		# are we on multi row mode
		self.multi_row_mode_out = multi_row_mode_out = Signal(reset=0)
		# is this start of new row?
		self.new_row_out = new_row_out = Signal(reset=1)

		# inner data needed for prediction
		self.cached_left_pixel = cached_left_pixel = Signal(constants.VIDEO_MAX_BIT_DEPTH+1, reset=2**(constants.VIDEO_MAX_BIT_DEPTH))
		self.cached_top_left_pixel = cached_top_left_pixel = Signal(constants.VIDEO_MAX_BIT_DEPTH)

		# I/O
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in cached_pixels_input} | \
					{_ for _ in pixels_output} | \
					{_ for _ in pred_output_pixels} | \
					{pause_signal, input_valid, end_in, multi_row_mode, new_row} | \
					{output_valid, end_out, multi_row_mode_out, new_row_out}


		self.sync += If(~pause_signal,
						#handle multi_row_mode_out
						multi_row_mode_out.eq(multi_row_mode),
						#handle new_row_out
						new_row_out.eq(new_row),
						#handle end_out
						end_out.eq(end_in),
						#handle output_valid
						output_valid.eq(input_valid),
						#handle pixels_output
						Cat(pixels_output).eq(Cat(pixels_input)),
						#handle cached_left_pixel & cached_top_left_pixel
						If(input_valid,
							cached_left_pixel.eq(pixels_input[-1]),
							cached_top_left_pixel.eq(cached_pixels_input[-1]),
						)
					)

		'''  handle pred_output_pixels  '''
		for index, pred_out in enumerate(pred_output_pixels):
			# handle first pixel
			if index == 0:
				self.sync += If(~pause_signal,
								# handle if in single row mode
								If(~multi_row_mode,
									pred_out.eq((cached_left_pixel>>1)),
								).Else(
									# handle if in new row
									If(new_row,
										pred_out.eq(cached_pixels_input[0]),
									# handle if normal pixel
									).Else(
										pred_out.eq(cached_pixels_input[0]-(cached_top_left_pixel>>1)),
									)
								)
							)
			# handle the rest of pixels
			else:
				self.sync += If(~pause_signal,
								# handle if in single row mode
								If(~multi_row_mode,
									pred_out.eq((pixels_input[index-1]>>1)),
								# handle the rest of pixels, whether it is new row or not
								# does not matter.
								).Else(
									pred_out.eq(cached_pixels_input[index]-(cached_pixels_input[index-1]>>1)),
								)
							)



class predictor_2(Module):

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
		# are we on multi row mode
		self.multi_row_mode = multi_row_mode = Signal()
		# semi-predicted pixels from last stage
		self.pred_input_pixels = pred_input_pixels = Array(Signal((constants.VIDEO_MAX_BIT_DEPTH+2,True)) for _ in range(constants.NUM_IO_PIXELS))
		# are these pixels are the first in a new row?
		self.new_row = new_row = Signal()

		# output
		# pixels output
		self.pixels_output = pixels_output = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))
		# pred_output_pixels output
		self.pred_output_pixels = pred_output_pixels = Array(Signal((constants.VIDEO_MAX_BIT_DEPTH+2,True)) for _ in range(constants.NUM_IO_PIXELS))
		# is output valid?
		self.output_valid = output_valid = Signal(reset=0)
		# end_out_signal, is there is no data to output?
		# end_in must be high and no data in the buffers to set end_out to 1
		self.end_out = end_out = Signal(reset=0) 

		# inner data needed for prediction
		self.cached_left_pixel = cached_left_pixel = Signal(constants.VIDEO_MAX_BIT_DEPTH, reset=2**(constants.VIDEO_MAX_BIT_DEPTH-1))

		# I/O
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in pixels_output} | \
					{_ for _ in pred_output_pixels} | \
					{_ for _ in pred_input_pixels} | \
					{pause_signal, input_valid, end_in, multi_row_mode, new_row} | \
					{output_valid, end_out}


		self.sync += If(~pause_signal,
						#handle end_out
						end_out.eq(end_in),
						#handle output_valid
						output_valid.eq(input_valid),
						#handle pixels_output
						Cat(pixels_output).eq(Cat(pixels_input)),
						#handle cached_left_pixel
						If(input_valid,
							cached_left_pixel.eq(pixels_input[-1]),
						)
					)

		'''  handle pred_output_pixels  '''
		for index, pred_out in enumerate(pred_output_pixels):
			# handle first pixel
			if index == 0:
				self.sync += If(~pause_signal,
								# handle if in single row mode
								If(~multi_row_mode,
									pred_out.eq(pred_input_pixels[0]),
								).Else(
									# handle if in new row
									If(new_row,
										pred_out.eq(pred_input_pixels[0]),
									# handle if normal pixel
									).Else(
										pred_out.eq(pred_input_pixels[0] + (cached_left_pixel>>1)),
									)
								)
							)

			# handle the rest of pixels
			else:
				self.sync += If(~pause_signal,
								# handle if in single row mode
								If(~multi_row_mode,
									pred_out.eq(pred_input_pixels[index]),
								).Else(
									pred_out.eq(pred_input_pixels[index] + (pixels_input[index-1]>>1)),
								)
							)



class difference(Module):

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
		# predicted pixels from predictor stages
		self.pred_input_pixels = pred_input_pixels = Array(Signal((constants.VIDEO_MAX_BIT_DEPTH+2,True)) for _ in range(constants.NUM_IO_PIXELS))


		# output
		# diff_output_pixels output
		self.diff_output_pixels = diff_output_pixels = Array(Signal((constants.VIDEO_MAX_BIT_DEPTH+2,True)) for _ in range(constants.NUM_IO_PIXELS))
		# is output valid?
		self.output_valid = output_valid = Signal(reset=0)
		# end_out_signal, is there is no data to output?
		# end_in must be high and no data in the buffers to set end_out to 1
		self.end_out = end_out = Signal(reset=0) 


		# I/O
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in diff_output_pixels} | \
					{_ for _ in pred_input_pixels} | \
					{pause_signal, input_valid, end_in} | \
					{output_valid, end_out}

		self.sync += If(~pause_signal,
						#handle end_out
						end_out.eq(end_in),
						#handle output_valid
						output_valid.eq(input_valid),
					)

		'''  handle diff_output_pixels  '''
		for index, diff_out in enumerate(diff_output_pixels):
				self.sync += If(~pause_signal,
								diff_out.eq(pixels_input[index]-pred_input_pixels[index]),
							)



class predictor_difference_stage(Module):

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
		# is cached_pixels_input valid or not, aka are we on multi row mode
		self.multi_row_mode = multi_row_mode = Signal()
		# are these pixels are the first in a new row?
		self.new_row = new_row = Signal()
		# cached pixels from prev row
		self.cached_pixels_input = cached_pixels_input = Array(Signal(constants.VIDEO_MAX_BIT_DEPTH) for _ in range(constants.NUM_IO_PIXELS))


		# output
		# diff_output_pixels output
		self.diff_output_pixels = diff_output_pixels = Array(Signal((constants.VIDEO_MAX_BIT_DEPTH+2,True)) for _ in range(constants.NUM_IO_PIXELS))
		# is output valid?
		self.output_valid = output_valid = Signal(reset=0)
		# end_out_signal, is there is no data to output?
		# end_in must be high and no data in the buffers to set end_out to 1
		self.end_out = end_out = Signal(reset=0)

		# I/O
		self.ios =	{_ for _ in pixels_input} | \
					{_ for _ in diff_output_pixels} | \
					{_ for _ in cached_pixels_input} | \
					{pause_signal, input_valid, end_in, multi_row_mode, new_row} | \
					{output_valid, end_out}

		# submodules
		self.submodules.pred1 = predictor_1()
		self.submodules.pred2 = predictor_2()
		self.submodules.diff = difference()

		''' connect the modules together '''
		# main-in and pred1 
		self.comb += Cat(self.pred1.pixels_input).eq(Cat(pixels_input))
		self.comb += self.pred1.input_valid.eq(input_valid)
		self.comb += self.pred1.pause_signal.eq(pause_signal)
		self.comb += self.pred1.end_in.eq(end_in)
		self.comb += self.pred1.multi_row_mode.eq(multi_row_mode)
		self.comb += self.pred1.new_row.eq(new_row)
		self.comb += Cat(self.pred1.cached_pixels_input).eq(Cat(cached_pixels_input))
		# pred1 and pred2 
		self.comb += Cat(self.pred2.pixels_input).eq(Cat(self.pred1.pixels_output))
		self.comb += self.pred2.new_row.eq(self.pred1.new_row_out)
		self.comb += self.pred2.input_valid.eq(self.pred1.output_valid)
		self.comb += self.pred2.pause_signal.eq(pause_signal)
		self.comb += self.pred2.end_in.eq(self.pred1.end_out)
		self.comb += self.pred2.multi_row_mode.eq(self.pred1.multi_row_mode_out)
		self.comb += Cat(self.pred2.pred_input_pixels).eq(Cat(self.pred1.pred_output_pixels))
		# pred2 and diff 
		self.comb += Cat(self.diff.pixels_input).eq(Cat(self.pred2.pixels_output))
		self.comb += self.diff.input_valid.eq(self.pred2.output_valid)
		self.comb += self.diff.pause_signal.eq(pause_signal)
		self.comb += self.diff.end_in.eq(self.pred2.end_out)
		self.comb += Cat(self.diff.pred_input_pixels).eq(Cat(self.pred2.pred_output_pixels))
		# diff and main-out
		self.comb += Cat(diff_output_pixels).eq(Cat(self.diff.diff_output_pixels))
		self.comb += output_valid.eq(self.diff.output_valid)
		self.comb += end_out.eq(self.diff.end_out)



if __name__ == "__main__":
	module = predictor_difference_stage()
	print(verilog.convert(module, module.ios))