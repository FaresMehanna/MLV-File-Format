#import python libraries
from migen import *
import random

#import buffer_stage_sequential module
from buffer_stage_sequential import buffer_stage_sequential

#import constants 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import constants




def buffer_stage_sequential_initial_values_test(dut):
	print("buffer_stage_sequential initial_values_test: started.")
	assert (yield dut.pixels_output) == [0 for _ in range(constants.NUM_IO_PIXELS)], 'Error in initial value of pixels_output'
	assert (yield dut.cached_pixels_output) == [0 for _ in range(constants.NUM_IO_PIXELS)], 'Error in initial value of cached_pixels_output'
	assert (yield dut.output_valid) == 0, 'Error in initial value of output_valid'
	assert (yield dut.multi_row_mode) == 0, 'Error in initial value of multi_row_mode'
	assert (yield dut.new_row) == 1, 'Error in initial value of new_row'
	assert (yield dut.input_counter) == 0 , 'Error in initial value of input_counter'
	print("buffer_stage_sequential initial_values_test: succeeded.")




def buffer_stage_sequential_first_row_test(dut):

	print("buffer_stage_sequential first_row_test: started.")
	# generate first row of image of size constants.ENCODER_VIDEO_WIDTH
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(constants.ROW_STEPS)]

	# set data in clk-0
	for inc, pix_in in enumerate(dut.pixels_input):
		yield pix_in.eq(img[0][inc])
	yield dut.input_valid.eq(1)
	yield

	# feed the buffer
	for i in range(constants.ROW_STEPS - 1):
		
		# data input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(img[i+1][inc])
		yield dut.input_valid.eq(1)
		
		# clk
		yield

		# output data check
		assert (yield dut.end_out) == 0, "Error in end_out, expected 0 but 1 found in step: " + str(i)
		assert (yield dut.pixels_output) == img[i], "Error in assertion in step: " + str(i)
		assert (yield dut.multi_row_mode) == 0, "Error in multi_row_mode, expected 0 but 1 found in step: " + str(i)
		assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
		assert (yield dut.cached_pixels_output) == [0 for _ in range(constants.NUM_IO_PIXELS)], "Error in cached_pixels_output, expected array of zeros in step: " + str(i)
		if i == 0:
			assert (yield dut.new_row) == 1, "Error in new_row, expected 1 but 0 found in step: " + str(i)
		else:
			assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)

	# test last step
	i += 1
	yield dut.input_valid.eq(0)
	yield dut.end_in.eq(1)
	yield
	assert (yield dut.end_out) == 0, "Error in end_out, expected 0 but 1 found in step: " + str(i)
	assert (yield dut.multi_row_mode) == 0, "Error in multi_row_mode, expected 0 but 1 found in step: " + str(i)
	assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.cached_pixels_output) == [0 for _ in range(constants.NUM_IO_PIXELS)], "Error in cached_pixels_output, expected array of zeros in step: " + str(i)
	assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)
	assert (yield dut.pixels_output) == img[i], "Error in assertion in step: " + str(i)
	yield
	assert (yield dut.end_out) == 1, "Error in end_out, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.output_valid) == 0, "Error in output_valid, expected 0 but 1 found in step: " + str(i)

	print("buffer_stage_sequential first_row_test: succeeded.")




def buffer_stage_sequential_full_image_test(dut):

	print("buffer_stage_sequential full_image_test: started.")
	# generate full image of size img_size*constants.NUM_IO_PIXELS
	img_size = int(constants.ROW_STEPS * constants.ENCODER_VIDEO_WIDTH / 4)
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]

	# set data in clk-0
	for inc, pix_in in enumerate(dut.pixels_input):
		yield pix_in.eq(img[0][inc])
	yield dut.input_valid.eq(1)
	yield

	# feed the buffer
	for i in range(img_size - 1):
		
		# data input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(img[i+1][inc])
		yield dut.input_valid.eq(1)
		
		# clk
		yield

		# output data check
		if i > constants.ROW_STEPS-1:
			assert (yield dut.pixels_output) == img[i], "Error in assertion in step: " + str(i)
			assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 0 but 1 found in step: " + str(i)
			assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
			assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
			if i%constants.ROW_STEPS == 0:
				assert (yield dut.new_row) == 1, "Error in new_row, expected 1 but 0 found in step: " + str(i)
			else:
				assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)

	# test last step
	i += 1
	yield dut.input_valid.eq(0)
	yield dut.end_in.eq(1)
	yield
	assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 0 but 1 found in step: " + str(i)
	assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
	assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)
	assert (yield dut.pixels_output) == img[i], "Error in assertion in step: " + str(i)
	yield
	assert (yield dut.end_out) == 1, "Error in end_out, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.output_valid) == 0, "Error in output_valid, expected 0 but 1 found in step: " + str(i)

	print("buffer_stage_sequential full_image_test: succeeded.")




