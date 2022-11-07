import os
import re
import requests

assets = {
    'https://raw.githubusercontent.com/vincentdoerig/latex-css/master/': [
        'fonts/LM-regular.woff2', 'fonts/LM-italic.woff2',
        'fonts/LM-bold.woff2', 'fonts/LM-bold-italic.woff2', 'style.css',
        'prism/prism.css', 'prism/prism.js'
    ],
    'https://cdn.jsdelivr.net/npm/katex@0.16.3/dist/': [
        'fonts/KaTeX_AMS-Regular.woff2',
        'fonts/KaTeX_Caligraphic-Bold.woff2',
        'fonts/KaTeX_Caligraphic-Regular.woff2',
        'fonts/KaTeX_Fraktur-Bold.woff2',
        'fonts/KaTeX_Fraktur-Regular.woff2',
        'fonts/KaTeX_Main-Bold.woff2',
        'fonts/KaTeX_Main-BoldItalic.woff2',
        'fonts/KaTeX_Main-Italic.woff2',
        'fonts/KaTeX_Main-Regular.woff2',
        'fonts/KaTeX_Math-BoldItalic.woff2',
        'fonts/KaTeX_Math-Italic.woff2',
        'fonts/KaTeX_SansSerif-Bold.woff2',
        'fonts/KaTeX_SansSerif-Italic.woff2',
        'fonts/KaTeX_SansSerif-Regular.woff2',
        'fonts/KaTeX_Script-Regular.woff2',
        'fonts/KaTeX_Size1-Regular.woff2',
        'fonts/KaTeX_Size2-Regular.woff2',
        'fonts/KaTeX_Size3-Regular.woff2',
        'fonts/KaTeX_Size4-Regular.woff2',
        'fonts/KaTeX_Typewriter-Regular.woff2',
        'katex.js',
        'contrib/auto-render.js',
        'katex.css',
        'katex.mjs',
        'contrib/auto-render.mjs',
    ],
}

