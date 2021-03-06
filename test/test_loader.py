from .helper import BJOTest
from bernard.actors import Locker, Notifier
from bernard.loader import YAMLLoader
from praw.models import Comment, Submission


class TestValidation(BJOTest):
    def setUp(self):
        super().setUp()
        self.loader = YAMLLoader(self.db, self.cur, self.subreddit)

    def test_bad_param_type(self):
        params = {'text': 3}
        with self.assertRaises(RuntimeError):
            self.loader.validate_subactor_config(Notifier, params, [])

    def test_good_param_type(self):
        params = {'text': "foobar"}
        self.loader.validate_subactor_config(Notifier, params, [])

    def test_bad_target_type(self):
        with self.assertRaises(RuntimeError):
            self.loader.validate_subactor_config(Locker, {}, [Comment])

    def test_good_target_type(self):
        self.loader.validate_subactor_config(Locker, {}, [Submission])
