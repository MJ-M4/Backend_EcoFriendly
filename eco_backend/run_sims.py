from src.simulation.hardware_simulator import run_hardware_simulation
from src.simulation.bin_simulator import run_bin_simulation
import time

run_hardware_simulation(interval_seconds=10)
run_bin_simulation(interval_seconds=10)

# Keep the process alive forever
while True:
    time.sleep(1000)