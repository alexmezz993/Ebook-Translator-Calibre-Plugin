import json
from contextlib import suppress
from urllib.parse import urlparse

from calibre.utils.localization import _  # type: ignore

from .. import EbookTranslator
from ..lib.utils import request
from .genai import GenAI
from .languages import google


load_translations()  # type: ignore


class OllamaTranslate(GenAI):
    name = 'Ollama'
    alias = 'Ollama'
    lang_codes = GenAI.load_lang_codes(google)
    
    # Default configuration
    host = 'http://localhost'
    port = 11434
    
    endpoint = f'{host}:{port}/api/chat'
    
    # GenAI specific
    prompt = (
        '### Role: You are an expert professional translator specializing in '
        'high-fidelity localization. You possess a deep understanding of '
        'cultural nuances and idioms in both <slang> and <tlang>. '
        '### Task Translate the provided text from <slang> to <tlang>. '
        '### Constraints: 1. **Accuracy:** Preserve the original tone, style, '
        'formatting, and meaning. 2. **No Filler:** Do not include \'Here is '
        'the translation\', notes, or explanations. 3. **Direct Output:** '
        'Your response must contain ONLY the translated text and nothing else.')
    
    samplings = ['temperature', 'top_p']
    sampling = 'temperature'
    temperature = 0.1
    top_p = 0.9
    stream = False  # Default to false as per user request example, generally easier to start with
    
    models: list[str] = []
    # TODO: Handle the default model more appropriately.
    model: str | None = None
    
    need_api_key = False

    # Force concurrency to 1 to ensure history order
    concurrency_limit = 1
    
    # Context settings
    context_limit = 0
    history: list[dict] = []
    current_text: str | None = None

    def __init__(self):
        super().__init__()
        # Load config
        self.host = self.config.get('host', self.host)
        self.port = self.config.get('port', self.port)
        self.context_limit = self.config.get('context_limit', self.context_limit)
        
        # Initialize history
        self.history = []
        
        # Ensure scheme
        if not self.host.startswith('http'):
            self.host = f'http://{self.host}'
            
        self.endpoint = f'{self.host}:{self.port}/api/chat'
        
        self.prompt = self.config.get('prompt', self.prompt)
        self.sampling = self.config.get('sampling', self.sampling)
        self.temperature = self.config.get('temperature', self.temperature)
        self.top_p = self.config.get('top_p', self.top_p)
        self.stream = self.config.get('stream', self.stream)
        self.model = self.config.get('model', self.model)

    def get_models(self):
        # https://github.com/ollama/ollama/blob/main/docs/api.md#list-local-models
        # GET /api/tags
        url = f'{self.host}:{self.port}/api/tags'
        try:
            response = request(
                url, headers=self.get_headers(),
                proxy_uri=self.proxy_uri,
                timeout=5) # Short timeout for local checks
            data = json.loads(response)
            return [model['name'] for model in data.get('models', [])]
        except Exception:
            return []

    def get_prompt(self):
        prompt = self.prompt.replace('<tlang>', self.target_lang)
        if self._is_auto_lang():
            prompt = prompt.replace('<slang>', 'detected language')
        else:
            prompt = prompt.replace('<slang>', self.source_lang)
        
        # Merge placeholder retention instruction if enabled
        if self.merge_enabled:
             prompt += (
                ' Ensure that placeholders matching the pattern {{id_\\d+}} '
                'in the content are retained.')
                
        return prompt

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'Ebook-Translator/%s' % EbookTranslator.__version__
        }

    def get_body(self, text):
        self.current_text = text
        
        messages = [{'role': 'system', 'content': self.get_prompt()}]
        
        # Inject history
        if self.context_limit > 0:
            messages.extend(self.history)
            
        # Add current request
        messages.append({
            'role': 'user',
            'content': f'### Input Text: {text}'
        })

        body = {
            'model': self.model,
            'messages': messages,
            'stream': self.stream,
            'options': {
                'num_predict': 2048,
                'num_ctx': 4096 
            }
        }
        
        # Apply sampling
        sampling_value = getattr(self, self.sampling)
        body['options'][self.sampling] = sampling_value
        
        return json.dumps(body)

    def _update_history(self, translation):
        if self.context_limit > 0 and self.current_text:
            self.history.append({
                'role': 'user', 
                'content': f'### Input Text: {self.current_text}'
            })
            self.history.append({
                'role': 'assistant',
                'content': translation
            })
            
            # Keep history within limit (limit * 2 because storing pairs)
            if len(self.history) > self.context_limit * 2:
                self.history = self.history[-(self.context_limit * 2):]

    def get_result(self, response):
        if self.stream:
            return self._parse_stream(response)
            
        data = json.loads(response)
        translation = data['message']['content']
        
        self._update_history(translation)
        
        return translation

    def _parse_stream(self, response):
        # Ollama streaming response: JSON objects one per line
        from http.client import IncompleteRead
        
        full_translation = []
        
        while True:
            try:
                line = response.readline().decode('utf-8').strip()
            except IncompleteRead:
                continue
            except Exception as e:
                raise Exception(
                    _('Can not parse returned response. Raw data: {}')
                    .format(str(e)))
            
            if not line:
                break
                
            try:
                data = json.loads(line)
                if 'message' in data and 'content' in data['message']:
                     content = data['message']['content']
                     if content:
                         yield content
                         full_translation.append(content)
                
                if data.get('done', False):
                    break
                    
            except json.JSONDecodeError:
                continue
        
        if full_translation:
            self._update_history(''.join(full_translation))
