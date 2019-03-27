#!/usr/bin/python

import xmlschema

format1 = xmlschema.XMLSchema('xsd/package_format1.xsd')
format2 = xmlschema.XMLSchema('xsd/package_format2.xsd')
format3 = xmlschema.XMLSchema('xsd/package_format3.xsd')

print("Format1: ", format1.validity)
print("Format2: ", format2.validity)
print("Format3: ", format3.validity)
