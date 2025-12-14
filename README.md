# Ebook Translator (a Calibre plugin)

![Ebook Translator Calibre Plugin](images/logo.png)

A Calibre plugin to translate ebook into a specified language.

__Plugin Homepage__: [https://github.com/alexmezz993/Ebook-Translator-Calibre-Plugin](https://github.com/alexmezz993/Ebook-Translator-Calibre-Plugin)

![Translation illustration](images/sample-en.png)

---

## Features

* Support both "Advanced Mode" and "Batch Mode" for different usage situations.
* Support languages supported by the selected translation engine (e.g. Google Translate supports 134 languages)
* Support multiple translation engines, including Google Translate, ChatGPT, Gemini, Claude, DeepL, DeepSeek, Ollama, etc.
* Support custom translation engines (you can configure to parse response in JSON or XML format)
* Support all ebook formats supported by Calibre (e.g. EPUB, AZW3, DOCX, PDF, etc.), as well as additional formats such as .srt
* Support to translate more than one ebooks. The translation process of each book is carried out simultaneously without affecting one another
* Support caching translated content, with no need to re-translate after request failure or network interruption
* Provide a large number of customization settings, such as saving translated ebooks to Calibre library or designated location

---

## Manual

* [Tutorial](wiki/Tutorial.md#a-brief-tour)
* [Installation](wiki/English.md#installation)
* [Usage](wiki/English.md#usage)
* [Settings](wiki/English.md#settings)

---

## Links

* [Project Homepage](https://github.com/alexmezz993/Ebook-Translator-Calibre-Plugin)

## Development Guide

### Prerequisites
* **Calibre**: Version >= 5.0.0
* **Python**: Version >= 3.8.5

### Information on Dependencies
External dependencies are **vendored** within the `vendor/` directory (e.g., `socks.py`, `cssselect`). This ensures the plugin functions without requiring users to manually install Python packages via `pip`.

### Configuration & Environment
The plugin uses Calibre's JSON configuration system (via `prefs` or internal config handling). Below are the key configuration options found in `setting.py` and environment behavior:

| Option / Variable | Description | Default / Note |
| :--- | :--- | :--- |
| **Environment Variables** | | |
| `CALIBRE_DEBUG` | If set (e.g. to `1`), enables debug logging. | Auto-set by `__init__.py` if Calibre is in debug mode. |
| `http_proxy`, `https_proxy` | System-level proxy settings. | Used via `lib/utils.py` if proxy is not configured in settings. |
| **Plugin Settings** | | |
| `preferred_mode` | Translation mode selection. | `advanced` or `batch` |
| `output_path` | Custom directory for saving translated books. | Used if `to_library` is false. |
| `translate_engine` | Active translation engine. | e.g. `Google`, `ChatGPT`, `Ollama`. |
| `api_keys` | Storage for API keys. | |
| `model` | Specific model for GenAI engines. | |
| `host`, `port` | Server details for self-hosted engines (Ollama). | Default: `http://localhost:11434` for Ollama. |
| `context_limit` | History limit for conversation context. | |
| `temperature`, `top_p` | Sampling (creativity) settings. | Defaults vary by engine. |
| `stream` | Enable streaming responses. | |
| `concurrency_limit` | Max concurrent HTTP requests. | Engine-specific defaults. |
| `cache_enabled` | Toggle translation caching. | |

### Running & Debugging
To run the plugin's test suite using Calibre's debug environment:

```bash
calibre-debug -e test.py
```

To debug the plugin within the Calibre GUI:
```bash
calibre-debug -g
```

## Packaging & Release Guide

### Plugin Build (Zipping)
### Plugin Build (Zipping)
To create a production-ready ZIP file, run the included python script:

```bash
python build_plugin.py
```

Or using `calibre-debug` (recommended if standard python is missing):
```bash
calibre-debug -e build_plugin.py
```

This script will:
1.  Automatically increment the patch version in `__init__.py`.
2.  Create a clean ZIP file (excluding `.git`, `tests`, `__pycache__`, etc.) in the `build/` directory.
3.  Name the file using the format: `{identifier}_{version}.zip` (e.g., `ebook-translator_2.4.3.zip`).

### CI/CD Pipeline
### CI/CD Pipeline
The project includes an automated GitHub Actions workflow for releasing versions.

**To trigger a release:**
1.  Commit your changes.
2.  Use a commit message containing the trigger pattern: `release ebook-translator@X.Y.Z`.
    *   Example: `feat: add new engines, release ebook-translator@2.5.0`
3.  Push to `main` or `master`.

**The workflow will:**
1.  Verify the version in the commit message.
2.  **Build the plugin** and generate the ZIP file in GitHub Actions.
3.  **Commit the ZIP file** back to the repository (message: `chore: release artifacts vX.Y.Z`).
4.  Create and push a git tag `vX.Y.Z` on this new commit.
5.  Create a GitHub Release `vX.Y.Z` with the plugin ZIP attached.

## License

[GNU General Public License v3.0](LICENSE)
