import app
import os
import io
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
            result = self.app.get('/')
            self.assertEqual(result.status_code, 200)

    def test_upload_status_code(self):
            result = self.app.get('/upload')
            self.assertEqual(result.status_code, 200)

    def test_fail_status_code(self):
            result = self.app.get('/some/path/that/doesnt/exist')
            self.assertEqual(result.status_code, 404)

    def test_send_data_and_buffer(self):

        with open('test.jpg', 'rb') as img1:
            img1StringIO = io.BytesIO(img1.read())

        result = self.app.post('/send_from_webcam',
                                 content_type='multipart/form-data',
                                 data={'webcam': (img1StringIO, 'test.jpg')},
                                 follow_redirects=True)

        self.assertEqual(result.data, b'{"status": "ok"}')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(app.array_buffer[-1].shape, (240, 320))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
