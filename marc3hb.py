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

    # 008 in looking at pub date some have a 906 others have a 4 digit year in 260.  Have to write an expression to capture that. If there is a date, use 'r' in position 6 then 11-14 for the date. Use year in release date for 7 to 10. Positions 15-17 - Place of publication, production, or execution 'utu'.  For position 23 'o' for online.  Not coding for language, because database is not coded for MARC lang codes only for ISO639-1--use MARCtag041 instead. Position 39 cataloging source d - Other.
    
    new_field_value = now.strftime('%y%m%d') + '|||||||||utu|||||o|||||||||||||| d'
    match_found = False

    for att in dc.book.attributes:
     if (att.fk_attriblist == 906 and att.fk_attriblist is not None) or (att.fk_attriblist == 260 and re.search(r'\b\d{4}\b', str(att.fk_attriblist))):
        new_field_value = now.strftime('%y%m%d') + 'r' + str(dc.release_date)[:4] + str(att.text) + 'utu|||||o|||||||||||||| d'
        match_found = True
        break

    if not match_found:
     new_field_value = now.strftime('%y%m%d') + 'r' + str(dc.release_date)[:4] + '||||utu|||||o|||||||||||||| d'

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


    for att in dc.book.attributes:
     if att.fk_attriblist == 20:
    
        field010 = pymarc.Field(
            tag='020',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field020)


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

    field50 = pymarc.Field(
            tag='50',
            indicators=[' ', "4"],
            subfields=[
               Subfield(code='a', value=str(loccs.id)) for loccs in dc.loccs
               ]
               )
    record.add_ordered_field(field50)



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


    field300 = pymarc.Field(
            tag='300',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value='1 online resource :'),
               Subfield(code='b', value='multiple file formats'),
                ]
               )
    record.add_ordered_field(field300)

    field336 = pymarc.Field(
            tag='336',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value='text'),
               Subfield(code='b', value='txt'),
               Subfield(code='2', value='rdacontent'),
                ]
               )
    record.add_ordered_field(field336)

    field337 = pymarc.Field(
            tag='337',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value='computer'),
               Subfield(code='b', value='c'),
               Subfield(code='2', value='rdamedia'),
                ]
               )
    record.add_ordered_field(field337)

    field338 = pymarc.Field(
            tag='338',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value='online resource'),
               Subfield(code='b', value='cr'),
               Subfield(code='2', value='rdacarrier'),
                ]
               )
    record.add_ordered_field(field338)


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
               Subfield(code='a', value=re.sub('\n', ' ', str(att.text))),
               ]
               )
        record.add_ordered_field(field500)
        
    field500 = pymarc.Field(
            tag='500',
            indicators=[' ', " "],
            subfields=[
               Subfield(code='a', value='Release date is ' + str(dc.release_date)),
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

    for att in dc.book.attributes:
     if att.fk_attriblist == 520:
    
        field508 = pymarc.Field(
            tag='520',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field520)

    for att in dc.book.attributes:
     if att.fk_attriblist == 546:
    
        field508 = pymarc.Field(
            tag='546',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(att.text)),
               ]
               )
        record.add_ordered_field(field546)



    for subject in dc.subjects:
    
        field653 = pymarc.Field(
            tag='653',
            indicators=[' ', ' '],
            subfields=[
               Subfield(code='a', value=str(subject.subject)),
               ]
               )
        record.add_ordered_field(field653)


    field856 = pymarc.Field(
            tag='856',
            indicators=['4', '0'],
            subfields=[
               Subfield(code='a', value=f"https://www.gutenberg.org/ebooks/{str(dc.project_gutenberg_id)}"),
                ]
               )
    record.add_ordered_field(field856)

    field264 = pymarc.Field(
            tag='264',
            indicators=[' ', '1'],
            subfields=[
               Subfield(code='a', value='Salt Lake City, UT :'),
               Subfield(code='b', value='Project Gutenberg,'),
               Subfield(code='c', value=str(dc.release_date)[:4]),
                ]
               )
    record.add_ordered_field(field264)

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
          for auth in dc.authors[0:1]:
               if auth.birthdate or auth.deathdate:
                         field100 = pymarc.Field(
                              tag='100',
                              indicators=['1', ' '],
                              subfields=[
                                        Subfield(code='a', value=re.sub(r'\(([^)]+)\)', r'$q(\1)', str(auth.name)+',')),
                                        Subfield(code='d', value=str(auth.birthdate) + '-' + str(auth.deathdate)),   
                              ]
                         )
                         record.add_ordered_field(field100)
               else:
                         field100 = pymarc.Field(
                              tag='100',
                              indicators=['1', ' '],
                              subfields=[
                                        Subfield(code='a', value=re.sub(r'\(([^)]+)\)', r'$q(\1)', str(auth.name))),
                              ]
                         )
                         record.add_ordered_field(field100)
    if num_auths > 1:
          for auth in dc.authors[1:]:
               if auth.birthdate or auth.deathdate:
                         field700 = pymarc.Field(
                              tag='700',
                              indicators=['1', ' '],
                              subfields=[
                                        Subfield(code='a', value=re.sub(r'\(([^)]+)\)', r'$q(\1)', str(auth.name)+',')),
                                        Subfield(code='d', value=str(auth.birthdate) + '-' + str(auth.deathdate)),   
                              ]
                         )
                         record.add_ordered_field(field700)
               else:
                         field700 = pymarc.Field(
                              tag='700',
                              indicators=['1', ' '],
                              subfields=[
                                        Subfield(code='a', value=re.sub(r'\(([^)]+)\)', r'$q(\1)', str(auth.name))),
                              ]
                         )
                         record.add_ordered_field(field700)

#f"{auth.birthdate if auth.birthdate else ''}" + f"{('-'+ auth.deathdate) if auth.birthdate else ''}"

 # Add Subfield to 245 indicating format
 
 
    for att in dc.book.attributes:
      if att.fk_attriblist == 245:
      
          if '\n'in dc.title:

           field245 = pymarc.Field(
            tag='245',
            indicators=['1', str(att.nonfiling)],
            subfields=[
               Subfield(code='a', value=dc.title_no_subtitle + ' :'),
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
                      ]
         )
          record.add_ordered_field(field245)

    # Publisher, date
    for att in dc.book.attributes:
      if att.fk_attriblist == 260:
        field534 = Field(
            tag='534',
            indicators=[' ', ' '],
            subfields=[
                Subfield(code='p', value=f"Originally published:"),
                Subfield(code='c', value=str(dc.pubinfo)),
            ]
        )
        record.add_ordered_field(field534)

        break

    else:
      field534 = Field(
            tag='534',
            indicators=[' ', ' '],
            subfields=[
                Subfield(code='n', value='Original publication data not identified'),
            ]
        )
      record.add_ordered_field(field534)


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
    booknums = list(range(68775, 69195))  # Replace with your actual book numbers
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
    booknums = list(range(1, 101))  # Replace with your actual book numbers

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

