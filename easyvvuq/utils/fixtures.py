import os
import shutil

__copyright__ = """

    Copyright 2018 Robin A. Richardson, David W. Wright

    This file is part of EasyVVUQ

    EasyVVUQ is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EasyVVUQ is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
__license__ = "LGPL"


class Fixture(object):

    def __init__(self, path, is_dir=False, common=False, exists_local=True,
                 target_name="", campaign_dir='.', group=''):
        """

        Parameters
        ----------
        path
            Path to file or directory
        common
            Will fixture be common to multiple runs
        exists_local
            Does the file exist on the local machine (i.e. can it be copied to
            a common or run directory by EasyVVUQ)
        target_name
            Target file name or path. Path should be relative to a run directory
            except for when `common` is set.
        """

        self.exists_local = exists_local

        self._basename = os.path.basename(path)

        if exists_local:

            abs_path = os.path.realpath(os.path.expanduser(path))

            if not os.path.exists(abs_path):
                raise IOError(f"Unable to find local fixture: {path}")

            self.src_path = abs_path

        else:

            self.src_path = path

        self.target_name = target_name
        self.common = common
        self._common_copied = False
        self.is_dir = is_dir
        self.campaign_dir = campaign_dir
        self.group = group

    def copy_to_target(self, target_dir=None):

        target_path = self.fixture_path(target_dir=target_dir, relative=False)

        if self.common and self._common_copied:
            return

        if self.is_dir:
            shutil.copytree(self.src_path, target_path)
        else:
            shutil.copy2(self.src_path, target_path)

        if self.common:
            self._common_copied = True

    def fixture_path(self, target_dir='', relative=True, depth_in_run=0):

        target_name = self.target_name
        common = self.common

        if not self.exists_local:
            return self.src_path

        fixture_path = ''

        if common:

            fixture_path = os.path.join(fixture_path, 'common')

            if self.group:
                fixture_path = os.path.join(fixture_path, 'group')

            if relative:
                fixture_path = os.path.join('..', fixture_path)

        if relative:

            for level in range(depth_in_run):
                fixture_path = os.path.join('..', fixture_path)

        else:

            if common:

                fixture_path = os.path.join(self.campaign_dir, fixture_path)

            else:

                if not target_dir:
                    raise RuntimeError(
                        f"A target_dir is needed to create target path "
                        f"for the fixture {self.path}")

                fixture_path = os.path.join(target_dir, fixture_path)

        if target_name:
            fixture_path = os.path.join(fixture_path, target_name)

        else:
            fixture_path = os.path.join(fixture_path, self._basename)

        return fixture_path
