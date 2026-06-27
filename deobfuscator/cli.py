import argparse
import os
import sys
import textwrap

from .core import analyze, detect_language
from .llm.deobfuscate import deobfuscate_with_llm
from . import __version__

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def c(text, color=None, bold=False, dim=False):
    parts = []
    if color:
        parts.append(color)
    if bold:
        parts.append(BOLD)
    if dim:
        parts.append(DIM)
    if parts:
        return "".join(parts) + text + RESET
    return text


def print_banner():
    banner = f"""{CYAN}{BOLD}
   ╔══════════════════════════════════════╗
   ║    AI Deobfuscator v{__version__:<12}║
   ║    PowerShell · VBA · JavaScript     ║
   ╚══════════════════════════════════════╝{RESET}
"""
    print(banner)


def handle_file(args):
    path = args.file
    if not os.path.exists(path):
        print(c(f"Error: file not found: {path}", RED))
        sys.exit(1)

    with open(path, 'r', errors='replace') as f:
        script = f.read()

    lang = args.lang or detect_language(script, hint=os.path.splitext(path)[1])
    print(f" Language: {c(lang.upper(), CYAN, bold=True)}")
    print(f"   Source: {c(path, DIM)}")
    print(f"   Length: {c(f'{len(script):,} chars', YELLOW)}")
    print()

    result = analyze(script, lang=lang)

    # Static deobfuscation steps
    if result.get("static_steps"):
        print(c("   ── Static Analysis ──", BOLD))
        for step in result["static_steps"]:
            print(f"   {c('✓', GREEN)} {step}")
        print()

    # Show deobfuscated result
    deobf = result.get("deobfuscated", "")
    if deobf and deobf.strip() != script.strip():
        print(c("   ── Deobfuscated (Static) ──", BOLD))
        print(textwrap.indent(deobf.strip(), "   "))
        print()
    elif deobf:
        print(c("   Static deobfuscation did not change the script.", DIM))
        print()

    # LLM deobfuscation
    if args.llm or args.api_key:
        api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
        model = args.model or "gpt-4o-mini"
        base_url = args.base_url
        print(c(f"   ── LLM Deobfuscation ({model}) ──", BOLD))
        print(c("   Calling LLM...", DIM))

        llm_result, error = deobfuscate_with_llm(
            script, lang, api_key=api_key, model=model, base_url=base_url
        )

        if error:
            print(c(f"   ✗ {error}", RED))
        else:
            print(c("   ✓ LLM analysis complete", GREEN))
            if llm_result.get("techniques"):
                print(f"\n   {c('Techniques detected:', BOLD)}")
                for t in llm_result["techniques"]:
                    print(f"     • {t}")
            if llm_result.get("summary"):
                print(f"\n   {c('Summary:', BOLD)} {llm_result['summary']}")
            if llm_result.get("deobfuscated"):
                print(f"\n   {c('Deobfuscated:', BOLD)}")
                print(textwrap.indent(llm_result["deobfuscated"].strip(), "   "))


def handle_stdin():
    script = sys.stdin.read()
    if not script.strip():
        print(c("No input received from stdin.", RED))
        sys.exit(1)

    lang = detect_language(script)
    print(f" Language: {c(lang.upper(), CYAN, bold=True)}")
    print()

    result = analyze(script, lang=lang)
    deobf = result.get("deobfuscated", "")
    if deobf:
        print(deobf.strip())
    else:
        print(c("Could not deobfuscate.", RED))


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered deobfuscator for PowerShell, VBA, and JavaScript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              deobfuscator -f obfuscated.ps1
              deobfuscator -f malware.vba --llm
              deobfuscator -f evil.js --api-key sk-... --model gpt-4o
              cat script.ps1 | deobfuscator --stdin
        """),
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-f", "--file", help="Path to obfuscated script file")
    input_group.add_argument("--stdin", action="store_true", help="Read script from stdin")

    parser.add_argument("-l", "--lang", help="Force language (powershell, vba, javascript)")
    parser.add_argument("--llm", action="store_true", help="Enable LLM-based deobfuscation")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env)")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model (default: gpt-4o-mini)")
    parser.add_argument("--base-url", help="OpenAI-compatible base URL (e.g., for local models)")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print(f"ai-deobfuscator v{__version__}")
        sys.exit(0)

    print_banner()

    if args.stdin:
        handle_stdin()
    elif args.file:
        handle_file(args)
    else:
        parser.print_help()
        print()
        print(c("Provide a file with -f or pipe input with --stdin", YELLOW))
        sys.exit(1)


if __name__ == "__main__":
    main()
