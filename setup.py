from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="novelreader-cli",
    version="1.0.0",
    author="Firdaus Aris",
    author_email="firdaus@firdausaris.com",
    description="Context-aware text-to-speech CLI for novel reading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firdausaris/novelreader-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "novelreader=novelreader:main",
        ],
    },
    keywords="text-to-speech, novel, writing, cli, tts, audio, accessibility",
    project_urls={
        "Bug Reports": "https://github.com/firdausaris/novelreader-cli/issues",
        "Source": "https://github.com/firdausaris/novelreader-cli",
    },
)