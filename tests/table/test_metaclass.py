from piccolo.columns.column_types import ForeignKey
from unittest import TestCase

from piccolo.columns import Secret
from piccolo.table import Table

from ..example_app.tables import Band


class TestMetaClass(TestCase):
    def test_tablename(self):
        self.assertEqual(Band._meta.tablename, "band")

    def test_protected_table_names(self):
        """
        Some tablenames are forbidden because they're reserved words in the
        database, and can potentially cause issues.
        """
        with self.assertRaises(ValueError):

            class User(Table):
                pass

        with self.assertRaises(ValueError):

            class MyUser(Table, tablename="user"):
                pass

    def test_help_text(self):
        """
        Make sure help_text can be set for the Table.
        """
        help_text = "The manager of a band."

        class Manager(Table, help_text=help_text):
            pass

        self.assertEqual(Manager._meta.help_text, help_text)

    def test_foreign_key_columns(self):
        """
        Make sure TableMeta.foreign_keys and TableMeta.foreign_key_references
        are setup correctly.
        """

        class TableA(Table):
            pass

        class TableB(Table):
            table_a = ForeignKey(references=TableA)

        self.assertEqual(TableB._meta.foreign_key_columns, [TableB.table_a])
        self.assertEqual(TableA._meta.foreign_key_references, [TableB.table_a])

    def test_secret_columns(self):
        """
        Make sure TableMeta.secret_columns are setup correctly.
        """

        class Classified(Table):
            top_secret = Secret()

        self.assertEqual(
            Classified._meta.secret_columns, [Classified.top_secret]
        )
