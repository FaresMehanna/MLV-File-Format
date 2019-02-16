#import python libraries
from migen import *
import random

#import bayer_to_sequence module
from bayer_to_sequence import bayer_to_sequence

#import constants 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import constants



def convert_image_to_bayer(img):

	img_list = [x for y in img for x in y]
	bayer_img_list = []
	j = int(constants.ENCODER_VIDEO_WIDTH/2)
	rows = int(len(img)/constants.ROW_STEPS)

	for r in range(rows):
		for i in range(0, j, 2):
			bayer_img_list.append(img_list[r*constants.ENCODER_VIDEO_WIDTH+i])
			bayer_img_list.append(img_list[r*constants.ENCODER_VIDEO_WIDTH+i+1])
			bayer_img_list.append(img_list[r*constants.ENCODER_VIDEO_WIDTH+j+i])
			bayer_img_list.append(img_list[r*constants.ENCODER_VIDEO_WIDTH+j+i+1])
	bayer_img = [[bayer_img_list[outer*constants.NUM_IO_PIXELS+inner] for inner in range(constants.NUM_IO_PIXELS)] for outer in range(constants.ROW_STEPS * rows)]
	return bayer_img



def bayer_to_sequence_initial_values_test(dut):
	print("bayer_to_sequence initial_values_test: started.")
	assert (yield dut.output_valid) == 0, 'Error in initial value of output_valid'
	assert (yield dut.input_counter) == 0, 'Error in initial value of input_counter'
	print("bayer_to_sequence initial_values_test: succeeded.")



