.PHONY: run setup clean

VENV = venv

setup:
	@echo "Creating virtual environment..."
	python -m venv $(VENV)
	@echo "Installing dependencies..."
	@if [ -f "$(VENV)/bin/activate" ]; then \
		. $(VENV)/bin/activate && pip install -r requirements.txt; \
	elif [ -f "$(VENV)/Scripts/activate" ]; then \
		. $(VENV)/Scripts/activate && pip install -r requirements.txt; \
	fi
	@echo "Setup complete!"

run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Running setup..."; \
		$(MAKE) setup; \
	fi
	@echo "Starting food tracker..."
	@if [ -f "$(VENV)/bin/python" ]; then \
		$(VENV)/bin/python food_tracker.py; \
	elif [ -f "$(VENV)/Scripts/python.exe" ]; then \
		$(VENV)/Scripts/python.exe food_tracker.py; \
	else \
		echo "Python not found in virtual environment"; \
		exit 1; \
	fi

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf modules/__pycache__
	rm -rf __pycache__
	rm -rf *.pyc
	@echo "Clean complete!"