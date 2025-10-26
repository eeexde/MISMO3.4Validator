from lxml import etree

try:
    with open('./schemas/DU_Wrapper_3.4.0_B324.xsd', 'rb') as f:
        schema_doc = etree.parse(f)
        schema = etree.XMLSchema(schema_doc)
except etree.XMLSchemaParseError as e:
    for error in e.error_log:
        print(f"Line {error.line}: {error.message}")