# Makefile for Terrorism Analysis Project

# Variables
VENV_NAME = .venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
DATA_FILE = globalterrorismdb_0522dist.xlsx
DATA_ZIP = globalterrorismdb_0522dist.zip

# Default target
all: setup data

# Create virtual environment and install dependencies
setup: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Setup complete!"

# Extract data file if it doesn't exist
data: $(DATA_FILE)

$(DATA_FILE): $(DATA_ZIP)
	@echo "Extracting data file..."
	unzip -o $(DATA_ZIP)
	@echo "Data extraction complete!"

# Run the Streamlit app
run: setup data
	@echo "Starting Streamlit app..."
	$(PYTHON) -m streamlit run streamlit_app.py

# Run data exploration script
explore: setup data
	@echo "Running data exploration..."
	$(PYTHON) explore_data.py

# Activate virtual environment (interactive shell)
shell: setup
	@echo "Activating virtual environment..."
	@echo "Type 'exit' to leave the virtual environment"
	@bash --rcfile <(echo '. ~/.bashrc; source $(VENV_NAME)/bin/activate; PS1="(.venv) $$PS1"')

# Clean up generated files
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	rm -f $(DATA_FILE)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Clean everything including the zip file
clean-all: clean
	rm -f $(DATA_ZIP)

# Install only (without data extraction)
install: setup

# Check if data file exists
check-data:
	@if [ -f "$(DATA_FILE)" ]; then \
		echo "✓ Data file exists: $(DATA_FILE)"; \
		ls -lh $(DATA_FILE); \
	else \
		echo "✗ Data file missing: $(DATA_FILE)"; \
		echo "Run 'make data' to extract it from $(DATA_ZIP)"; \
	fi

# Show help
help:
	@echo "Available targets:"
	@echo "  all      - Setup environment and extract data (default)"
	@echo "  setup    - Create virtual environment and install dependencies"
	@echo "  data     - Extract data file from zip"
	@echo "  run      - Start the Streamlit application"
	@echo "  explore  - Run the data exploration script"
	@echo "  shell    - Activate virtual environment (interactive shell)"
	@echo "  install  - Install dependencies only"
	@echo "  check-data - Check if data file exists"
	@echo "  clean    - Remove virtual environment and extracted data"
	@echo "  clean-all - Remove everything including zip file"
	@echo "  help     - Show this help message"

# Declare phony targets
.PHONY: all setup data run explore shell clean clean-all install check-data help
