from setuptools import setup, find_packages

setup(
    name='pdf_to_markdown',
    version='0.1.0',
    description='Enterprise PDF to Markdown converter for LLM optimization',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pdfminer.six',
    ],
    python_requires='>=3.7',
)
