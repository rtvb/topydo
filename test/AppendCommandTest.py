# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import AppendCommand
import CommandTest
import TodoList

class AppendCommandTest(CommandTest.CommandTest):
    def setUp(self):
        self.todolist = TodoList.TodoList([])
        self.todolist.add("Foo")

    def test_append1(self):
        command = AppendCommand.AppendCommand([1, "Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo Bar\n")
        self.assertEqual(self.errors, "")

    def test_append2(self):
        command = AppendCommand.AppendCommand([2, "Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_append3(self):
        command = AppendCommand.AppendCommand([1, ""], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.output, "")

    def test_append4(self):
        command = AppendCommand.AppendCommand([1], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_append5(self):
        command = AppendCommand.AppendCommand([1, "Bar", "Baz"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo Bar Baz\n")
        self.assertEqual(self.errors, "")

    def test_append6(self):
        command = AppendCommand.AppendCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_append7(self):
        command = AppendCommand.AppendCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_help(self):
        command = AppendCommand.AppendCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")
