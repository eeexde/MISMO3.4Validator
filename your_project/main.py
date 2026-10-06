"""Validate a MISMO 3.4 XML file against the Fannie Mae DU wrapper schema.

Usage:
    python your_project/main.py [XML_PATH] [--xsd XSD_PATH]

Exit codes:
    0  XML is valid
    1  XML failed schema validation
    2  XML/XSD could not be read or parsed
"""
import argparse
import os
import sys

from lxml import etree

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_XML = os.path.join(REPO_ROOT, "your_project", "loan_file.xml")
DEFAULT_XSD = os.path.join(REPO_ROOT, "schemas", "DU_Wrapper_3.4.0_B324.xsd")

EXIT_VALID = 0
EXIT_INVALID = 1
EXIT_ERROR = 2


def load_schema(xsd_path):
    # Parse by path (not file object) so lxml knows the document's base URL
    # and resolves xsd:include/xsd:import relative to the XSD itself.
    return etree.XMLSchema(etree.parse(os.path.abspath(xsd_path)))


def parse_xml(xml_path):
    # Loan files are untrusted input: no entity expansion, no network access.
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    return etree.parse(os.path.abspath(xml_path), parser)


def validate_mismo(xml_path, xsd_path, schema=None):
    """Return (is_valid, errors) where errors is a list of lxml log entries."""
    if schema is None:
        schema = load_schema(xsd_path)
    xml_doc = parse_xml(xml_path)
    is_valid = schema.validate(xml_doc)
    return is_valid, list(schema.error_log)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate MISMO 3.4 DU/ULAD XML files.")
    parser.add_argument("xml", nargs="*", default=[DEFAULT_XML], help="XML file(s) to validate")
    parser.add_argument("--xsd", default=DEFAULT_XSD, help="XSD schema (default: DU wrapper)")
    args = parser.parse_args(argv)

    try:
        schema = load_schema(args.xsd)
    except (OSError, etree.XMLSyntaxError, etree.XMLSchemaParseError) as e:
        print(f"ERROR: could not load schema {args.xsd}: {e}", file=sys.stderr)
        return EXIT_ERROR

    exit_code = EXIT_VALID
    for xml_path in args.xml:
        print(f"Validating {xml_path} ...")
        try:
            is_valid, errors = validate_mismo(xml_path, args.xsd, schema=schema)
        except (OSError, etree.XMLSyntaxError) as e:
            print(f"ERROR: could not parse {xml_path}: {e}", file=sys.stderr)
            exit_code = EXIT_ERROR
            continue

        if is_valid:
            print("VALID: XML conforms to the DU MISMO 3.4 schema.")
        else:
            print(f"INVALID: {len(errors)} schema error(s).")
            for error in errors:
                print(f"  Line {error.line}, col {error.column}: {error.message}")
            exit_code = max(exit_code, EXIT_INVALID)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
