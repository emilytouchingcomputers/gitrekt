# gitrekt

# github codesearch for recon

To add dependencies (ESP32 SDK, u8g2, MicroPython, etc.):

`git submodule update --init --recursive`

If you need to set up the ESP32 development environment,
follow step 1: https://esp-idf.readthedocs.io/en/v2.0/linux-setup.html

`cd components/micropython/micropython-esp32/mpy-cross/ && make clean && make && cd -`

To build and flash firmware:

`cd firmware/esp32`

`make`

`make flash` OR

`python esptool/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader.bin 0x10000 cpv2017.bin 0x8000 partitions.bin`

# TODO:
Possible off-by-one issues when catching errors.  Page count seems to be off.



#I think this line turns the normal API responses into prettified JSON.  Unsure.

#cat json.txt | python -m json.tool >> pretty.txt


HOW TO USE GIT HOLY CRAP

git clone (repoURL)

git pull origin master

git add file_i_changed

git commit -m "comments"

git commit

git push
