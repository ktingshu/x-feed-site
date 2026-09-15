import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fetch_x as app


class FetchTests(unittest.TestCase):
    def run_fetch(self, result):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        output = Path(directory.name) / 'data.json'
        original = {'generated_at': '2026-09-01 08:30', 'accounts': [
            {'handle': 'example', 'tweets': [{'id': '1'}]}]}
        output.write_text(json.dumps(original), encoding='utf-8')
        before = output.read_bytes()
        with patch.object(app, 'OUTPUT_FILE', str(output)), \
             patch.object(app, 'read_followed', return_value=[('example', 'Example')]), \
             patch.object(app, 'HAS_AUTH', True), \
             patch.object(app, 'fetch_account', return_value=result), \
             patch('sys.argv', ['fetch_x.py']), \
             contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            code = app.main()
        return code, before, output.read_bytes()

    def test_all_failed_does_not_change_existing_file(self):
        code, before, after = self.run_fetch(None)
        self.assertEqual(code, 1)
        self.assertEqual(before, after)

    def test_success_records_freshness(self):
        code, _, after = self.run_fetch({'handle': 'example', 'tweets': [{'id': '2'}]})
        self.assertIsNone(code)
        payload = json.loads(after)
        self.assertEqual(payload['fetch_summary']['fresh'], 1)
        self.assertFalse(payload['accounts'][0]['stale'])
        self.assertIn('fetched_at', payload['accounts'][0])

    def test_unknown_timeline_is_not_silent_empty_success(self):
        with self.assertRaises(ValueError):
            app.flatten_timeline({'data': {}})

    def test_both_timeline_shapes(self):
        entry = {'content': {'itemContent': {'tweet_results': {'result': {
            'tweet': {'legacy': {'id_str': '123', 'full_text': 'hello'}}}}}}}
        for key in ('timeline', 'timeline_v2'):
            data = {'data': {'user': {'result': {key: {'timeline': {
                'instructions': [{'entries': [entry]}]}}}}}}
            self.assertEqual(app.flatten_timeline(data)[0]['id'], '123')


if __name__ == '__main__':
    unittest.main()
