from django.test import TestCase
from http import HTTPStatus

class AddCommentViewTest(TestCase):
    def test_add_comment_view(self):
        response = self.client.get('/blog/add_comment/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': 'test', 'email': 'sniphermarube@gmail.com', 'body': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': 'test', 'email': 'sniphermarube@gmail.com', 'body': ''})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid_email(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': 'test', 'email': 'sniphermarube', 'body': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid_name(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': '', 'email': 'sniphermarube@gmail.com', 'body': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid_email_name(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': '', 'email': 'sniphermarube', 'body': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid_email_body(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': 'test', 'email': 'sniphermarube', 'body': ''})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid_name_body(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': '', 'email': 'sniphermarube@gmail.com', 'body': ''})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')

    def test_add_comment_view_post_invalid_email_name_body(self):
        response = self.client.post('/blog/add_comment/',
                                    {'name': '', 'email': 'sniphermarube', 'body': ''})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Add Comment')


