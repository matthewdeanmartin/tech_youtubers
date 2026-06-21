UV ?= uv
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

help:
	@echo 'Makefile for YouTubers on Mastodon'
	@echo ''
	@echo 'Page generation:'
	@echo '   make generate-pages    generate Pelican pages from data/ JSON'
	@echo '   make stubs             generate stub review/bio files'
	@echo ''
	@echo 'Site build:'
	@echo '   make html              (re)generate the web site'
	@echo '   make build             generate-pages + html'
	@echo '   make clean             remove the generated files'
	@echo '   make serve             serve site at http://localhost:8000'
	@echo '   make devserver         serve and auto-regenerate on change'
	@echo '   make publish           generate using production settings'
	@echo ''
	@echo 'Quality gates:'
	@echo '   make quality-python    lint generated HTML artifacts and internal links'
	@echo '   make quality-node      validate HTML, CSS browser support, and a11y'
	@echo '   make quality           build + all quality gates'

generate-pages:
	$(UV) run python generate_pages.py

stubs:
	$(UV) run python generate_review_stubs.py

build: generate-pages html

html:
	$(UV) run pelican "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

clean:
	$(UV) run python -c "import shutil; shutil.rmtree('output', ignore_errors=True)"

serve:
	$(UV) run pelican -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

devserver:
	$(UV) run pelican -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

publish:
	$(UV) run pelican "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)

quality-python: html
	$(UV) run python scripts/check_pelican_artifacts.py --site-dir "$(OUTPUTDIR)"
	$(UV) run python scripts/check_links.py --site-dir "$(OUTPUTDIR)" --internal-only

quality-node: html
	npm run quality

quality: build quality-python quality-node

.PHONY: help generate-pages stubs build html clean serve devserver publish quality-python quality-node quality
