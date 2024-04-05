import pyb
import io_config
import time
import fabulous_demo

io_config.run_poweron()

# This is needed to make sure the GPIO configuration is done.
time.sleep(15)
fabulous_demo.run()
