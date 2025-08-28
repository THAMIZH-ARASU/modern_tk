from setuptools import setup, find_packages

setup(
    name="modern-tk",
    version="0.1.0",
    description="Modern, CSS-inspired styling for Tkinter applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Modern TK Team",
    author_email="team@modern-tk.com",
    url="https://github.com/modern-tk/modern-tk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    include_package_data=True,
    package_data={
        "modern_tk": ["assets/**/*"],
    },
)