patches = {
    'style.css': {
        r"(?<=--body-bg-color: )hsl\(210, 20%, 98%\)":
        "#ffffff",
        r"(?<=--body-bg-color: )hsl\(0, 0%, 16%\)":
        "#1e1e1e",
        r"(?<=--pre-bg-color: )hsl\(210, 28%, 93%\)":
        "#f1f1f1",
        r"(?<=--pre-bg-color: )hsl\(0, 1%, 25%\)":
        "#161616",
        r"(?<=--body-color: )hsl\(0, 5%, 10%\)":
        "#000000",
        r"(?<=--body-color: )hsl\(0, 0%, 86%\)":
        "#d4d4d4",
        r"(?<=background: var\(--pre-bg-color\))":
        " !important",
        r"(?<=src: url)\('(.*?)'\) format\('woff2'\).*?format\('truetype'\)":
        r"(.\1) format('woff2')",
        r"(?<=body {)":
        "\n  display: flex;\n  flex-direction: column;",
        r"(?<=padding: )2rem 1.25rem":
        "1rem",  # body padding
        r"(?<=max-width: )80ch":
        "calc(100% - max(0rem, min(100% - 1050px, 0rem) + 28rem))",  # body width
        r"(?<=margin-right: )-20vw":
        "-14rem",  # sidenote margin
        r"(?<=width: )18vw":
        "13rem",  # sidenote width
        r"(?<=:root {)":
        """
  --webkit-scrollbar: hsl(0, 0%, 98%);
  --webkit-scrollbar-thumb: hsl(0, 0%, 67%);
  --webkit-scrollbar-thumb-hover: hsl(0, 0%, 53%);""",
        r"(?<=latex-dark \{)|(?<=latex-dark-auto \{)":
        """
  --webkit-scrollbar: hsl(0, 0%, 16%);
  --webkit-scrollbar-thumb: hsl(0, 0%, 33%);
  --webkit-scrollbar-thumb-hover: hsl(0, 0%, 47%);""",
        r"((?<=counter-increment: theorem;\n  display: )|(?<=counter-increment: definition;\n  display: )|(?<=.proof \{\n  display: ))block":
        "inline",
        r"(?<=theorem::before \{)":
        "\n  text-transform: capitalize;",
        r"(?<=content: )'Theorem '":
        "attr(title) ' '",
        r"\.proof:after \{.*?\}":
        "qed {\n  filter: var(--proof-symbol-filter);\n  float: right;\n}",
        r"\.footnotes \{.*?\}":
        "",
        r"$":
        """
.title, .title * {
  text-decoration: none;
}

.nav-header {
  display: flex;
  justify-content: space-around;
}

.nav-header > span > a {
  font-size: 1.2rem;
}

time {
  font-size: 1rem;
  font-weight: normal;
}

.post-title {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

header > h1 {
  margin-bottom: 0rem;
}

main {
  flex-grow: 1;
}

::-webkit-scrollbar {
	height: 8px;
	width: 8px;
	background-color: var(--webkit-scrollbar);
}

::-webkit-scrollbar-thumb {
	background-color: var(--webkit-scrollbar-thumb);
}

::-webkit-scrollbar-thumb:hover {
	background-color: var(--webkit-scrollbar-thumb-hover);
}

nav ul {
	counter-reset: item;
	padding-left: 2rem;
}

.caption-table {
  text-align: center;
  font-size: .923rem;
  padding-bottom: 1rem;
}

.caption-table::before {
  content: 'Table ' counter(caption) '. ';
  font-weight: bold;
}

table {
  margin-left: auto;
  margin-right: auto;
}

figure {
  counter-increment: figcaption;
}

.figure {
	margin-left: auto;
	margin-right: auto;
}

.caption-figure {
  text-align: center;
  padding-bottom: 1rem;
}

.caption-figure::before {
  content: 'Figure ' counter(figcaption) '. ';
  font-weight: bold;
}

:root {
	--selection-bg-color: #264f78;
}

::selection {
	background-color: var(--selection-bg-color);
}
""",
    },
    'katex.css': {
        r"(?<=src: url)\((.*?)\) format\('woff2'\).*?format\('truetype'\)":
        r"(../\1) format('woff2')",
        "1.21em":
        "1em",
        r"(?<=katex-display > \.katex \{)":
        "\n  overflow-x: auto;\n  overflow-y: hidden;",
    },
}

minify_paths = []


def download_file(url: str, path: str):
	print('Downloading', url)
	r = requests.get(url, allow_redirects=True)
	dir_path = os.path.dirname(path)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	open(path, 'wb').write(r.content)


def patch_file(path: str, patches: dict):
	print('Patching', path)
	with open(path, 'r', encoding='utf-8') as f:
		content = f.read()
	for pattern, replacement in patches.items():
		count = 0 if pattern != r'$' else 1
		content = re.sub(pattern, replacement, content, count, re.DOTALL)
	patch_path = path.rstrip(
	    path.split('.')[-1]) + 'patched.' + path.split('.')[-1]
	with open(patch_path, 'w', encoding='utf-8') as f:
		f.write(content)
	minify_paths.append(patch_path)


def main():
	for url, files in assets.items():
		for file in files:
			basename = file.split('/')[-1]
			extension = basename.split('.')[-1]
			dir = extension
			if extension == 'woff2':
				dir = 'fonts'
			elif extension == 'mjs':
				dir = 'js'
			path = f'static/assets/{dir}/{basename}'
			if extension in ['css', 'js']:
				minify_paths.append(path)
			download_file(url + file, path)
			if basename in patches:
				patch_file(path, patches[basename])

	for path in minify_paths:
		minified_path = path.rstrip(
		    path.split('.')[-1]) + 'min.' + path.split('.')[-1]
		print(f'Minifying {path} to {minified_path}')
		os.system(f'minify {path} > {minified_path}')


if __name__ == '__main__':
	main()