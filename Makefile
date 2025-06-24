.PHONY: help install test lint format clean docs demo

help:
    @echo "Cross-Border Semantic Negotiation - Available Commands:"
    @echo "  install    Install package in development mode"
    @echo "  test       Run test suite"
    @echo "  lint       Run linting checks"
    @echo "  format     Format code with black"
    @echo "  demo       Open the interactive demo"
    @echo "  clean      Clean up temporary files"
    @echo "  docs       Build documentation"

install:
    pip install -e ".[dev]"

test:
    pytest tests/ -v --cov=src

lint:
    flake8 src/ tests/
    mypy src/ --ignore-missing-imports

format:
    black src/ tests/ examples/

demo:
    @echo "Opening demo in your default browser..."
    @python -c "import webbrowser; webbrowser.open('file://$(PWD)/demo/cross_border_demo.html')"

clean:
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    rm -rf build/ dist/ *.egg-info/

docs:
    @echo "Documentation will be built with Sphinx"
    @echo "Run 'pip install sphinx' then 'sphinx-quickstart docs/'"
