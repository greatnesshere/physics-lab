from configparser import ConfigParser
import os.path,glob
from sys import argv
FILE=argv[1]
cfg=ConfigParser()
cfg.read(
    FILE,
    encoding="utf-8"
)
# TODO: refactor as needed for now
for ent in cfg["applies to"]:
    print(ent)