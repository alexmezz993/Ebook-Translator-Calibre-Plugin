
import unittest
import json
from unittest.mock import patch, Mock
from types import GeneratorType

from ...engines.ollama import OllamaTranslate
from ...lib.exception import UnexpectedResult

module_name = 'calibre_plugins.ebook_translator.engines.ollama'

class TestOllama(unittest.TestCase):
    def setUp(self):
        OllamaTranslate.set_config({})
        self.translator = OllamaTranslate()
        # Mock some attributes for isolation
        self.translator.host = 'http://localhost'
        self.translator.port = 11434
        self.translator.model = 'llama3'

    @patch(module_name + '.request')
    def test_get_models_success(self, mock_request):
        mock_request.return_value = json.dumps({
            "models": [
                {"name": "llama3"},
                {"name": "mistral"}
            ]
        })
        
        models = self.translator.get_models()
        self.assertEqual(models, ['llama3', 'mistral'])
        mock_request.assert_called_once()
        self.assertIn('/api/tags', mock_request.call_args[0][0])

    @patch(module_name + '.request')
    def test_get_models_failure(self, mock_request):
        mock_request.side_effect = Exception("Network Error")
        models = self.translator.get_models()
        self.assertEqual(models, [])

    @patch(module_name + '.request')
    def test_translate_success(self, mock_request):
        self.translator.stream = False
        mock_request.return_value = json.dumps({
            "message": {
                "content": "Translated Text"
            },
            "done": True
        })
        
        result = self.translator.translate('Original Text')
        self.assertEqual(result, "Translated Text")
        mock_request.assert_called_once()

    @patch(module_name + '.request')
    def test_translate_malformed_json(self, mock_request):
        self.translator.stream = False
        mock_request.return_value = "Invalid JSON"
        
        with self.assertRaises(json.JSONDecodeError):
             self.translator.translate('Original Text')

    @patch(module_name + '.request')
    def test_translate_stream(self, mock_request):
        self.translator.stream = True
        
        # Mocking a response object that behaves like a file with readline
        mock_response = Mock()
        # Simulate lines from Ollama streaming API
        lines = [
            b'{"message": {"content": "Trans"}, "done": false}',
            b'{"message": {"content": "lated"}, "done": false}',
            b'{"message": {"content": " Text"}, "done": true}'
        ]
        mock_response.readline.side_effect = lines + [b''] # End of stream
        mock_request.return_value = mock_response
        
        result_generator = self.translator.translate('Original Text')
        self.assertIsInstance(result_generator, GeneratorType)
        
        full_text = "".join(result_generator)
        self.assertEqual(full_text, "Translated Text")

    @patch(module_name + '.request')
    def test_translate_stream_parse_error(self, mock_request):
        self.translator.stream = True
        mock_response = Mock()
        # Simulate broken JSON line
        lines = [b'{"message": {"content": "OK"}}', b'{broken_json}']
        mock_response.readline.side_effect = lines + [b'']
        mock_request.return_value = mock_response

        # The loop in _parse_stream continues on JSONDecodeError as per implementation
        # except block: continue
        
        result_generator = self.translator.translate('Original Text')
        results = list(result_generator)
        self.assertEqual("".join(results), "OK") 
        # It should just skip the broken line if that's the implementation logic.
        # Let's verify _parse_stream implementation:
        # except json.JSONDecodeError: continue

    @patch(module_name + '.request')
    def test_translate_stream_network_error(self, mock_request):
        self.translator.stream = True
        mock_response = Mock()
        mock_response.readline.side_effect = Exception("Read Timeout")
        mock_request.return_value = mock_response
        
        result_generator = self.translator.translate('Original Text')
        
        # Generator raises when iterating
        with self.assertRaisesRegex(Exception, "Can not parse returned response"):
            next(result_generator)

