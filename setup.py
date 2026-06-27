from setuptools import setup, find_packages

setup(
    name="ai-deobfuscator",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "deobfuscator=deobfuscator.cli:main",
        ],
    },
    python_requires=">=3.8",
)
