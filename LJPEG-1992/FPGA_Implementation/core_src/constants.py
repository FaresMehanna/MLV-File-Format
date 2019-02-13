# ENCODER_VIDEO_WIDTH equal 2 * actual video size
# ENCODER_VIDEO_WIDTH = 512 can encode a video with width 256
# ENCODER_VIDEO_WIDTH must be power of two
# ENCODER_VIDEO_WIDTH must be > NUM_IO_PIXELS
ENCODER_VIDEO_WIDTH = 512

# VIDEO_MAX_BIT_DEPTH must be >= 2
# VIDEO_MAX_BIT_DEPTH must be <= 16
VIDEO_MAX_BIT_DEPTH = 12

# NUM_IO_PIXELS must be power of two
# NUM_IO_PIXELS must be < ENCODER_VIDEO_WIDTH
# If buffer_stage_bayer used, NUM_IO_PIXELS must be also multiple of four
NUM_IO_PIXELS = 16

ROW_STEPS = int(ENCODER_VIDEO_WIDTH/NUM_IO_PIXELS)	#32