import io_config
import time
import upload_vga_demo

# This can be used to run the fabulous demo automatically after powering up the Nucleo
# board.

io_config.run_poweron()

# This is needed to make sure the GPIO configuration is done.
time.sleep(15)
upload_vga_demo.run()
