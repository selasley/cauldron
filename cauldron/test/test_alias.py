from cauldron.test import support
from cauldron.test.support import scaffolds


class TestAlias(scaffolds.ResultsTest):
    """

    """

    def test_list(self):
        """
        """

        r = support.run_command('alias list')
        self.assertFalse(r.failed, 'should not have failed')
