# English

## Features
- Support both "Advanced Mode" and "Batch Mode" for different usage situations.
- Support languages supported by the selected translation engine (e.g. Google Translate supports 134 languages)
- Support multiple translation engines, including Google Translate, ChatGPT, Gemini Pro, Claude, DeepL and so on
- Support custom translation engine (you can configure to parse the response in JSON or XML format)
- **Support all ebook formats supported by Calibre (e.g. EPUB, AZW3, DOCX, PDF, etc.), as well as additional formats such as .srt and .pgn**
- **Support to translate more than one ebooks (Batch Mode). The translation process of each book is carried out simultaneously without affecting one another**
- **Support to review and edit translation result before outputting to ebook file (Advanced Mode)**
- **Support caching translated content, with no need to re-translate after request failure or network interruption**
- **Provide a large number of customization settings, such as saving translated ebooks to Calibre library or designated location**

## Installation
Please make sure [Calibre](https://calibre-ebook.com/) is installed on your OS, and install the plugin via either ways below:
### [ Install from Calibre ]
1. Click Calibre Menu [Preference... → Plug-ins → Get new plugins].
2. Select Ebook Translator from the plugin list, and click [Install].
3. Reboot Calibre.
### [ Load from file ]
1. Download the plugin zip file from [https://github.com/alexmezz993/Ebook-Translator-Calibre-Plugin](https://github.com/alexmezz993/Ebook-Translator-Calibre-Plugin).
2. Click Calibre Menu [Preference... → Plug-ins → Load plug-in from file], and choose the zip file you downloaded.
3. Reboot Calibre.

If the "Translate Book" plugin is not showing up on Calibre menu, you need to add it from [Preference... → Toolbars & menus], choose [The main toolbar], find the plugin and click [>], and [Apply].

## Usage
### [Advanced Mode]
1. Choose the ebook and enter "Advanced Mode" by either:
    - clicking "Advanced Mode" from the drop-down list of the plugin icon
    - clicking the plugin icon button if "Advanced Mode" is your Preferred Mode in General Setting
2. Select the Input Format and Target Language if needed, and click [START].
3. [Optional] Click [Delete] button to delete the selected paragraph if you don't need to translate it.
4. Translate the ebook by either:
    - clicking [Translate Selected] button to translate the selected paragraph
    - clicking [Translate All] button to translate the whole ebook
5. [Optional] After translation completed, check the "Review" area at right, edit the translation result at bottom and click [SAVE] if you need to modify the text.
6. Click [Output] button at the top right to save the ebook. The output process will be taken over by Calibre Jobs.

### [ Batch Mode ]
1. Choose the ebook(s) and enter "Batch Mode" by either:
    - clicking "Batch Mode" from the drop-down list of the plugin icon
    - clicking the plugin icon button if "Batch Mode" is your Preferred Mode in General Setting
2. Modify the eBook title if needed for generating the output filename.
3. Select the Target Language (and Output Format if needed).
4. Click [TRANSLATE] button.

After that, you can check the translation process by clicking "Jobs" at the bottom right. Double clicking the job item, you can check the real-time translation log from the window it prompts.

## Cache Manager
You can enter "Cache Manager" window via either ways below:
- Click "Cache" from the drop-down list of the plugin icon
- Follow the "Manage" link from the Cache setting of the plugin

### [ Cache Path ]
- **Choose:** Specify an empty folder to save all caches of the translated data. After that, not only will the old cache files (.db) be moved to the new path, but the future generated caches will also be saved here too
- **Reset:** Move all cache files back to the default folder. In future, the translated data will be saved in the default folder
- **Reveal:** Open the cache folder

### [ Cache Data ]
- **Clear All:** Delete all caches
- **Delete:** Delete the selected cache file(s)
You can also delete selected cache file(s) via context menu.

## Settings
You can customize the plugin through "General", "Engine" and "Content" panels.

### General

#### [ Preferred Mode ]
- **Advanced Mode:** This mode provides additional options for the translation process, allowing for more control and customization.
- **Batch Mode:** This mode allows users to translate multiple ebooks at one time, streamlining the translation process and saving time.

#### [ Output Path ]
- **Library [default]:** After the ebook is translated, it will be placed in Calibre library
- **Path:** After the ebook is translated, it will be stored in the specified directory

Why can't I find the translated ebooks? On Windows, there is a feature called "[Storage Sense](https://support.microsoft.com/en-us/windows/manage-drive-space-with-storage-sense-654f6ada-7bfc-45e5-966b-e24aded96ad5#ID0EBD=Windows_11)" that may cause this problem, as it automatically cleans up temporary files of long-running programs. You can try turning it off or specifying a directory to store temporary files for Calibre using its environment variable CALIBRE_TEMP_DIR.
```
CALIBRE_TEMP_DIR
```

#### [ Preferred Format ]
- **Input Format [default EBOOK SPECIFIC]:** Set the preferred input format for ebook
- **Output Format [default EPUB]:** Set the preferred output format for ebook

#### [ Merge to Translate ]
- **Enable [default unchecked]:** Enable to merge to translate
You can specify the number of characters to translate at one time, default value is 1800.

#### [ Network Proxy ]
- **Enable [default unchecked]:** Enable network proxy
- **Type [default HTTP]:** Choose proxy type (HTTP or SOCKS5)
- **Host:** IP or domain name
- **Port:** Range 0-65536
- **Test:** Test the connectivity of proxy
Suppose your HTTP or SOCKS proxy requires a username and password. In that case, you can append this information to the IP or domain followed by @, for example, username@127.0.0.1 or username:password@127.0.0.1 (using : to concatenate username and password).

#### [ Cache ]
- **Enable [default checked]:** Enable to cache the translated content
Enabling the caching function can avoid re-translation of the translated content after request failure or network interruption.
To clear/delete cache or customize the cache path, you can follow the "Manage" link aside to enter "Cache Manager" window.

#### [ Job Log ]
- **Show translation [default checked]:** The translation content will be displayed in real time from the respective log window of the translation job

#### [ Notification ]
- **Enable [default checked]:** Enable showing notification once translation was completed.

#### [ Search Paths ]
One path per line. This plugin will search for external programs using these paths.

### Engine

#### [ Translation Engine ]
- **Google (Free) [default]:** Free translation engine
- **Google (Basic):** API key required ([obtain](https://console.cloud.google.com/apis/credentials))
- **Google (Basic) ADC:** Set up ADC required ([instruction](https://cloud.google.com/docs/authentication/provide-credentials-adc))
- **Google (Advanced) ADC:** Set up ADC required ([instruction](https://cloud.google.com/docs/authentication/provide-credentials-adc))
- **ChatGPT (OpenAI):** API key required ([obtain](https://platform.openai.com/account/api-keys))
- **ChatGPT (Azure):** API key required ([obtain](https://azure.microsoft.com/en-us/free/))
- **Gemini Pro:** API key required ([obtain](https://aistudio.google.com/app/apikey))
- **Claude (Anthropic):** API key required ([obtain](https://console.anthropic.com/account/keys))
- **DeepL:** API key required ([obtain](https://www.deepl.com/pro?cta=header-pro-button/))
- **DeepL (Pro):** API key required ([obtain](https://www.deepl.com/pro?cta=header-pro-button/))
- **DeepL (Free):** Free translation engine
- **Microsoft Edge (Free):** Free translation engine
- **Youdao:** APP key and secret required ([obtain](https://ai.youdao.com/console/#/app-overview/create-application))
- **Baidu:** APP id and key required ([obtain](https://api.fanyi.baidu.com/register))
- **DeepSeek:** API key required ([obtain](https://platform.deepseek.com/api_keys))
- **Ollama:** Local engine, no API key required ([obtain](https://ollama.com/), [obtain tested model](https://ollama.com/library/gemma2:9b-instruct-q5_K_M))
- **[Custom]:** Customize your own translation engine

#### Custom Engine
Click the [Custom] button, you will enter the "Custom Translation Engine" interface, where you can add, delete and configure a translation engine.
The data to configure a custom translation engine is in JSON format. Each time you add a new custom translation engine, a data template is provided.

- **name:** The name of the translation engine displayed on the UI.
- **languages:** The language codes supported by the translation engine.
- **request:** Request data (url, method, headers, data).
- **response:** The expression used to parse the response data.

#### Local Engine Configuration

##### Ollama Example

To configure a local engine (e.g. Ollama), use the following JSON configuration:

```json
{
    "name": "Local (Chat)",
    "languages": {
       "source": {
            "Auto": "auto",
            "English": "English",
            "Spanish": "Spanish",
            "French": "French",
            "German": "German",
            "Italian": "Italian",
            "Japanese": "Japanese",
            "Chinese": "Chinese",
            "Russian": "Russian",
            "Portuguese": "Portuguese"
        },
        "target": {
            "English": "English",
            "Spanish": "Spanish",
            "French": "French",
            "German": "German",
            "Italian": "Italian",
            "Japanese": "Japanese",
            "Chinese": "Chinese",
            "Russian": "Russian",
            "Portuguese": "Portuguese"
        }
    },
    "request": {
        "url": "http://localhost:11434/api/chat",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "model": "gemma2:9b-instruct-q5_K_M",
            "messages": [
                  {
                    "role": "system",
                    "content": "### Role: You are an expert professional translator specializing in high-fidelity localization. You possess a deep understanding of cultural nuances and idioms in both <source> and <target>. ### Task Translate the provided text from <source> to <target>. ### Constraints: 1. **Accuracy:** Preserve the original tone, style, formatting, and meaning. 2. **No Filler:** Do not include 'Here is the translation', notes, or explanations. 3. **Direct Output:** Your response must contain ONLY the translated text and nothing else."
                },
                {
                    "role": "user",
                    "content": "### Input Text: <text>"
                }
            ],
            "stream": false,
            "options": {
                "temperature": 0.1,
                "num_predict": 2048,
                "num_ctx": 4096
            }
        }
    },
    "response": "response['message']['content']"
}
```


#### [ Preferred Language ]
- **Source Language [default Auto detect]:** Set the preferred source language.
- **Target Language [default UI language]:** Set the preferred target language.

#### [ HTTP Request ]
- **Concurrency limit:** The number of concurrent requests.
- **Interval (seconds):** The time interval to request translation engine.
- **Attempt times [default 3]:** The number of times to attempt if failed.
- **Timeout (seconds) [default 10]:** The timeout for single request.

#### [ Abort Translation ]
- **[default 10]:** The number of consecutive errors to abort translation.

#### [ Tune ChatGPT ]
- **Prompt:** Customize the prompt.
- **Endpoint:** The URL provided by ChatGPT API.
- **Model:** Select the model.
- **Sampling:** Choose to use specific temperature or top_p.
- **Stream:** Enable streaming text.

#### [ Tune Gemini ]
- **Prompt:** Customize the prompt.
- **temperature:** Controls randomness.
- **topP:** The maximum cumulative probability of tokens.
- **topK:** The maximum number of tokens.

#### [ Tune Claude ]
- **Prompt:** Customize the prompt.
- **Endpoint:** The URL provided by Claude API.
- **Model:** Select the model.
- **temperature:** Controls randomness.
- **Stream:** Enable streaming text.

### Content

#### [ Translation Position ]
- **Below original [default]:** Add the translation text after original text
- **Above original:** Add the translation text before original text
- **Right to original:** Add the translation text to the right of the original text
- **Left to original:** Add the translation text to the left of the original text
- **With no original:** Add the translation text and delete original text

#### [ Original Text Color ]
- **Color Value:** CSS color value.

#### [ Translation Text Color ]
- **Color Value:** CSS color value.

#### [ Translation Glossary ]
- **Enable [default unchecked]:** Enable to use the selected translation glossary file

#### [ Priority Element ]
CSS selectors for priority elements. One rule per line.

#### [ Ignore Element ]
CSS selectors for ignoring elements. One rule per line.

#### [ Ignore Paragraph ]
Do not translate extracted elements that match these rules.

#### [ Reserve Element ]
CSS selectors for keeping elements. One rule per line.

#### [ Ebook Metadata ]
- **Metadata translation [default unchecked]:** Translate all of the metadata information.
- **Language Mark [default unchecked]:** Append the target language to the metadata title.
- **Language Code [default unchecked]:** Replace the language in metadata with "Target Language".
- **Append Subjects:** Add the specified subjects to metadata.
