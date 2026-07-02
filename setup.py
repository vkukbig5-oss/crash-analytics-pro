from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crash-analytics-pro",
    version="0.1.0",
    author="vkukbig5-oss",
    description="Production-quality analytics platform with plugin-based Reader architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vkukbig5-oss/crash-analytics-pro",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    install_requires=[
        "PySide6>=6.7.0",
        "PyQtGraph>=0.13.7",
        "SQLAlchemy>=2.0.0",
        "pandas>=2.2.0",
        "openpyxl>=3.1.0",
        "PyYAML>=6.0",
        "aiofiles>=23.2.0",
        "aiohttp>=3.9.0",
        "click>=8.1.0",
        "requests>=2.31.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
    ],
)
