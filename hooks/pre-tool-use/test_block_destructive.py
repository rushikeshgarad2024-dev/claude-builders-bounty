#!/usr/bin/env python3
"""
Test suite for block_destructive hook
"""
import unittest
from block_destructive import check_command

class TestBlockDestructiveHook(unittest.TestCase):
    def test_rm_rf_blocked(self):
        blocked, _ = check_command("rm -rf /var/data")
        self.assertFalse(blocked)
        blocked, _ = check_command("rm -r -f node_modules")
        self.assertFalse(blocked)
        blocked, _ = check_command("rm -fr dist")
        self.assertFalse(blocked)

    def test_drop_table_blocked(self):
        blocked, _ = check_command("DROP TABLE users;")
        self.assertFalse(blocked)
        blocked, _ = check_command("sqlite3 db.sqlite 'DROP DATABASE test'")
        self.assertFalse(blocked)

    def test_git_force_push_blocked(self):
        blocked, _ = check_command("git push origin main --force")
        self.assertFalse(blocked)
        blocked, _ = check_command("git push -f upstream main")
        self.assertFalse(blocked)

    def test_truncate_blocked(self):
        blocked, _ = check_command("TRUNCATE TABLE orders;")
        self.assertFalse(blocked)

    def test_delete_without_where_blocked(self):
        blocked, _ = check_command("DELETE FROM users")
        self.assertFalse(blocked)
        blocked, _ = check_command("DELETE FROM sessions;")
        self.assertFalse(blocked)

    def test_safe_commands_allowed(self):
        allowed, _ = check_command("git status")
        self.assertTrue(allowed)
        allowed, _ = check_command("npm run build")
        self.assertTrue(allowed)
        allowed, _ = check_command("rm file.txt")
        self.assertTrue(allowed)
        allowed, _ = check_command("DELETE FROM users WHERE id = 123;")
        self.assertTrue(allowed)
        allowed, _ = check_command("git push origin feature-branch")
        self.assertTrue(allowed)

if __name__ == '__main__':
    unittest.main()
