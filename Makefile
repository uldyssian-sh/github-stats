.PHONY: help install modern classic test clean

help: ## Show this help message
	@echo "GitHub Stats Generator Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

modern: ## Generate modern stats with GitHub logo
	python generate_modern_images.py

classic: ## Generate classic stats
	python generate_images.py

all: modern classic ## Generate both modern and classic stats

test: ## Test modern stats generation
	python test_modern_stats.py

clean: ## Clean generated files
	rm -f generated/*.svg

setup: install ## Setup environment and install dependencies
	@echo "✅ Setup complete! Set your ACCESS_TOKEN environment variable and run 'make modern'"