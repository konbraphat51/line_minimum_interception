from setuptools import setup

setup(
    name="line_minimum_interception",
    version="0.0.1",
    description="project_description",
    url="https://github.com/author_name/project_urlname/",
    long_description="a",
    long_description_content_type="text/markdown",
    author="author_name",
    packages=["line_minimum_interception"],
    install_requires=["scipy", "matplotlib"],
    entry_points={
        "console_scripts": ["project_name = project_name.__main__:main"]
    },
)