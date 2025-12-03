# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import shutil
import unittest

from chatbot_util import __main__, file_io

from .. import utilities


class TestChain(unittest.TestCase):
    def test_verified_when_no_backup(self):
        lines = ["abc\n"]
        with utilities.TestFileContent(lines) as temp_file:
            # monkey patch to set config filename to tempfile
            file_io.FILENAMES["permutated"] = temp_file.filename

            verified = __main__.verify()
            self.assertTrue(verified)

            # reset monkey patch to prevent muddying state for other tests
            file_io.FILENAMES["permutated"] = f"{file_io.DIR}/{file_io.PERMUTATED}"

    def test_verified_when_identical_backup(self):
        lines = ["abc\n"]
        with utilities.TestFileContent(lines) as temp_file:
            # monkey patch to set config filename to tempfile
            file_io.FILENAMES["permutated"] = temp_file.filename
            shutil.copy(temp_file.filename, temp_file.filename + ".backup")

            verified = __main__.verify()
            self.assertTrue(verified)

            # reset monkey patch to prevent muddying state for other tests
            file_io.FILENAMES["permutated"] = f"{file_io.DIR}/{file_io.PERMUTATED}"

    def test_verified_when_adding_lines(self):
        lines = ["abc\n"]
        with (
            utilities.TestFileContent(lines) as temp_file,
            open(temp_file.filename + ".backup", "w", encoding="utf-8"),
        ):
            # monkey patch to set config filename to tempfile
            file_io.FILENAMES["permutated"] = temp_file.filename

            verified = __main__.verify()
            self.assertTrue(verified)

            # reset monkey patch to prevent muddying state for other tests
            file_io.FILENAMES["permutated"] = f"{file_io.DIR}/{file_io.PERMUTATED}"

    def test_unverified_when_missing_lines(self):
        lines = ["abc\n"]
        with (
            utilities.TestFileContent(lines) as temp_file,
            open(temp_file.filename + ".backup", "w+", encoding="utf-8") as copy,
        ):
            # monkey patch to set config filename to tempfile
            file_io.FILENAMES["permutated"] = temp_file.filename

            copy.write("abc\ndef\n")

            # need to reset buffer pointer before reading in verify() since
            # we haven't closed the copy file yet
            copy.seek(0)

            verified = __main__.verify()
            self.assertFalse(verified)

            # reset monkey patch to prevent muddying state for other tests
            file_io.FILENAMES["permutated"] = f"{file_io.DIR}/{file_io.PERMUTATED}"
