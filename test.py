# http://gokhanatil.com/2017/11/python-for-data-science-importing-xml-to-pandas-dataframe.html
import pandas as pd
import xml.etree.cElementTree as et
import zipfile

df_json = pd.read_json('test.json')
print (df_json)

df_csv = pd.read_csv('test.csv')
print(df_csv)

df_xls = pd.read_excel('test.xlsx')
print(df_xls)

df_json_raw = pd.read_json('test.json')
df_json = df_json_raw.apply(lambda x: pd.Series([x[0]['name'], x[0]['email']]), axis=1)
df_json.columns = ['name', 'email']
print (df_json)

with zipfile.ZipFile("D:/Python/MiscProc/test.zip") as z:
    list = z.namelist()
    with z.open(list[0]) as f:
        for line in f:
            line = line.decode()
            print(line)




def getvalueofnode(node):
    """ return node text or None """
    return node.text if node is not None else None


def main():
    """ main """
    print("parse xml")
    parsed_xml = et.parse("test.xml")
    dfcols = ['name', 'email', 'phone', 'street']
    df_xml = pd.DataFrame(columns=dfcols)

    for node in parsed_xml.getroot():
        name = node.attrib.get('name')
        email = node.find('email')
        phone = node.find('phone')
        street = node.find('address/street')

        df_xml = df_xml.append(
            pd.Series([name, getvalueofnode(email), getvalueofnode(phone),
                       getvalueofnode(street)], index=dfcols),
            ignore_index=True)

    print (df_xml)
    for index, row in df_xml.iterrows():
        print (row['name'], row['email'], row['phone'], row['street'])

def parseWikipedia():
    print("parse Wikipedia")
    parsed_xml = et.parse("D:/Wikipedia/arwiki-20160111-corpus-sample.xml")
    #<article name="ماء">
    #<crosslanguage_link language="en" name="Water"/>
    dfcols = ['ar', 'en']
    df_xml = pd.DataFrame(columns=dfcols)

    for node in parsed_xml.getroot():
        article = node.find('article')
        crosslanguage_link = node.find('crosslanguage_link')

        ar = ""
        en = ""
        name = node.attrib.get('name')

        df_xml = df_xml.append(
            pd.Series([ar, getvalueofnode(en)], index=dfcols), ignore_index=True)

    print (df_xml)
    for index, row in df_xml.iterrows():
        print (row['ar'], row['en'])

if __name__ == '__main__':
    main()
    parseWikipedia()