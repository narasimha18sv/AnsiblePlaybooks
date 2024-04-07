# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""
Lint rule class to test if some blocked modules were used.
"""
import sys
from typing import TYPE_CHECKING
from ansiblelint.constants import LINE_NUMBER_KEY
from ansiblelint.rules import AnsibleLintRule, TransformMixin
from ansiblelint.utils import get_cmd_args
from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.utils import Task

ID: str = 'blocked_modules'
C_BLOCKED_MODULES: str = 'blocked'

DESC: str = """Rule to check if some blocked modules were used in tasks."""

class BlockedModules(AnsibleLintRule):
    """
    Lint rule class to test if variables defined by users follow the namging
    conventions and guildelines.
    """
    id: str = ID
    shortdesc: str = 'Blocked modules'
    description: str = DESC
    severity: str = 'HIGH'
    tags = [ID, 'module']

    def matchtask(
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> bool | str:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        try:
            mod = task.get("delegate_to", False)
            if not mod:
                return []
            return [
                self.create_matcherror(
                    message=self.description,
                    filename=file,
                    tag=f"{self.id}[task]",
                    lineno=task[LINE_NUMBER_KEY],
                ),
                ]
            # mod = task["action"]["__ansible_module__"]
            # if mod in ['delegate_to', 'add_host']:
            #     #return True
            #     return f'{self.shortdesc}: {mod}'
        except KeyError:
            pass

        return False

# vim:sw=4:ts=4:et:
