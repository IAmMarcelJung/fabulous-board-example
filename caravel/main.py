import pyb
import io_config
import time
import fabulous_demo

# sw = pyb.Switch()
# sw.callback(io_config.run())
# io_config.run()
io_config.run_poweron()
time.sleep(15)
fabulous_demo.run()
