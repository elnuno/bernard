from .helper import BJOTest
import mock


class BrowserTest(BJOTest):
    def test_reasons(self):
        self.assertEqual(self.browser.header[:4], "Your")

    def test_scan_post(self):
        self.r.login(self.un, password=self.un_pswd, disable_warning=True)
        post_id = self.r.submit(self.sr, 'BrowserTest.test_scan_post',
                                text='', send_replies=False).id
        post = self.browser.r.get_submission(submission_id=post_id)
        post.report('1')
        post.refresh()
        self.browser.scan_post(post)
        post.refresh()
        self.assertTrue(post.locked)

    def test_scan_reports(self):
        self.r.login(self.un, password=self.un_pswd, disable_warning=True)
        post_id = self.r.submit(self.sr, 'BrowserTest.test_scan_reports',
                                text='', send_replies=False).id
        post = self.browser.r.get_submission(submission_id=post_id)
        post.report('1')
        self.browser.scan_reports()
        post.refresh()
        self.assertTrue(post.locked)

    def test_check_approvals(self):
        self.r.login(self.un, password=self.un_pswd, disable_warning=True)
        post_id = self.r.submit(self.sr, 'BrowserTest.test_check_approvals',
                                text='', send_replies=False).id
        post = self.browser.r.get_submission(submission_id=post_id)
        post.report('1')
        self.browser.scan_reports()
        post.approve()
        self.browser.check_approvals()

        post.refresh()
        self.assertFalse(post.locked)
        self.assertIsNone(post.banned_by)

        with mock.patch('praw.objects.Comment.remove') as mock_comment_remove:
            self.browser.check_approvals()
            self.assertFalse(mock_comment_remove.called)
