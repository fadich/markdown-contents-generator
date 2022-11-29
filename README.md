# Markdown Contents Generator

Generate table of contents for markdown files.

- [Installation](#installation)
  - [Install via PIP](#install-via-pip)
  - [Install from Source](#install-from-source)
- [Usage](#usage)
  - [Generate Table of Contents](#generate-table-of-contents)
  - [Insert Table of Contents into a File](#insert-table-of-contents-into-a-file)
    - [Replace Contents Tags](#replace-contents-tags)

## Installation

### Install via PIP

Install via python _pip_ (python3 required):
```shell
pip install markdown-contents-generator --user
```

### Install from Source

Clone git-repository and make setup inside the project directory:
```shell
git clone https://github.com/fadich/markdown-contents-generator.git \
  && cd markdown-contents-generator

python3 setup.py install
```

## Usage

Once the package installed, it provides a console command:
```shell
md-contents-generator
```

You can call it with no arguments to view the instructions. The only required parameter is a path to the markdown file which table of contents you're going to generate.

### Generate Table of Contents

By proving `MARKDOWN_FILEPATH` positional parameter, you can generate its contents and check the console output results. For example:
```shell
md-contents-generator README.md
```

You will see something like that (for this README.md file):
```markdown
- [Installation](#installation)
  - [Install via PIP](#install-via-pip)
  - [Install from Source](#install-from-source)
- [Usage](#usage)
  - [Generate Table of Contents](#generate-table-of-contents)
  - [Insert Table of Contents into a File](#insert-table-of-contents-into-a-file)
    - [Replace Contents Tags](#replace-contents-tags)
```

You can copy-paste it to the file you need or make auto-insertion to your working file (see below).

### Insert Table of Contents into a File

Command can be called with optional `--insert` flag:
```shell
md-contents-generator README.md --insert
```

This will automatically insert auto-generated contents inside the _contents tags_. So, before calling this command, add these tags to your markdown file:
```markdown
...

<contents-start />
                     <--- Your table of contents will be inserted right here
<contents-finish />

...
```

Result should be like this:
```markdown
...

<contents-start />

- [Installation](#installation)
  - [Install via PIP](#install-via-pip)
  - [Install from Source](#install-from-source)
- [Usage](#usage)
  - [Generate Table of Contents](#generate-table-of-contents)
  - [Insert Table of Contents into a File](#insert-table-of-contents-into-a-file)
    - [Replace Contents Tags](#replace-contents-tags)

<contents-finish />

...
```

Note, that the insertion **replaces everything** inside the tags!

That's why, you can call it each time you update your markdown file to automatically update the table of contents. In common, these tags won't be rendered, and you can leave them in the source code if you prefer.

You can also add `style="display: none"` (or any other attributes) for your tags if needed. The only necessary is to keep the tags naming and put single tag on a single line (multiline tags do not supported).

#### Replace Contents Tags

If you'd like to insert table of contents but don't want to leave these contents tags, just call the command with both `--insert` and `--replace-tags` flags:
```shell
md-contents-generator README.md --insert --replace-tags
```

However, in this case, you will not be able to update you table of contents, and will have to generate and insert the table of contents each time manually.
