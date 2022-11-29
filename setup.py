import os

from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as file:
        return file.read()


setup(
    name="markdown_contents_generator",
    version="0.1.2",
    keywords=[
        "markdown-contents-generator",
        "md-contents-generator",
        "md",
        "markdown",
        "contents",
        "contents-generator",
        "generator",
        "content",
    ],
    url="https://github.com/fadich/markdown-contents-generator",
    author="Fadi A.",
    author_email="royalfadich@gmail.com",
    description="Generate table of contents for markdown files",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(
        include=[
            "markdown_contents_generator",
            "markdown_contents_generator.*",
            "markdown_contents_generator/cli/*"
        ]
    ),
    requires=[
    ],
    scripts=[
        "markdown_contents_generator/cli/md-contents-generator"
    ]
)
