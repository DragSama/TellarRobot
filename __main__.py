from TellarBot import client
from TellarBot.plugins import TO_LOAD

import importlib

for LOAD in TO_LOAD:
    importlib.import_module("TellarBot.plugins." + LOAD)

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
