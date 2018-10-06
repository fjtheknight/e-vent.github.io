# Common code shared between backport.py and updatefiles.py

from os import listdir, remove
from os.path import isfile

DIVIDER_1 = "<!--buildscriptdivider$header-content-->"
DIVIDER_2 = "<!--buildscriptdivider$content-footer-->"

def _process(name, transform_content, src_suffix, dst_suffix):
  print()
  print("Considering \"" + name + "\"")
  srcpath = name + src_suffix
  dstpath = name + dst_suffix
  remove(dstpath)
  if isfile(srcpath):
    with open(srcpath, "r") as s:
      content = s.read()
    result = transform_content(content, name) + "\n"
    with open(dstpath, "w") as d:
      d.write(result)
    print("Generated: " + dstpath)
  else:
    print("Error: File could not be found!: " + srcpath)

def _run(transform_content, dst_suffix, src_suffix):
  for f in listdir():
    if f.endswith(".html") and "_" not in f:
      name = f[:-5]
      _process(name, transform_content, dst_suffix, src_suffix)

def realmain(desc, transform_content, src_suffix, dst_suffix):
  print(desc + ". This is a destructive operation!")
  confirm = input("Are you sure you want to continue? [y/N]:")
  if confirm == "y":
    _run(transform_content, src_suffix, dst_suffix)
  else:
    print("Not running")