def buffer_stage_sequential_full_image_random_pauses_test(dut):

	print("buffer_stage_sequential full_image_random_pauses_test: started.")
	# generate full image of size img_size*constants.NUM_IO_PIXELS
	img_size = int(constants.ROW_STEPS * constants.ENCODER_VIDEO_WIDTH / 4)
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]

	# set data in clk-0
	for inc, pix_in in enumerate(dut.pixels_input):
		yield pix_in.eq(img[0][inc])
	yield dut.input_valid.eq(1)
	yield

	# feed the buffer
	for i in range(img_size - 1):
		
		# data input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(img[i+1][inc])
		yield dut.input_valid.eq(1)
		
		#random pauses
		if random.randint(0,100) < 20:
			yield dut.pause_signal.eq(1)
			# data input
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(img[max(i-8,0)][inc])
			yield dut.input_valid.eq(1)
			yield
			yield
			yield
			yield
			yield
			#check the old output
			if i > constants.ROW_STEPS-1:
				assert (yield dut.pixels_output) == img[i], "Error in img[i] assertion in step: " + str(i)
				assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 1 but 0 found in step: " + str(i)
				assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
				assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
				if i%constants.ROW_STEPS == 0:
					assert (yield dut.new_row) == 1, "Error in new_row, expected 1 but 0 found in step: " + str(i)
				else:
					assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)
			yield dut.pause_signal.eq(0)
			# data input
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(img[i+1][inc])
			yield dut.input_valid.eq(1)
		
		# clk
		yield

		# output data check
		if i > constants.ROW_STEPS-1:
			assert (yield dut.pixels_output) == img[i], "Error in img[i] assertion in step: " + str(i)
			assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 1 but 0 found in step: " + str(i)
			assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
			assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
			if i%constants.ROW_STEPS == 0:
				assert (yield dut.new_row) == 1, "Error in new_row, expected 1 but 0 found in step: " + str(i)
			else:
				assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)

	# test last step
	i += 1
	yield dut.input_valid.eq(0)
	yield dut.end_in.eq(1)
	yield
	assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
	assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)
	assert (yield dut.pixels_output) == img[i], "Error in assertion in step: " + str(i)
	yield
	assert (yield dut.end_out) == 1, "Error in end_out, expected 1 but 0 found in step: " + str(i)
	assert (yield dut.output_valid) == 0, "Error in output_valid, expected 0 but 1 found in step: " + str(i)

	print("buffer_stage_sequential full_image_random_pauses_test: succeeded.")




def buffer_stage_sequential_full_image_random_pauses_invalids_test(dut):

	print("buffer_stage_sequential full_image_random_pauses_invalids_test: started.")
	# generate full image of size img_size*constants.NUM_IO_PIXELS
	img_size = int(constants.ROW_STEPS * constants.ENCODER_VIDEO_WIDTH / 4)
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]

	# feed the buffer
	for i in range(img_size):
		
		# data input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(img[i][inc])
		yield dut.input_valid.eq(1)

		# clk
		yield
		yield dut.input_valid.eq(0)
		#random pauses
		if random.randint(0,100) < 20:
			yield dut.pause_signal.eq(1)
			yield
			yield
			yield
			yield
			yield
			#check the old output
			if i > constants.ROW_STEPS-1:
				assert (yield dut.pixels_output) == img[i], "Error in img[i] assertion in step: " + str(i)
				assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 1 but 0 found in step: " + str(i)
				assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
				assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
				if i%constants.ROW_STEPS == 0:
					assert (yield dut.new_row) == 1, "Error in new_row, expected 1 but 0 found in step: " + str(i)
				else:
					assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)
			yield dut.pause_signal.eq(0)
		yield

		# output data check
		if i > constants.ROW_STEPS-1:
			assert (yield dut.pixels_output) == img[i], "Error in img[i] assertion in step: " + str(i)
			assert (yield dut.multi_row_mode) == 1, "Error in multi_row_mode, expected 1 but 0 found in step: " + str(i)
			assert (yield dut.output_valid) == 1, "Error in output_valid, expected 1 but 0 found in step: " + str(i)
			assert (yield dut.cached_pixels_output) == img[i - constants.ROW_STEPS], "Error in cached_pixels_output, expected array of cached_pixels_output in step: " + str(i)
			if i%constants.ROW_STEPS == 0:
				assert (yield dut.new_row) == 1, "Error in new_row, expected 1 but 0 found in step: " + str(i)
			else:
				assert (yield dut.new_row) == 0, "Error in new_row, expected 0 but 1 found in step: " + str(i)

	print("buffer_stage_sequential full_image_random_pauses_invalids_test: succeeded.")



if __name__ == "__main__":
	dut1 = buffer_stage_sequential()
	run_simulation(dut1, buffer_stage_sequential_initial_values_test(dut1), vcd_name="buffer_stage_sequential_initial_values_test.vcd")
	dut2 = buffer_stage_sequential()
	run_simulation(dut2, buffer_stage_sequential_first_row_test(dut2), vcd_name="buffer_stage_sequential_first_row_test.vcd")
	dut3 = buffer_stage_sequential()
	run_simulation(dut3, buffer_stage_sequential_full_image_test(dut3), vcd_name="buffer_stage_sequential_full_image_test.vcd")
	dut4 = buffer_stage_sequential()
	run_simulation(dut4, buffer_stage_sequential_full_image_random_pauses_test(dut4), vcd_name="buffer_stage_sequential_full_image_random_pauses_test.vcd")
	dut5 = buffer_stage_sequential()
	run_simulation(dut5, buffer_stage_sequential_full_image_random_pauses_invalids_test(dut5), vcd_name="buffer_stage_sequential_full_image_random_pauses_invalids_test.vcd")