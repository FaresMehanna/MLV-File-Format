#import python libraries
from migen import *
import random

#import predictor_difference_stage module
from predictor_difference_stage import predictor_difference_stage

#import constants 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import constants



def predictor_difference_stage_initial_values_test(dut):
	print("predictor_difference_stage initial_values_test: started.")
	assert (yield dut.output_valid) == 0, 'Error in initial value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in initial value of end_out'
	print("predictor_difference_stage initial_values_test: succeeded.")



def pred_diff_img(img, rows_size, rows_count, bit_depth, num_io_pixels):
	
	img_list = [x for y in img for x in y]
	pred_img_list = []
	row_elements = rows_size*num_io_pixels

	#do the first row
	if rows_count > 0:
		for pixel_index in range(row_elements):
			if pixel_index == 0:
				pred_img_list.append(img_list[pixel_index] - 2**(bit_depth-1))
			else:
				pred_img_list.append(img_list[pixel_index] - (img_list[pixel_index-1]>>1))

	#do rest of rows
	for row in range(1, rows_count):
		for cell in range(row_elements):
			if cell == 0:
				pred_img_list.append(img_list[row*row_elements+cell] - img_list[(row-1)*row_elements+cell])
			else:
				pred_img_list.append(img_list[row*row_elements+cell] - (img_list[(row-1)*row_elements+cell] + (img_list[row*row_elements+cell-1]>>1) - (img_list[(row-1)*row_elements+cell-1]>>1)))

	pred_img = [[pred_img_list[outer*constants.NUM_IO_PIXELS+inner] for inner in range(constants.NUM_IO_PIXELS)] for outer in range(len(img))]
	return pred_img



def predictor_difference_stage_sanity_test(dut):

	print("predictor_difference_stage sanity_test: started.")
	# every 3 steps represent single row
	rows_size = 3
	rows_count = 4
	img_size = rows_size * rows_count
	# create img with 12 steps
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]
	img_ctr = 0
	pred_img = pred_diff_img(img, rows_size, rows_count, constants.VIDEO_MAX_BIT_DEPTH, constants.NUM_IO_PIXELS)
	pred_img_result = []
	# send first row
	# send first part of first row
	yield dut.multi_row_mode.eq(0)
	yield dut.new_row.eq(1)
	yield dut.pause_signal.eq(0)
	yield dut.input_valid.eq(1)
	for inc, pix_in in enumerate(dut.pixels_input):
		yield pix_in.eq(img[img_ctr][inc])
	img_ctr += 1
	yield
	assert (yield dut.output_valid) == 0, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	# send rest of parts of first row
	for i in range(rows_size-1):
		yield dut.multi_row_mode.eq(0)
		yield dut.new_row.eq(0)
		yield dut.pause_signal.eq(0)
		yield dut.input_valid.eq(1)
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(img[img_ctr][inc])
		img_ctr += 1
		yield
		assert (yield dut.output_valid) == 0, 'Error in value of output_valid'
		assert (yield dut.end_out) == 0, 'Error in value of end_out'
	# send 2,3,4 rows
	offset_img_ctr = img_ctr
	for row in range(rows_count-1):
		n_row = 1
		for cell in range(rows_size):
			yield dut.multi_row_mode.eq(1)
			yield dut.new_row.eq(n_row)
			yield dut.pause_signal.eq(0)
			yield dut.input_valid.eq(1)
			for inc, pix_in in enumerate(dut.cached_pixels_input):
				yield pix_in.eq(img[img_ctr-offset_img_ctr][inc])
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(img[img_ctr][inc])
			img_ctr += 1
			yield
			assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
			assert (yield dut.end_out) == 0, 'Error in value of end_out'
			pred_img_result.append((yield dut.diff_output_pixels))
			n_row = 0
	#end the stream
	yield dut.input_valid.eq(0)
	yield dut.end_in.eq(1)
	yield
	assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	pred_img_result.append((yield dut.diff_output_pixels))
	yield
	assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	pred_img_result.append((yield dut.diff_output_pixels))
	yield
	assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	pred_img_result.append((yield dut.diff_output_pixels))
	yield
	assert (yield dut.output_valid) == 0, 'Error in value of output_valid'
	assert (yield dut.end_out) == 1, 'Error in value of end_out'
	assert pred_img == pred_img_result, 'Error in diff-predicted data'
	print("predictor_difference_stage sanity_test: succeeded.")



