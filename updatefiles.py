# Generate final HTML from content

from os.path import isfile
import re
from buildscript_common import DIVIDER_1, DIVIDER_2, realmain

HEADER_PATH = "_common_header.html"
FOOTER_PATH = "_common_footer.html"
HEADER = ""
FOOTER = ""
TITLES_PATH = "titles.txt"
TITLES = {}
TITLE_SEPARATOR = "§"
SRC_SUFFIX = "_content.html"
DST_SUFFIX = ".html"
REGEX = re.compile(r"\$\$\$BUILDSCRIPT\$LINK\$([a-zA-Z0-9]+)\.html\$\$\$")

def get_title(name):
  if name in TITLES:
    return TITLES[name]
  else:
    print("Warning: could not find title: \"" + name + "\", using default!")
    return TITLES["DEFAULT"]

def stick_end(s):
  while len(s) != 0 and s[-1] == "\n":
    s = s[:-1]
  return s

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
  if "DEFAULT" not in TITLES:
    raise ValueError("Default title is missing")
  return stick_end(header), stick_end(footer)

HEADER, FOOTER = load_global()

if __name__ == "__main__":
  realmain("This will generate final HTML from content", transform_content, SRC_SUFFIX, DST_SUFFIX)
