from configparser import ConfigParser
from pathlib import Path
from sys import argv
from argparse import ArgumentParser
parser=ArgumentParser(
    prog="build",
    description="refactor relevant files"
)
parser.add_argument("filename")
args=parser.parse_args()
FILE=Path(args.filename)
cfg=ConfigParser()
cfg.read(FILE,encoding="utf-8")
print(FILE.parent)
for target in FILE.parent.glob(cfg["applies to"]["pattern"]):
    with open(target,mode="r+",encoding="utf-8") as file:
        formatted_contents=file.read().format(
            **dict(cfg["settings"])
        )
