# Generate final HTML from content

from os import listdir, remove
from os.path import isfile
import re

HEADER_PATH = "_common_header.html"
FOOTER_PATH = "_common_footer.html"
HEADER = ""
DIVIDER_1 = "<!--buildscript header-content divider-->"
DIVIDER_2 = "<!--buildscript content-footer divider-->"
FOOTER = ""
TITLES_PATH = "titles.txt"
TITLES = {}
TITLE_SEPARATOR = "§"
REGEX = re.compile(r"\$\$\$BUILDSCRIPT\$LINK\$([a-zA-Z0-9]+)\.html\$\$\$")

def get_title(name):
  if name in TITLES:
    return TITLES[name]
  else:
    print("Warning: could not find title: \"" + name + "\", using default!")
    return TITLES["DEFAULT"]

def stick_end(s):
  return s[:-1] if len(s) != 0 and s[-1] == "\n" else s

def transform_content(content, name):
  sticky = stick_end(content)
  title = get_title(name)
  result = HEADER + DIVIDER_1 + sticky + DIVIDER_2 + FOOTER
  result = result.replace("$$$BUILDSCRIPT$MY_NAME$$$", name)
  result = result.replace("$$$BUILDSCRIPT$TITLE$$$", title)
  result = result.replace("$$$BUILDSCRIPT$LINK$" + name + ".html$$$", "#")
  result = REGEX.sub("\g<1>.html#", result)
  if "$$$BUILDSCRIPT" in result:
    print("Warning: unhandled BUILDSCRIPT transform in: \"" + name + "\"!")
  return result

def process(name):
  print()
  print("Considering \"" + name + "\"")
  ctntname = name + "_content.html"
  trgtname = name + ".html"
  remove(trgtname)
  if isfile(ctntname):
    with open(ctntname, "r") as s:
      content = s.read()
    result = transform_content(content, name)
    with open(trgtname, "w") as d:
      d.write(result)
    
    print("Generated:", trgtname)
  else:
    print("Data file could not be found!:", ctntname)

def check_loaded():
  if not HEADER:
    raise ValueError("Header is empty")
  if not FOOTER:
    raise ValueError("Footer is empty")
  if "DEFAULT" not in TITLES:
    raise ValueError("Default title is missing")

def read_or_error(path, name):
  if not isfile(path):
    raise ValueError("Could not read " + name + ": " + path)
  with open(path, "r") as f:
    return f.read()

def load_global():
  header = read_or_error(HEADER_PATH, "header")
  footer = read_or_error(FOOTER_PATH, "footer")
  titles = read_or_error(TITLES_PATH, "titles")
  for line in titles.split("\n"):
    if "\r" in line:
      raise ValueError("The titles file has been corrupted by Microsoft Windows")
    sections = line.split(TITLE_SEPARATOR)
    if line == "":
      continue
    if len(sections) != 2:
      raise ValueError("Expecting title separator to occur exactly once per line")
    key = sections[0]
    value = sections[1]
    TITLES[key] = value
  return stick_end(header), stick_end(footer)

HEADER, FOOTER = load_global()
check_loaded()

def run():
  check_loaded()
  for f in listdir():
    if f.endswith(".html") and "_" not in f:
      process(f[:-5])

if __name__ == "__main__":
  print("This will generate final HTML from content. This is a destructive operation!")
  confirm = input("Are you sure you want to continue? [y/N]:")
  if confirm == "y":
    run()
  else:
    print("Not running")