def bayer_to_sequence_first_row_test(dut):

	print("bayer_to_sequence first_row_test: started.")
	
	# generate first 2 rows of image of size constants.ENCODER_VIDEO_WIDTH
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(constants.ROW_STEPS * 2)]
	bayer_img = convert_image_to_bayer(img)

	CLK = 0
	for i in range(2*constants.ROW_STEPS):

		#set input
		yield dut.input_valid.eq(1)
		yield dut.pause_signal.eq(0)

		# pixels input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(bayer_img[i][inc])

		#Clk
		yield
		CLK +=1
		if i <= constants.ROW_STEPS:
			assert (yield dut.output_valid) == 0, "Error in value of output_valid in step: " + str(i)
		else:
			assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
			assert (yield dut.pixels_output) == img[i-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(i)
	
	for i in range(constants.ROW_STEPS+1):
		#set input
		yield dut.input_valid.eq(1)
		yield dut.pause_signal.eq(0)

		#Clk
		yield
		CLK +=1
		assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
		assert (yield dut.pixels_output) == img[i+constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(i)

	print("bayer_to_sequence first_row_test: succeeded.")



def bayer_to_sequence_full_image_test(dut):

	print("bayer_to_sequence full_image_test: started.")
	# generate full image of size img_size*constants.NUM_IO_PIXELS
	img_size = int(constants.ROW_STEPS * constants.ENCODER_VIDEO_WIDTH / 4)
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]
	bayer_img = convert_image_to_bayer(img)

	# feed the buffer
	CLK = reads = writes = 0
	for i in range(img_size):
		
		#set input
		yield dut.input_valid.eq(1)
		yield dut.pause_signal.eq(0)

		# pixels input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(bayer_img[i][inc])
		writes += 1

		#Clk
		yield
		CLK +=1

		assert (yield dut.end_out) == 0, "Error in value of end_out in step: " + str(i)
		if i > constants.ROW_STEPS:
			assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
			assert (yield dut.pixels_output) == img[i-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(i)
			reads += 1
	#signal end
	yield dut.input_valid.eq(0)
	yield dut.pause_signal.eq(0)
	yield dut.end_in.eq(1)

	#check last bits of data
	for i in range(constants.ROW_STEPS+1):

		#Clk
		yield
		CLK +=1

		assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
		assert (yield dut.end_out) == 0, "Error in value of end_out in step: " + str(CLK-1)
		assert (yield dut.pixels_output) == img[i+img_size-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(CLK-1)
		reads += 1
	#Clk
	yield
	CLK +=1
	assert (yield dut.output_valid) == 0, "Error in value of output_valid in step: " + str(CLK-1)
	assert (yield dut.end_out) == 1, "Error in value of end_out in step: " + str(CLK-1)

	assert reads == writes
	print("bayer_to_sequence full_image_test: succeeded.")



def bayer_to_sequence_full_image_test_random_pauses(dut):

	print("bayer_to_sequence full_image_test_random_pauses: started.")
	# generate full image of size img_size*constants.NUM_IO_PIXELS
	img_size = int(constants.ROW_STEPS * constants.ENCODER_VIDEO_WIDTH / 8)
	img = [[random.randint(0,int(pow(2,constants.VIDEO_MAX_BIT_DEPTH))-1) for _ in range(constants.NUM_IO_PIXELS)] for _ in range(img_size)]
	bayer_img = convert_image_to_bayer(img)

	# feed the buffer
	CLK = reads = writes = pauses = 0
	for i in range(img_size):
		
		#set input
		yield dut.input_valid.eq(1)
		yield dut.pause_signal.eq(0)

		# pixels input
		for inc, pix_in in enumerate(dut.pixels_input):
			yield pix_in.eq(bayer_img[i][inc])
		writes += 1

		#random pauses
		if random.randint(0,100) < 50:
			yield dut.pause_signal.eq(1)
			yield
			yield
			yield
			yield
			assert (yield dut.end_out) == 0, "Error in value of end_out in step: " + str(i)
			if i > constants.ROW_STEPS:
				assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
				assert (yield dut.pixels_output) == img[i-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(i)
			yield
			yield
			# pixels input
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(bayer_img[i][inc])
			yield
			yield dut.pause_signal.eq(0)

		#Clk
		yield
		CLK +=1

		assert (yield dut.end_out) == 0, "Error in value of end_out in step: " + str(i)
		if i > constants.ROW_STEPS:
			assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
			assert (yield dut.pixels_output) == img[i-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(i)
			reads += 1

	#signal end
	yield dut.input_valid.eq(0)
	yield dut.pause_signal.eq(0)
	yield dut.end_in.eq(1)

	#check last bits of data
	for i in range(constants.ROW_STEPS + 1):

		#random pauses
		if random.randint(0,100) < 50:
			yield dut.pause_signal.eq(1)
			yield
			yield
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(img[max(0,i-5)][inc])
			yield
			yield
			assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
			assert (yield dut.pixels_output) == img[i+img_size-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(CLK-1)
			assert (yield dut.end_out) == 0, "Error in value of end_out in step: " + str(CLK-1)
			yield
			yield
			# pixels input
			for inc, pix_in in enumerate(dut.pixels_input):
				yield pix_in.eq(bayer_img[i][inc])
			yield
			yield dut.pause_signal.eq(0)

		#Clk
		yield
		CLK +=1

		assert (yield dut.output_valid) == 1, "Error in value of output_valid in step: " + str(i)
		assert (yield dut.pixels_output) == img[i+img_size-constants.ROW_STEPS-1], "Error in value of pixels_output in step: " + str(CLK-1)
		assert (yield dut.end_out) == 0, "Error in value of end_out in step: " + str(CLK-1)
		reads += 1

	#Clk
	yield
	CLK +=1
	assert (yield dut.output_valid) == 0, "Error in value of output_valid in step: " + str(CLK-1)
	assert (yield dut.end_out) == 1, "Error in value of end_out in step: " + str(CLK-1)

	assert reads == writes
	print("bayer_to_sequence full_image_test_random_pauses: succeeded.")



if __name__ == "__main__":
	dut1 = bayer_to_sequence()
	run_simulation(dut1, bayer_to_sequence_initial_values_test(dut1), vcd_name="bayer_to_sequence_initial_values_test.vcd")
	dut2 = bayer_to_sequence()
	run_simulation(dut2, bayer_to_sequence_first_row_test(dut2), vcd_name="bayer_to_sequence_first_row_test.vcd")
	dut3 = bayer_to_sequence()
	run_simulation(dut3, bayer_to_sequence_full_image_test(dut3), vcd_name="bayer_to_sequence_full_image_test.vcd")
	dut4 = bayer_to_sequence()
	run_simulation(dut4, bayer_to_sequence_full_image_test_random_pauses(dut4), vcd_name="bayer_to_sequence_full_image_test_random_pauses.vcd")