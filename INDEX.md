# Repository Index

## Purpose

This repository is a mixed Python learning workspace. It contains:

- structured learning notes and experiments
- practice solutions for competitive programming and general problem solving
- standalone projects and prototypes
- a small reference area with QA/testing snippets

The repository was reorganized on 2026-03-15 into a purpose-based hierarchy:

- `learning/`
- `practice/`
- `projects/`
- `reference/`

## Current Top-Level Layout

### `learning/`

Learning material, experiments, and topic-based labs.

- `learning/concepts/awareness`
  - small concept-focused files and notebooks such as `x-if-or.py`, list comprehension notes, private/protected naming, and return-behavior experiments
- `learning/concepts/advanced`
  - advanced Python topics and small experiments
  - includes decorators, doctests, classmethod, inheritance, dict behavior, `asyncio`, Redis, sockets, signals, Selenium testing, pandas notebooks, scopes, tkinter, and configuration notes
  - notable folders: `__dender-methods__`, `decorators`, `x-pandas`, `x-selenium-for-testing`, `x-signals`, `x-socket`
- `learning/concepts/special`
  - niche topic labs such as caching, CSV, datetime, pandas, pyautogui, tkinter, and XML-to-dict

- `learning/lessons/basics`
  - lesson-style basics files: output, input, variables, casting, operators, unpacking, assertions, exceptions, decorators, imports
- `learning/lessons/fastapi`
  - FastAPI lesson snippets with templates and static files
- `learning/lessons/python-modules`
  - lesson-style module examples: argparse, collections, colorama, decimal, json, numpy, regex, requests, SQLAlchemy, logging
- `learning/lessons/pyfun`
  - smaller app experiments and one notebook
- `learning/lessons/special`
  - lesson-oriented pandas, pyautogui, tkinter, and `getch` examples
- `learning/lessons/design-patterns`
  - singleton examples

- `learning/topic-labs/basics`
  - a second, broader basics track with more granular folders like `x-decorators`, `x-exceptions`, `x-import`, `x-import2`, `x-strings`, `x-datetimeconv`
- `learning/topic-labs/python-modules`
  - a broader module sandbox with FastAPI, Flask, hashlib, matplotlib, multiprocessing, OS, pickles, pydantic, requests, shutil, SMTP, SQLAlchemy, uuid, pygame, and more
- `learning/topic-labs/packaging`
  - a small packaging example under `project_1`

Note:
- `learning/lessons/*` and `learning/topic-labs/*` overlap in subject matter but are not exact duplicates; they were kept separate because their contents differ.

### `practice/`

Problem-solving and training material.

- `practice/competitive-programming/codeforces`
  - Codeforces solutions, contest folders, and notebook drafts
  - includes `1669 Div.4`, `1927`, and `practice-`
- `practice/competitive-programming/spoj`
  - SPOJ solutions such as `VLN.py`, `WORDS1.py`, and helper files

- `practice/problem-solving/leetcode`
  - LeetCode solutions in `.py` and `.ipynb` format, plus input helper text files
- `practice/problem-solving/general-exercises/algorithms`
  - algorithm practice
- `practice/problem-solving/general-exercises/challenges`
  - small challenge scripts
- `practice/problem-solving/general-exercises/data-structures`
  - data-structure practice, including Segment Tree material
- `practice/problem-solving/general-exercises/others`
  - numbered problem files and miscellaneous exercises
- `practice/problem-solving/general-exercises/read-code`
  - read-and-understand exercises
- `practice/problem-solving/general-exercises/testing`
  - testing-focused exercise snippets
- `practice/problem-solving/general-exercises/`
  - also contains numbered root exercise files moved from the old `Exercises/` root

- `practice/training/python-training`
  - a separate training subtree with its own embedded `.git`
  - includes `Problems`, `python_classes`, `python_demo`, `python_global`, and `python_modules`

### `projects/`

Standalone projects grouped by domain.

#### `projects/automation-and-sc***ing/`

- `arabi-little-mag`
  - Selenium/undetected-chromedriver script for collecting links from the Al Arabi site
  - entry file: `get_links.py`
- `keyboard-presser`
  - pyautogui automation script for repeated keyboard input
  - entry file: `main.py`
- `marks-crawler`
  - scripts for sc***ing or posting to Syrian exam/marks pages
  - files include `main.py`, `get_makrs.py`, `old_test.py`, and `bdh.php`
- `parse-spoj-page`
  - fetches a SPOJ user page and derives problem names/links
  - entry file: `main.py`

#### `projects/computer-vision/`

- `camera-capture`
  - simple OpenCV camera capture example
