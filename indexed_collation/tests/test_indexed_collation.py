# coding=utf-8
from __future__ import unicode_literals
from unittest import TestCase
from indexed_collation import IndexedCollation


class IndexedCollationTestCase(TestCase):
    def test_english_punctuation(self):
        titles = ['’Tis Sweet to Sing the Matchless Love', 'Teach Me to Walk in the Light']
        sections = [section[2] for section in IndexedCollation('eng').sections(titles) if section[0] == 'T']
        self.assertEqual(1, len(sections))
        self.assertEqual(['Teach Me to Walk in the Light', '’Tis Sweet to Sing the Matchless Love'], sections[0])

    def test_german_whitespace1(self):
        titles = ['Gehet tapfer vorwärts', 'Geht hin in alle Welt', 'Geh voran!']
        sections = [section[2] for section in IndexedCollation('de').sections(titles) if section[0] == 'G']
        self.assertEqual(1, len(sections))
        self.assertEqual(['Geh voran!', 'Gehet tapfer vorwärts', 'Geht hin in alle Welt'], sections[0])

    def test_german_whitespace2(self):
        titles = ['Herrliches Zion, hehr erbaut', 'Herr, wir wollen preisen, loben',
                  'Herr und Gott der Himmelsheere']
        sections = [section[2] for section in IndexedCollation('de').sections(titles) if section[0] == 'H']
        self.assertEqual(1, len(sections))
        self.assertEqual(['Herr und Gott der Himmelsheere', 'Herr, wir wollen preisen, loben',
                          'Herrliches Zion, hehr erbaut'], sections[0])

    def test_latvian(self):
        titles = ['\u0160ai sabat\u0101', 'Svētā gavēnī']
        sections = [section[2] for section in IndexedCollation('lav').sections(titles) if section[0] == 'S']
        self.assertEqual(1, len(sections))
        self.assertEqual(['Svētā gavēnī', '\u0160ai sabat\u0101'], sections[0])

    # Lithuanian test cases derived from:
    #     http://msdn.microsoft.com/en-us/library/cc194879.aspx

    def test_lithuanian_i_and_y(self):
        titles = ['yucca', 'yen', 'yuan', 'irdisch']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] == 'I']
        self.assertEqual(1, len(sections))
        self.assertEqual(['yen', 'irdisch', 'yuan', 'yucca'], sections[0])

    def test_lithuanian_c(self):
        titles = ['čučet']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] == 'Č']
        self.assertEqual(1, len(sections))
        self.assertEqual(titles, sections[0])

    def test_lithuanian_s(self):
        titles = ['symbol', 'šàran', 'subtle', 'Sietla', 'ślub']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] in ['S', 'Š']]
        self.assertEqual(2, len(sections))
        self.assertEqual(['Sietla', 'symbol', 'ślub', 'subtle'], sections[0])
        self.assertEqual(['šàran'], sections[1])

    def test_lithuanian_z(self):
        titles = ['žena', 'zysk']
        sections = [section[2] for section in IndexedCollation('lit').sections(titles) if section[0] in ['Z', 'Ž']]
        self.assertEqual(2, len(sections))
        self.assertEqual(['zysk'], sections[0])
        self.assertEqual(['žena'], sections[1])

    def test_japanese(self):
        titles = ['システム', 'プログラムの追加と削除', 'フォント']
        sections = [section[2] for section in IndexedCollation('jpn').sections(titles) if section[0] in ['さ', 'は']]
        self.assertEqual(2, len(sections))
        self.assertEqual(['システム'], sections[0])
        self.assertEqual(['フォント', 'プログラムの追加と削除'], sections[1])
