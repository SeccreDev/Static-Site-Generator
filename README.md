# Static Markdown Site Generator

This is a simple static site generator written in Python. It converts a directory of Markdown (`.md`) files into styled HTML pages using a HTML template. The output is served as a complete, ready-to-deploy static website.

## Features

- Parses and converts Markdown content into HTML
- Supports inline formatting:
  - **Bold**, _Italic_, `Code`
  - Links and Images
- Supports block types:
  - Paragraphs
  - Headings 
  - Code blocks 
  - Blockquotes 
  - Ordered and unordered lists
- Automatically wraps content using a shared HTML template
- Outputs to a `docs/` directory (configurable)
- Fully recursive processing of nested content folders

## Installation
1. Clone the Repository

```sh
https://github.com/SeccreDev/Static-Site-Generator.git
```

2. Navigate to the project folder:
```sh
cd markdown-site-generator
```

## Usage

### 1. Add Your Content

Place your Markdown files inside the `content/` directory. Place your images inside the `static/images` directory. Files can be nested in folders.

### 2. Run the Generator
To run locally use:
```
python3 main.sh
```
You can also specify a base path:
```
python3 src/main.py /base-path/
```