- `digit-finder-cv`
  - screen-capture and CV experiments for digit/object detection
  - contains screenshots, intermediate processed images, notes, and an embedded `.git`
- `dollar-bill-reader-cv`
  - OCR experiment to extract a dollar bill serial number
  - includes sample bill images, `extract_serial.py`, `setup.sh`, and a checked-in `venv/`
- `face-detection`
  - mediapipe/OpenCV experiment, now normalized to `main.py`
- `image-experiments`
  - a large image/OCR workspace
  - main areas:
    - `OCR/`: OCR test images, papers, PDFs, and supporting folders
    - `PIL/`: PIL-related experiments
    - `python/`: notebooks and additional image/webcam experiments
- `monitor-mobile`
  - webcam/vision + websocket experiments
  - includes `eyes.py`, `web-socket-test.py`, a notebook, and pickle data
- `screen-ocr`
  - OCR-from-screen script based on a Stack Overflow source, with attribution already present in the file

#### `projects/data-and-storage/`

- `clean-duplicate-files`
  - duplicate-file detector by content hash
  - includes a test tree under `test/`
- `clustering-experiments`
  - plotting and k-means clustering experiments with numeric input files
- `sqlite-with-json`
  - experiments combining SQLite tables with JSON storage patterns
  - includes database files and several alternative approaches

#### `projects/document-tools/`

- `pdf-edit`
  - multiple attempts at PDF text replacement using `pdfrw`, `PyPDF2`, streams, and reportlab

#### `projects/games-and-ui/`

- `stars-and-bars`
  - small script with random/game-like helpers, normalized to `main.py`
- `stars-and-bars-game`
  - a mixed folder of terminal/asciimatics/image experiments around a stars-and-bars game idea
  - includes images, helper scripts, and tests
- `with-chatgpt`
  - simple GUI and activation/security toy examples
- `worldmap-test`
  - SVG world-map experiments and one notebook

#### `projects/text-and-parsing/`

- `questions-bank`
  - parser for Arabic multiple-choice question text with screenshots/assets
- `spell-checker`
  - dictionary-based spell checker using Levenshtein distance
  - includes full and shorter implementations plus `dict.txt`

#### `projects/web-and-api/`

- `api-tldr`
  - Flask app with templates, static assets, and a SQLite database
- `flask-experiments`
  - two Flask subprojects:
    - `flask-project1`
    - `flask-project2`
- `kafka-hello`
  - Docker Compose setup for a Kafka learning environment
- `quiz-app`
  - Flask + HTML/JS quiz app prototype with notes and data file
- `solved-problems-catalog`
  - a Python file containing a list of solved SPOJ problem links
- `stateful-cli-app`
  - simple persistent phone-book style CLI
- `web-python-js`
  - Flask + SQLite + static HTML project

### `reference/`

Small reference/scratch area.

- `reference/qa`
  - QA-style returned-value snippet
- `reference/testing`
  - simple testing/read-and-understand scripts

## Important Repository Notes

### Generated and Environment Folders

These were left in place because the request was to organize, not delete:

- many `__pycache__/` folders across learning and project areas
- `projects/computer-vision/dollar-bill-reader-cv/venv/`

This `venv/` is the main reason `projects/` has a much higher raw file count than the rest of the repo.

### Embedded Git Repositories

This repo contains nested git directories:

- `practice/training/python-training/.git`
- `projects/computer-vision/digit-finder-cv/.git`

The main repository root also has its own `.git/`.

### File Count Snapshot

Approximate current counts:

- `learning/`: 255 files
- `practice/`: 192 files
- `projects/`: 5061 files raw
- `projects/`: 494 files excluding `venv/` and `__pycache__/`
- `reference/`: 3 files

## Reorganization Summary

Major normalization performed:

- moved mixed top-level study folders under `learning/`
- moved exercises and competitive-programming work under `practice/`
- grouped standalone projects by domain under `projects/`
- normalized awkward project names such as:
  - `Digits Finder CV-` -> `digit-finder-cv`
  - `Marks Crawler` -> `marks-crawler`
  - `screen_ocr` -> `screen-ocr`
  - `x-project_spell_checker.py` -> `spell-checker`
  - `x-statefull.py` -> `stateful-cli-app`
- converted several single-file projects into folders with `main.py`

## Paths To Check First

If you want a fast guided tour, start here:

- `learning/lessons/`
- `learning/topic-labs/`
- `practice/competitive-programming/`
- `practice/problem-solving/leetcode/`
- `projects/computer-vision/`
- `projects/web-and-api/`
- `projects/data-and-storage/clean-duplicate-files/`

