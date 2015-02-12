# coding=utf-8
from unittest import TestCase
from indexed_collation import IndexedCollation


class IndexedCollationTestCase(TestCase):
    def test_english_punctuation(self):
        titles = [u'’Tis Sweet to Sing the Matchless Love', u'Teach Me to Walk in the Light']
        sections = [section[2] for section in IndexedCollation('eng').sections(titles) if section[0] == 'T']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], [u'Teach Me to Walk in the Light', u'’Tis Sweet to Sing the Matchless Love'])

    def test_german_whitespace1(self):
        titles = [u'Gehet tapfer vorwärts', u'Geht hin in alle Welt', u'Geh voran!']
        sections = [section[2] for section in IndexedCollation('deu').sections(titles) if section[0] == 'G']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], [u'Geh voran!', u'Gehet tapfer vorwärts', u'Geht hin in alle Welt'])

    def test_german_whitespace2(self):
        titles = [u'Herrliches Zion, hehr erbaut', u'Herr, wir wollen preisen, loben',
                  u'Herr und Gott der Himmelsheere']
        sections = [section[2] for section in IndexedCollation('deu').sections(titles) if section[0] == 'H']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], [u'Herr und Gott der Himmelsheere', u'Herr, wir wollen preisen, loben',
                                       u'Herrliches Zion, hehr erbaut'])

    def test_latvian(self):
        titles = [u'\u0160ai sabat\u0101', u'Svētā gavēnī']
        sections = [section[2] for section in IndexedCollation('lav').sections(titles) if section[0] == 'S']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], [u'Svētā gavēnī', u'\u0160ai sabat\u0101'])

    # Lithuanian test cases derived from:
    #     http://msdn.microsoft.com/en-us/library/cc194879.aspx

    def test_lithuanian_i_and_y(self):
        titles = [u'yucca', u'yen', u'yuan', u'irdisch']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] == 'I']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], [u'yen', u'irdisch', u'yuan', u'yucca'])

    def test_lithuanian_c(self):
        titles = [u'čučet']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] == u'Č']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0], titles)

    def test_lithuanian_s(self):
        titles = [u'symbol', u'šàran', u'subtle', u'Sietla', u'ślub']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] in [u'S', u'Š']]
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0], [u'Sietla', u'symbol', u'ślub', u'subtle'])
        self.assertEqual(sections[1], [u'šàran'])

    def test_lithuanian_z(self):
        titles = [u'žena', u'zysk']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] in [u'Z', u'Ž']]
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0], [u'zysk'])
        self.assertEqual(sections[1], [u'žena'])
