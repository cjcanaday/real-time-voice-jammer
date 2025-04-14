import sounddevice as sd
import numpy as np
from collections import deque
import argparse



# Command line args
parser = argparse.ArgumentParser(description="Real-Time Voice Jammer")
parser.add_argument('--delay', type=float, default=0.3,
                    help='Delay in seconds (default: 0.3)')
parser.add_argument('--samplerate', type=int, default=44100,
                    help='Sample rate in Hz (default: 44100)')
parser.add_argument('--blocksize', type=int, default=2048,
                    help='Block size (default: 2048)')
parser.add_argument('--device', type=int, nargs=2, metavar=('IN', 'OUT'),
                    help='Input and output device IDs (e.g. --device 1 3)')
args = parser.parse_args()

# config values
DELAY = args.delay
SAMPLE_RATE = args.samplerate
BLOCK_SIZE = args.blocksize

DELAY_SAMPLES = int(np.ceil(DELAY * SAMPLE_RATE / BLOCK_SIZE))
BUFFER = deque(maxlen=DELAY_SAMPLES)

def jammer(indata, outdata, frames, time, status):
    if status:
        print(status, flush=True)

    # Store a copy of the current input block
    BUFFER.append(indata.copy())

    if len(BUFFER) == BUFFER.maxlen:
       # if buffer is full, return old audio from DELAY seconds ago
        outdata[:] = BUFFER[0]
    else:
        # if buffer isn't full, return no sound
        outdata[:] = np.zeros_like(indata)


device = args.device if args.device else None

print("Voice Jammer running")
print(f"  Delay: {DELAY}s | Sample Rate: {SAMPLE_RATE} | Block Size: {BLOCK_SIZE}")
print(f"  Using device: {device if device else 'default'}")
print(f"  Blocks delayed: {DELAY_SAMPLES}\n")


try:
    with sd.Stream(device=(1,3),channels=1, dtype='float32', callback=jammer, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE):
        while True:
            pass  # Keep the stream open
except KeyboardInterrupt:
    print("\n Stopped by user.")   