def predictor_difference_stage_random_pauses_test(dut):

	def rand_pause_check(dut, valid, end):
		#random pauses
		if random.randint(0,100) < 90:
			yield dut.pause_signal.eq(1)
			yield
			yield
			assert (yield dut.output_valid) == valid, 'Error in value of output_valid'
			assert (yield dut.end_out) == end, 'Error in value of end_out'
			yield
			yield
			yield
			yield dut.pause_signal.eq(0)

	print("predictor_difference_stage random_pauses_test: started.")
	# every 3 steps represent single row
	rows_size = 3
	rows_count = 4
	img_size = rows_size * rows_count
	# create img with 12 steps
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]
	img_ctr = 0
	pred_img = pred_diff_img(img, rows_size, rows_count, constants.VIDEO_MAX_BIT_DEPTH, constants.NUM_IO_PIXELS)
	pred_img_result = []
	#random pauses
	rand_pause_check(dut, 0, 0)
	# send first row
	# send first part of first row
	yield dut.multi_row_mode.eq(0)
	yield dut.new_row.eq(1)
	yield dut.pause_signal.eq(0)
	yield dut.input_valid.eq(1)
	for inc, pix_in in enumerate(dut.pixels_input):
		yield pix_in.eq(img[img_ctr][inc])
	img_ctr += 1
	yield
	assert (yield dut.output_valid) == 0, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	# send rest of parts of first row
	for i in range(rows_size-1):
		#random pauses
		rand_pause_check(dut, 0, 0)
		#data input
		yield dut.multi_row_mode.eq(0)
		yield dut.new_row.eq(0)
		yield dut.pause_signal.eq(0)
		yield dut.input_valid.eq(1)
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(img[img_ctr][inc])
		img_ctr += 1
		yield
		assert (yield dut.output_valid) == 0, 'Error in value of output_valid'
		assert (yield dut.end_out) == 0, 'Error in value of end_out'
	# send 2,3,4 rows
	offset_img_ctr = img_ctr
	for row in range(rows_count-1):
		n_row = 1
		for cell in range(rows_size):
			#random pauses
			rand_pause_check(dut, 1, 0)
			#data input
			yield dut.multi_row_mode.eq(1)
			yield dut.new_row.eq(n_row)
			yield dut.pause_signal.eq(0)
			yield dut.input_valid.eq(1)
			for inc, pix_in in enumerate(dut.cached_pixels_input):
				yield pix_in.eq(img[img_ctr-offset_img_ctr][inc])
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(img[img_ctr][inc])
			img_ctr += 1
			yield
			assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
			assert (yield dut.end_out) == 0, 'Error in value of end_out'
			pred_img_result.append((yield dut.diff_output_pixels))
			n_row = 0
	#end the stream
	yield dut.input_valid.eq(0)
	yield dut.end_in.eq(1)
	rand_pause_check(dut, 1, 0)
	yield
	rand_pause_check(dut, 1, 0)
	assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	pred_img_result.append((yield dut.diff_output_pixels))
	rand_pause_check(dut, 1, 0)
	yield
	rand_pause_check(dut, 1, 0)
	assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	pred_img_result.append((yield dut.diff_output_pixels))
	rand_pause_check(dut, 1, 0)
	yield
	rand_pause_check(dut, 1, 0)
	assert (yield dut.output_valid) == 1, 'Error in value of output_valid'
	assert (yield dut.end_out) == 0, 'Error in value of end_out'
	pred_img_result.append((yield dut.diff_output_pixels))
	rand_pause_check(dut, 1, 0)
	yield
	rand_pause_check(dut, 0, 1)
	assert (yield dut.output_valid) == 0, 'Error in value of output_valid'
	assert (yield dut.end_out) == 1, 'Error in value of end_out'
	assert pred_img == pred_img_result, 'Error in diff-predicted data'
	print("predictor_difference_stage random_pauses_test: succeeded.")



if __name__ == "__main__":
	dut1 = predictor_difference_stage()
	run_simulation(dut1, predictor_difference_stage_initial_values_test(dut1), vcd_name="predictor_difference_stage_initial_values_test.vcd")
	dut2 = predictor_difference_stage()
	run_simulation(dut2, predictor_difference_stage_sanity_test(dut2), vcd_name="predictor_difference_stage_sanity_test.vcd")
	dut3 = predictor_difference_stage()
	run_simulation(dut3, predictor_difference_stage_random_pauses_test(dut3), vcd_name="predictor_difference_stage_random_pauses_test.vcd")