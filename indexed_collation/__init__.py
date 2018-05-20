from __future__ import unicode_literals
import json
import pkg_resources
import re
from icu import Locale, Collator, UnicodeString
from builtins import str


class IndexedCollation:
    def __init__(self, iso639_3):
        try:
            self.spec = json.loads(
                pkg_resources.resource_string(__name__, 'data/{language}.json'.format(language=iso639_3)).decode(
                    'utf-8'))
        except IOError:
            self.spec = json.loads(
                pkg_resources.resource_string(__name__, 'data/{language}.json'.format(language='eng')).decode('utf-8'))

    @property
    def section_titles(self):
        return self.spec.get('section_titles', self.spec.get('index_titles'))

    @property
    def index_titles(self):
        return self.spec.get('index_titles', self.spec.get('section_titles'))

    @property
    def start_strings(self):
        return self.spec.get('start_strings', [self.to_lowercase(title) for title in self.index_titles])

    @property
    def section_classes(self):
        return self.spec.get('section_classes', [0 for _ in self.section_titles])

    @property
    def locale(self):
        return Locale(self.spec['collation'])

    @property
    def collator(self):
        return Collator.createInstance(self.locale)

    def sections(self, iterable, key=None):
        # Create sections
        sections = []
        for index_title, section_title in zip(self.index_titles, self.section_titles):
            sections.append((index_title, section_title, []))

        # Populate sections
        compare = self.collator.compare
        for obj in sorted(iterable, key=lambda obj: self.key_for_sorting(obj, key=key)):
            sections[self.section(obj, cmp=compare, key=key)][2].append(obj)

        # Remove unused classes of sections
        used_classes = set([self.section_classes[i] for i, section in enumerate(sections) if len(section[2]) > 0])
        sections = [section for i, section in enumerate(sections) if self.section_classes[i] in used_classes]

        return sections

    def section(self, obj, cmp, key=None):
        # Change to lowercase, under the assumption that the start_strings are lowercase
        value = self.to_lowercase(self.transformed_for_sorting(obj, key=key))

        start_strings = self.start_strings
        for i, start_string in enumerate(start_strings):
            if i == 0:
                continue

            if cmp(value, start_string) < 0:
                return i - 1

        return len(start_strings) - 1

    def transformed_for_sorting(self, obj, key=None):
        value = key(obj) if key else obj
        # Strip leading punctuation for sorting
        value = re.sub(r'^\W+', '', value, flags=re.UNICODE)
        return value

    def key_for_sorting(self, obj, key=None):
        return self.collator.getSortKey(self.transformed_for_sorting(obj, key=key))

    def to_lowercase(self, value):
        return str(UnicodeString(str(value)).toLower(self.locale))
