# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
Test class for Partition table CLI
"""

from robottelo.cli.partitiontable import PartitionTable
from robottelo.cli.factory import make_partition_table
from robottelo.common.helpers import generate_name
from robottelo.test import MetaCLITestCase
from robottelo.common import ssh
import tempfile


class TestPartitionTable(MetaCLITestCase):

    factory = make_partition_table
    factory_obj = PartitionTable
    file = ""

    def setUp(self):
        """Set up file"""
        self.file = tempfile.NamedTemporaryFile(delete=True)
        self.file.write("This is a test partition table file \n")
        return self.file.name

    def tearDown(self):
        """Remove the file"""
        self.file.close()

    def test_dump_ptable_1(self):
        """
        @Feature: Partition Table - Create
        @Test: Check if Partition Table can be created with specific content
        @Assert: Partition Table is created
        """

        content = "Fake ptable"
        name = generate_name(6)
        make_partition_table({'name': name, 'content': content})

        ptable = PartitionTable().exists(tuple_search=('name', name)).stdout

        args = {
            'id': ptable['id'],
        }

        ptable_content = PartitionTable().dump(args)

        self.assertTrue(content in ptable_content.stdout[0])

    def test_delete_ptable_1(self):
        """
        @Feature: Partition Table - Delete
        @Test: Check if Partition Table can be deleted
        @Assert: Partition Table is deleted
        """

        content = "Fake ptable"
        name = generate_name(6)
        make_partition_table({'name': name, 'content': content})

        ptable = PartitionTable().exists(tuple_search=('name', name)).stdout

        args = {
            'id': ptable['id'],
        }

        PartitionTable().delete(args)
        self.assertFalse(
            PartitionTable().exists(tuple_search=('name', name)).stdout)

    def test_create_ptable(self):
        """
        @Feature: Partition Table - Create
        @Test: Check if Partition Table can be created
        @Assert: Partition Table is created
        """

        content = "Fake ptable"
        name = generate_name(6)

        file_name = self.setUp()
        ssh.upload_file(file_name, remote_file=file_name)

        args = {
            'name': name,
            'os-family': 'Redhat',
            'file': file_name,
            'content': content
        }

        try:
            make_partition_table(args)
        except Exception as e:
                self.fail(e)

        self.assertTrue(
            PartitionTable().exists(tuple_search=('name', name)).stdout)
        self.tearDown()

    def test_update_ptable(self):
        """
        @Feature: Partition Table - Update
        @Test: Check if Partition Table can be updated
        @Assert: Partition Table is updated
        """

        content = "Fake ptable"
        name = generate_name(6)
        new_name = generate_name(6)

        file_name = self.setUp()
        ssh.upload_file(file_name, remote_file=file_name)

        args = {
            'name': name,
            'os-family': 'Redhat',
            'file': file_name,
            'content': content
        }

        try:
            make_partition_table(args)
        except Exception as e:
                self.fail(e)

        self.assertTrue(
            PartitionTable().exists(tuple_search=('name', name)).stdout)

        args = {
            'name': name,
            'os-family': 'Redhat',
            'file': file_name,
            'new-name': new_name
        }

        PartitionTable().update(args)
        self.assertFalse(
            PartitionTable().exists(tuple_search=('new-name',
                                                  new_name)).stdout)
        self.tearDown()
