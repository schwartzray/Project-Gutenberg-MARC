import re
import pymarc
from pymarc import Subfield, Record, Field, MARCWriter
from datetime import datetime
from libgutenberg import GutenbergDatabase
from libgutenberg.DublinCoreMapping import DublinCoreObject
from os.path import join


def stub(dc):
    record = pymarc.Record()
    now = datetime.now()

    # c - Corrected or revised, a - Language material, m - Monograph/Item, 3 - Abbreviated level, u - Unknown
    
    record.leader[5] = 'c'
    record.leader[6] = 'a'
    record.leader[7] = 'm'
    record.leader[17] = '3'
    record.leader[18] = 'u'
   
    field001 = pymarc.Field(tag='001', data=str(dc.project_gutenberg_id))
    record.add_ordered_field(field001)

    field003 = pymarc.Field(tag='003', data='UtSlPG')
    record.add_ordered_field(field003)
    
    # m - Computer file/Electronic resource - Coded data elements relating to either a computer file or an electronic resource in form.

    field006 = pymarc.Field(tag='006', data='m')
    record.add_ordered_field(field006)

    # c - Electronic resource, r - Remote, n - Not applicable
    
    field007 = pymarc.Field(tag='007', data='cr n')
    record.add_ordered_field(field007)

    # 008 in looking at pub date some have a 906 others have a 4 digit year in 260.  Have to write an expression to capture that. If there is a date, use 's' in position 6 then 7-10 for the date. Otherwise '|' for 6 to 10 meaning 'no attempt to code'. Positions 15-17 - Place of publication, production, or execution 'xx#' - No place, unknown, or undetermined.  For position 23 could be o for online or s for electronic.  May have to not code for language. Because database is not coded for MARC lang codes only for ISO639-1--use MARCtag041 instead. Position 39 cataloging source d - Other.

    new_field_value = now.strftime('%y%m%d') + '|||||||||xx |||||o|||||||||||||| d'
    match_found = False

    for att in dc.book.attributes:
     if (att.fk_attriblist == 906 and att.fk_attriblist is not None) or (att.fk_attriblist == 260 and re.search(r'\b\d{4}\b', str(att.fk_attriblist))):
        new_field_value = now.strftime('%y%m%d') + 's' + str(att.text) + '||||||||xx |||||o|||||||||||||| d'
        match_found = True
        break

    if not match_found:
     new_field_value = now.strftime('%y%m%d') + '|||||||||xx |||||o|||||||||||||| d'

    field008 = pymarc.Field(tag='008', data=new_field_value)
    record.add_ordered_field(field008)

      
    for att in dc.book.attributes:
     if att.fk_attriblist == 10:
    
        field010 = pymarc.Field(
            tag='010',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field010)


    field040 = pymarc.Field(
            tag='040',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value='UtSlPG'),
                ]
               )
    record.add_ordered_field(field040)

    if len(dc.languages):
  
        field041 = pymarc.Field(
            tag='041',
            indicators=[' ', '7'],
            subfields=[
                    Subfield(code='a', value=str(lang.id)) for lang in dc.languages
                ] + [
                    Subfield(code='2', value='iso639-1')
                ]
            )
        record.add_ordered_field(field041)


    for att in dc.book.attributes:
     if att.fk_attriblist == 240:
    
        field240 = pymarc.Field(
            tag='240',
            indicators=['1', str(att.nonfiling)],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field240)

    for att in dc.book.attributes:
     if att.fk_attriblist == 246:
    
        field246 = pymarc.Field(
            tag='246',
            indicators=['1', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field246)

    for att in dc.book.attributes:
     if att.fk_attriblist == 250:
    
        field250 = pymarc.Field(
            tag='250',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field250)

    for att in dc.book.attributes:
     if att.fk_attriblist == 300:
    
        field300 = pymarc.Field(
            tag='300',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field300)

    for att in dc.book.attributes:
     if att.fk_attriblist == 440:
    
        field490 = pymarc.Field(
            tag='490',
            indicators=['1', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field490)

    for att in dc.book.attributes:
     if att.fk_attriblist == 440:
    
        field830 = pymarc.Field(
            tag='830',
            indicators=[' ', '0'],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field830)

# need to replace carriage returns.  Tag 500 has multiple lines.

    for att in dc.book.attributes:
     if att.fk_attriblist == 500:
    
        field500 = pymarc.Field(
            tag='500',
            indicators=[' ', " "],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field500)

    for att in dc.book.attributes:
     if att.fk_attriblist == 505:
    
        field505 = pymarc.Field(
            tag='505',
            indicators=['0', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field505)


    for att in dc.book.attributes:
     if att.fk_attriblist == 508:
    
        field508 = pymarc.Field(
            tag='508',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field508)

    for subject in dc.subjects:
    
        field653 = pymarc.Field(
            tag='653',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(subject.subject)),
               ]
               )
        record.add_ordered_field(field653)


    for att in dc.book.attributes:
     if att.fk_attriblist == 904:
    
        field856 = pymarc.Field(
            tag='856',
            indicators=['4', '0'],
            subfields=[
               Subfield(code='a', value=f"https://www.gutenberg.org/ebooks/{str(dc.project_gutenberg_id)}"),
               ]
               )
        record.add_ordered_field(field856)


    for att in dc.book.attributes:
     if att.fk_attriblist == 904:
    
        field856 = pymarc.Field(
            tag='856',
            indicators=['4', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field856)


    # Author name
    num_auths = len(dc.authors)
    if num_auths:
        field100 = pymarc.Field(
            tag='100',
            indicators=['1', ' '],
            subfields=[
                Subfield(code='a', value=dc.format_author_date(dc.authors[0]))  # Can do better
            ]
        )
        record.add_ordered_field(field100)
    if num_auths > 1:
        for auth in dc.authors[1:]:
            field = pymarc.Field(
                tag='700',
                indicators=['1', ' '],
                subfields=[
                    Subfield(code='a', value=dc.format_author_date(auth)),
                    Subfield(code='e', value='joint author.'),
                ]
            )
            record.add_ordered_field(field)


 # Add Subfield to 245 indicating format
 
 
    for att in dc.book.attributes:
      if att.fk_attriblist == 245:
      
          if '\n'in dc.title:

           field245 = pymarc.Field(
            tag='245',
            indicators=['1', str(att.nonfiling)],
            subfields=[
               Subfield(code='a', value=dc.title_no_subtitle),
               Subfield(code='h', value='[electronic resource] :'),
               Subfield(code='b', value=re.sub(r'^[^\n]*\n', '', dc.title).replace('\n', ' ')),
                      ]
         )
          else:
        
           for att in dc.book.attributes:
            if att.fk_attriblist == 245:
               
             field245 = pymarc.Field(
              tag='245',
              indicators=['1', str(att.nonfiling)],
              subfields=[
               Subfield(code='a', value=dc.title_no_subtitle),
               Subfield(code='h', value='[electronic resource]'),
                      ]
         )
          record.add_ordered_field(field245)

    # Publisher, date
      if att.fk_attriblist == 260:
        field260 = pymarc.Field(
            tag='260',
            indicators=[' ', ' '],
            subfields=[
                Subfield(code='a', value=f"{dc.pubinfo.place} :"),
                Subfield(code='b', value=f"{dc.pubinfo.publisher},"),
                Subfield(code='c', value=str(dc.pubinfo.years).replace('[(\'copyright\', \'', 'c').replace('\'), (\'pubdate\', \'', ', ').replace('\'), (\'copyright\', \'', ', c').replace('\')]', '.')),
            ]
        )

        record.add_ordered_field(field260)

    add_license(record, dc)

    return record

def add_license(record, dc):
    if dc.rights:
        # Add 540 field (terms governing use)
        field540 = pymarc.Field(
            tag='540',
            indicators=[' ', ' '],
            subfields=[
                Subfield(code='a', value=dc.rights),
            ]
        )
        record.add_ordered_field(field540)


def add_subject(record, dc):
    if dc.subjects:
     field653 = pymarc.Field(
    	tag='653', 
    	indicators=[' ', ' '],
    	subfields=[
    	    Subfield(code='a', data=dc.subjects),
    	    ]
    	   )
    record.add_ordered_field(field653)


# Generate 100 records
all_records = []  # Create a list to store all records
for i in range(100):
    booknums = list(range(1, 101))  # Replace with your actual book numbers
    dc = DublinCoreObject()
    dc.load_from_database(booknums[i])
    record = stub(dc)
    all_records.append(record)  # Append each record to the list

# Write all records to one file
with open("combined_output.txt100f", "w") as text_file:
    for record in all_records:
        text_file.write(str(record) + "\n")  # Separate records with a newline

print("Combined records written to combined_output.txt")


# Generate 100 records
all_records = []  # Create a list to store all records
for i in range(100):
    booknums = list(range(68995, 69195))  # Replace with your actual book numbers
    dc = DublinCoreObject()
    dc.load_from_database(booknums[i])
    record = stub(dc)
    all_records.append(record)  # Append each record to the list

# Write all records to one file
with open("combined_output.txt69000f", "w") as text_file:
    for record in all_records:
        text_file.write(str(record) + "\n")  # Separate records with a newline

print("Combined records written to combined_output.txt")


all_records = []  # Create a list to store all records

for i in range(100):
    booknums = list(range(68995, 69195))  # Replace with your actual book numbers

    dc = DublinCoreObject()
    dc.load_from_database(booknums[i])

    record = stub(dc)
    all_records.append(record)  # Append each record to the list

# Write all records to one MARC file
with open("combined_output.mrc", "wb") as marc_file:
    writer = MARCWriter(marc_file)
    for record in all_records:
        writer.write(record)
    writer.close()

print("Combined records written to combined_output.mrc")

