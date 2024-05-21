# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import os
import os.path

import testtools
import fixtures

from .stage_output_renames import rename_exts


class TestStageOutputRenames(testtools.TestCase):
    def test_rename_file(self):
        rename_root = self.useFixture(fixtures.TempDir()).path
        subdir = os.path.join(rename_root, 'subdir')
        os.mkdir(subdir)

        renamed_file1 = os.path.join(rename_root, 'foo.log')
        renamed_file2 = os.path.join(subdir, 'bar.something.log')
        ignored_file = os.path.join(subdir, 'foo.txt')

        with open(renamed_file1, 'w') as f:
            f.write("This is a test file: renamed 1")
        with open(renamed_file2, 'w') as f:
            f.write("This is a test file: renamed 2")
        with open(ignored_file, 'w') as f:
            f.write("This is a test file: ignored")

        results = rename_exts(rename_root, ['.log', '.notused'])
        # Check the files we expect are present
        self.assertTrue(
            os.path.isfile('_'.join(renamed_file1.rsplit('.', 1)) + '.txt'))
        self.assertTrue(
            os.path.isfile('_'.join(renamed_file2.rsplit('.', 1)) + '.txt'))
        self.assertTrue(os.path.isfile(ignored_file))
        # Check the files we don't expect are gone
        self.assertFalse(os.path.isfile(renamed_file1))
        self.assertFalse(os.path.isfile(renamed_file2))
        self.assertFalse(
            os.path.isfile('_'.join(ignored_file.rsplit('.', 1)) + '.txt'))

        self.assertFalse(results['errors'])
        self.assertEqual(len(results['renamed'].items()), 2)
