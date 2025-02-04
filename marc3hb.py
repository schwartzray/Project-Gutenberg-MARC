'''
 code to write a Marc file from the Project Gutenberg database
'''

import re
from datetime import datetime

import pymarc
from pymarc import Subfield, Record, Field, MARCWriter
from sqlalchemy import select
from sqlalchemy import not_

from libgutenberg.Models import Book
from libgutenberg import GutenbergDatabase
from libgutenberg.DublinCoreMapping import DublinCoreObject

OB = GutenbergDatabase.Objectbase(False)

# compiling a regular expression is a bit of work, only do it once.
RE_NAME_PAREN = re.compile(r'(\s*\([^)]*\))')

def auth_paren(a_name):
    """
    deal with parentheses in author name : 'Ray S. (Librarian)' -> 'Ray S.', ' (Librarian)'
    """
    nm = RE_NAME_PAREN.search(a_name)
    if nm:
        return a_name.replace(nm.group(1), ''), nm.group(1).strip()
    return a_name, None


def auth_dates(author):
    """format the author birth and death dates"""
    def format_dates(d1, d2):
        """ Format dates """
        # Hack to display 9999? if only d2 is set
        if d2 and not d1:
            if d2 < 0:
                # remember, the was no year 0; 0 represents 1 BCE
                return "%d? BCE" % abs(d2 - 1)
            return "%d?" % d2
        if not d1:
            return ''
        if d2 and d1 != d2:
            d3 = max(d1, d2)
            if d3 < 0:
                return "%d? BCE" % abs(d3 - 1)
            return "%d?" % d3
        if d1 < 0:
            return "%d BCE" % abs(d1 - 1)
        return str(d1)

    born = format_dates(author.birthdate, author.birthdate2)
    died = format_dates(author.deathdate, author.deathdate2)
    return f',{born}-{died}'

# book_record function definiton

