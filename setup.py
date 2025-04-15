from setuptools import setup, find_packages

setup(
    name="bmail",
    version="0.1.0",
    author="Ben Rinauto",
    author_email="ben.rinauto@gmail.com",  # Hardcoded instead of importing from config
    description="A simple Gmail client library designed for LLM integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benbuzz790/bmail",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "google-auth",  # Added this as it's required by auth.py
    ],
    test_suite="tests",
)
