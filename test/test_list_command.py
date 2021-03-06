# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import re
import unittest
from collections import namedtuple

from test.command_testcase import CommandTest
from test.facilities import load_file_to_todolist
from topydo.commands.ListCommand import ListCommand
from topydo.lib.Config import config

# We're searching for 'mock'
# 'mock' was added as 'unittest.mock' in Python 3.3, but PyPy 3 is based on Python 3.2
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock


class ListCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandTest.txt")
        self.terminal_size = namedtuple('terminal_size', ['columns', 'lines'])

    def test_list01(self):
        command = ListCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list03(self):
        command = ListCommand(["Context1"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list04(self):
        command = ListCommand(["-x", "Context1"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list05(self):
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list06(self):
        command = ListCommand(["Project3"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_list07(self):
        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list08(self):
        command = ListCommand(["--", "-project1"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list09(self):
        command = ListCommand(["--", "-project1", "-Drink"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list10(self):
        command = ListCommand(["text1", "2"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list11(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list12(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["-x", "project"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list13(self):
        command = ListCommand(["-x", "--", "-@Context1 +Project2"],
                              self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list14(self):
        config("test/data/listcommand2.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, " |  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n |  4| (C) Drink beer @ home\n |  5| (C) 13 + 29 = 42\n |  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list15(self):
        command = ListCommand(["p:<10"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list16(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|t5c| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|wa5| (C) Drink beer @ home\n|z63| (C) 13 + 29 = 42\n|mfg| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list17(self):
        command = ListCommand(["-x", "id:"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output,
                         "|  3| (C) Baz @Context1 +Project1 key:value\n")
        self.assertEqual(self.errors, "")

    def test_list18(self):
        command = ListCommand(["-x", "date:2014-12-12"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  6| x 2014-12-12 Completed but with date:2014-12-12\n")

    def test_list19(self):
        """ Force showing all tags. """
        config('test/data/listcommand-tags.conf')

        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| (C) Baz @Context1 +Project1 id:1 key:value\n|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list20(self):
        command = ListCommand(["-f text"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list21(self):
        command = ListCommand(["-f invalid"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list22(self):
        """ Handle tag lists with spaces and punctuation."""
        config(p_overrides={('ls', 'hide_tags'): 'p, id'})
        self.todolist = load_file_to_todolist('test/data/ListCommandTagTest.txt')

        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, '|  1| Foo.\n')

    def test_list31(self):
        """ Don't show any todos with -n 0 """
        command = ListCommand(["-n", "0"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_list32(self):
        """ Only show the top todo. """
        command = ListCommand(["-n", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list33(self):
        """ Negative values result in showing all relevent todos. """
        command = ListCommand(["-n", "-1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list34(self):
        """ Test non-integer value for -n """
        config(p_overrides={('ls', 'list_limit'): '2'})

        command = ListCommand(["-n", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n")
        self.assertEqual(self.errors, "")

    def test_list35(self):
        """ -x flag takes precedence over -n """
        command = ListCommand(["-x", "-n", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list36(self):
        command = ListCommand(["-i", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list37(self):
        command = ListCommand(["-i", "1,foo,3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n")
        self.assertEqual(self.errors, "")

    def test_list38(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand(["-i", "1,foo,z63"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|t5c| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|z63| (C) 13 + 29 = 42\n")
        self.assertEqual(self.errors, "")

    def test_list39(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand(["-i", "t5c,foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|t5c| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list40(self):
        command = ListCommand(["(<C)"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list41(self):
        command = ListCommand(["-z", "Zzz"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "option -z not recognized\n")

    def test_list42(self):
        command = ListCommand(["-x", "+Project1", "-id:1"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list43(self):
        """Test basic 'N' parameter."""
        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    def test_list44(self, mock_terminal_size):
        """
        Test 'N' parameter with output longer than available terminal lines.
        """
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")
        mock_terminal_size.return_value = self.terminal_size(80, 23)

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (A) item 1\n| 27| (A) item 27\n|  2| (B) item 2\n| 28| (B) item 28\n|  3| (C) item 3\n| 29| (C) item 29\n|  4| (D) item 4\n| 30| (D) item 30\n|  5| (E) item 5\n| 31| (E) item 31\n|  6| (F) item 6\n| 32| (F) item 32\n|  7| (G) item 7\n| 33| (G) item 33\n|  8| (H) item 8\n| 34| (H) item 34\n|  9| (I) item 9\n| 35| (I) item 35\n| 10| (J) item 10\n| 36| (J) item 36\n| 11| (K) item 11\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    def test_list45(self, mock_terminal_size):
        """Test basic 'N' parameter with nine line terminal."""
        # have 9 lines on the terminal will print 7 items and leave 2 lines
        # for the next prompt
        mock_terminal_size.return_value = self.terminal_size(100, 9)
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (A) item 1\n| 27| (A) item 27\n|  2| (B) item 2\n| 28| (B) item 28\n|  3| (C) item 3\n| 29| (C) item 29\n|  4| (D) item 4\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    def test_list46(self, mock_terminal_size):
        """Test basic 'N' parameter with zero height terminal."""
        # we still print at least 1 item
        mock_terminal_size.return_value = self.terminal_size(100, 0)
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (A) item 1\n")
        self.assertEqual(self.errors, "")

    def test_list47(self):
        command = ListCommand(["created:2015-11-05"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_help(self):
        command = ListCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")


class ListCommandUnicodeTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

    def test_list_unicode1(self):
        """ Unicode filters."""
        command = ListCommand([u"\u25c4"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())

        expected = u"|  1| (C) And some sp\u00e9cial tag:\u25c4\n"

        self.assertEqual(self.output, expected)


class ListCommandJsonTest(CommandTest):
    def test_json(self):
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-f", "json"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.is_dirty())

        jsontext = ""
        with codecs.open('test/data/ListCommandTest.json', 'r',
                         encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")

    def test_json_unicode(self):
        todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

        command = ListCommand(["-f", "json"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.is_dirty())

        jsontext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.json', 'r',
                         encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")


def replace_ical_tags(p_text):
    # replace identifiers with dots, since they're random.
    result = re.sub(r'\bical:....\b', 'ical:....', p_text)
    result = re.sub(r'\bUID:....\b', 'UID:....', result)

    return result


class ListCommandIcalTest(CommandTest):
    def setUp(self):
        self.maxDiff = None

    def test_ical(self):
        todolist = load_file_to_todolist("test/data/ListCommandIcalTest.txt")

        command = ListCommand(["-x", "-f", "ical"], todolist, self.out,
                              self.error)
        command.execute()

        self.assertTrue(todolist.is_dirty())

        icaltext = ""
        with codecs.open('test/data/ListCommandTest.ics', 'r',
                         encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output),
                         replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")

    def test_ical_unicode(self):
        todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

        command = ListCommand(["-f", "ical"], todolist, self.out, self.error)
        command.execute()

        self.assertTrue(todolist.is_dirty())

        icaltext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.ics', 'r',
                         encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output),
                         replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")

if __name__ == '__main__':
    unittest.main()
