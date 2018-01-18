import xml.etree.ElementTree as ET

data = '''
<person>
  <name>Chuck</name>
  <phone type="intl">
     +1 734 303 4456
   </phone>
   <email hide="yes"/>
</person>'''

tree = ET.fromstring(data)
print(tree.find('name').__str__)
print('Name:', tree.find('name').text)
print('Attr:', tree.find('phone').get('type'))
print('Attr:', tree.find('phone').text)
print('Attr:', tree.find('email').get('hide'))
