"""Check that the DU wrapper XSD and everything it includes/imports compiles."""
import os
import sys

from lxml import etree

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XSD_PATH = os.path.join(REPO_ROOT, "schemas", "DU_Wrapper_3.4.0_B324.xsd")

try:
    etree.XMLSchema(etree.parse(XSD_PATH))
except etree.XMLSchemaParseError as e:
    for error in e.error_log:
        print(f"Line {error.line}: {error.message}")
    sys.exit(1)

print(f"Schema OK: {XSD_PATH}")
