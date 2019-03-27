#!/usr/bin/python

import xmlschema

format1 = xmlschema.XMLSchema('xsd/package_format1.xsd')
print("'xsd/package_format1.xsd' file is valid.")
format2 = xmlschema.XMLSchema('xsd/package_format2.xsd')
print("'xsd/package_format2.xsd' file is valid.")
format3 = xmlschema.XMLSchema('xsd/package_format3.xsd')
print("'xsd/package_format3.xsd' file is valid.")
