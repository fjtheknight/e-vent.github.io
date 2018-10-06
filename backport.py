# Attempt to reconstruct content from final HTML

import re
from buildscript_common import DIVIDER_1, DIVIDER_2, realmain

def make_dollar_regex(s):
  return s.replace("$", r"\$")

SRC_SUFFIX = ".html"
DST_SUFFIX = "_content.html"
REGEX = re.compile(make_dollar_regex(DIVIDER_1) + r"([\s\S]*)" + make_dollar_regex(DIVIDER_2))

def transform_content(content, name):
  search = REGEX.search(content)
  if not search:
    print("Error: \"buildscriptdivider\"s are missing")
    return ""
  result = search.groups()
  if len(result) != 1:
    print("Error: wrong number of dividers. You need to manually backport the changes.")
    return ""
  return result[0]

if __name__ == "__main__":
  realmain("This will reconstruct content from final HTML.", transform_content, SRC_SUFFIX, DST_SUFFIX)
