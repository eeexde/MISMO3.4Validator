from lxml import etree
import os

def validate_mismo(xml_path, xsd_path):
    try:
        xml_path = os.path.abspath(xml_path)
        xsd_path = os.path.abspath(xsd_path)
        os.chdir(os.path.dirname(xsd_path))  # 👈 ensures relative imports in XSD work

        # Parse DU Wrapper XSD schema
        with open(xsd_path, 'rb') as xsd_file:
            xmlschema_doc = etree.parse(xsd_file)
            xmlschema = etree.XMLSchema(xmlschema_doc)

        # Parse MISMO XML
        with open(xml_path, 'rb') as xml_file:
            xml_doc = etree.parse(xml_file)

        # Validate XML
        print("Validating MISMO 3.4 DU/ULAD XML, please wait...")
        if xmlschema.validate(xml_doc):
            print("✅ XML is valid according to DU MISMO 3.4 schema.")
        else:
            print("❌ XML validation failed.")
            for error in xmlschema.error_log:
                print(f"Line {error.line}: {error.message}")

    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    xml_path = "./your_project/loan_file.xml"
    xsd_path = "./schemas/DU_Wrapper_3.4.0_B324.xsd"
    validate_mismo(xml_path, xsd_path)
