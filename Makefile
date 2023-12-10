# set up development environment
# these assume you have created a virtual environment already and activated it
# ex.) python3 -m venv venv && source venv/bin/activate

dev:
	python3 -m pip install -r requirements.txt

test-files:
	python -m generate_test_files

play:
	python -m player --file data/jupiter1.mp4 --n 10



# Run development pipelines for various components of the workflow

stabilizer:
	python -m stabilization_pipeline_dev

quality:
	python -m quality_pipeline_dev
