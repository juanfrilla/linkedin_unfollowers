from halo import Halo
from time import sleep

spinner = Halo(text='Loading', spinner='shark')
spinner.start()

# Run time consuming work here
# You can also change properties for spinner as and when you want
for num in range(1,50):
    sleep(1)

spinner.stop()