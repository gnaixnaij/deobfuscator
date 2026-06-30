# Changelog

## v1.0.0 (2026-06-29)

### Initial Release

- PowerShell deobfuscation: Base64 decode, IEX extraction, variable noise removal, nested invoke unwrapping
- VBA deobfuscation: Chr() resolution, line continuation collapse, string concatenation, dead variable stripping
- JavaScript deobfuscation: atob/base64, hex escapes, unicode escapes, String.fromCharCode(), eval() unwrapping
- Optional LLM-powered analysis via OpenAI-compatible APIs
- Language auto-detection from file extension or content heuristics
- CLI interface with file and stdin input support