def book_record(dc):
    # Make sure the dc object exists in db
    if not dc.book:
        print(f"No book for {dc}")
        return None

    # Make sure the dc object is of type 'text'
    for category in dc.categories:
        print(f"{dc.book.pk} is a {category}")
        return None

    record = pymarc.Record()
    now = datetime.now()

    # c - Corrected or revised, a - Language material, m - Monograph/Item,
    # 3 - Abbreviated level, u - Unknown

    record.leader[5] = 'c'
    record.leader[6] = 'a'
    record.leader[7] = 'm'
    record.leader[17] = '3'
    record.leader[18] = 'u'

    field001 = pymarc.Field(tag='001', data=str(dc.project_gutenberg_id))
    record.add_ordered_field(field001)

    field003 = pymarc.Field(tag='003', data='UtSlPG')
    record.add_ordered_field(field003)

    # m - Computer file/Electronic resource - Coded data elements relating to either a computer
    # file or an electronic resource in form.

    field006 = pymarc.Field(tag='006', data='m')
    record.add_ordered_field(field006)

    # c - Electronic resource, r - Remote, n - Not applicable

    field007 = pymarc.Field(tag='007', data='cr n')
    record.add_ordered_field(field007)

    # 008 in looking at pub date some have a 906 others have a 4 digit year in 260.
    # Have to write an expression to capture that.
    # If there is a date, use 'r' in position 6 then 11-14 for the date.
    # Use year in release date for 7 to 10. Positions 15-17 - Place of publication, production, or
    # execution 'utu'.  For position 23 'o' for online.  Not coding for language, because database
    # is not coded for MARC lang codes only for ISO639-1--use MARCtag041 instead.
    # Position 39 cataloging source d - Other.

    new_field_value = now.strftime('%y%m%d') + '|||||||||utu|||||o|||||||||||||| d'
    match_found = False

    for att in dc.book.attributes:
        if att.fk_attriblist == 906 or (att.fk_attriblist == 260 
            and re.search(r'\b\d{4}\b', str(att.fk_attriblist))):
            new_field_value = now.strftime('%y%m%d') + 'r' + str(dc.release_date)[:4] \
                + str(att.text) + 'utu|||||o|||||||||||||| d'
            match_found = True
            break

    if not match_found:
        new_field_value = now.strftime('%y%m%d') + 'r' + str(dc.release_date)[:4] \
            + '||||utu|||||o|||||||||||||| d'

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


        if att.fk_attriblist == 20:

            field020 = pymarc.Field(
                tag='020',
                indicators=[' ', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field020)

        if att.fk_attriblist == 240:

            field240 = pymarc.Field(
                tag='240',
                indicators=['1', str(att.nonfiling)],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field240)

        if att.fk_attriblist == 246:

            field246 = pymarc.Field(
                tag='246',
                indicators=['1', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field246)

        if att.fk_attriblist == 250:

            field250 = pymarc.Field(
                tag='250',
                indicators=[' ', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field250)

        if att.fk_attriblist == 300:

            field300 = pymarc.Field(
                tag='300',
                indicators=[' ', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field300)

        if att.fk_attriblist == 440:

            field490 = pymarc.Field(
                tag='490',
                indicators=['1', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field490)

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

        if att.fk_attriblist == 500:

            field500 = pymarc.Field(
                tag='500',
                indicators=[' ', " "],
                subfields=[
                    Subfield(code='a', value=re.sub('\n', ' ', str(att.text))),
                    ]
                )
            record.add_ordered_field(field500)

        if att.fk_attriblist == 505:

            field505 = pymarc.Field(
                tag='505',
                indicators=['0', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field505)


        if att.fk_attriblist == 508:

            field508 = pymarc.Field(
                tag='508',
                indicators=[' ', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field508)

        if att.fk_attriblist == 520:

            field520 = pymarc.Field(
                tag='520',
                indicators=[' ', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field520)

        if att.fk_attriblist == 521:

            field520 = pymarc.Field(
                tag='521',
                indicators=['8', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field521)


        if att.fk_attriblist == 546:

            field546 = pymarc.Field(
                tag='546',
                indicators=[' ', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field546)

        if att.fk_attriblist == 904:

            field856 = pymarc.Field(
                tag='856',
                indicators=['4', ' '],
                subfields=[
                    Subfield(code='a', value=str(att.text)),
                    ]
                )
            record.add_ordered_field(field856)

        if att.fk_attriblist == 245:

            if '\n'in dc.title:
                subfields = [
                   Subfield(code='a', value=dc.title_no_subtitle + ' :'),
                   Subfield(code='b', value=re.sub(r'^[^\n]*\n', '', dc.title).replace('\n', ' ')),
                   ]
            else:
                subfields = [
                    Subfield(code='a', value=dc.title_no_subtitle),
                    ]

            field245 = pymarc.Field(
                tag='245',
                indicators=['1', str(att.nonfiling)],
                subfields=subfields
                )
            record.add_ordered_field(field245)

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

    field500 = pymarc.Field(
        tag='500',
        indicators=[' ', " "],
        subfields=[
            Subfield(code='a', value='Release date is ' + str(dc.release_date)),
            ]
        )
    record.add_ordered_field(field500)

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
            Subfield(
                code='a',
                value=f"https://www.gutenberg.org/ebooks/{str(dc.project_gutenberg_id)}"
                )
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


    # Author name
    first_auth = True
    for auth in dc.authors:
        authname, paren = auth_paren(auth.name)
        subfields = [Subfield(code='a', value=authname)]
        if paren:
            subfields.append(Subfield(code='q', value=' ' + paren))
        if auth.birthdate or auth.deathdate:
            subfields.append(Subfield(code='d', value=auth_dates(auth)))
        field = pymarc.Field(
            tag='100' if first_auth else '700',
            indicators=['1', ' '],
            subfields=subfields
        )
        first_auth = False
        record.add_ordered_field(field)


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

    return record

MAXBOOKNUM = 1000

def main():
    session = OB.get_session()
    start = datetime.now()
    booknums = session.execute(select(Book.pk).filter(not_(Book.categories.any())))

    # Write all records to one MARC file
    with open("combined_output1000.mrc", "wb") as marc_file:
        writer = MARCWriter(marc_file)
        for booknum in booknums:

            dc = DublinCoreObject(session=session)
            dc.load_from_database(booknum.pk, load_files=False)  # booknum is a tuple: (pk,)

            record = book_record(dc)
            # Check if the record is a valid pymarc.Record object
            if isinstance(record, Record):
                writer.write(record)
            else:
                print(f"Skipping invalid record for book number {booknum.pk}")
            if booknum.pk > MAXBOOKNUM:
                break
        writer.close()
    elapsed = datetime.now() - start
    print(f"Combined records written to combined_output.mrc in {elapsed}")

# boilerplate for main method
if __name__ == '__main__':
    main ()
