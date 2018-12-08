SLUG = blank

SLIDE_HTML = $(SLUG).html
ZIP_FILE = $(SLUG).zip

SUPPORT = lineselect.js slides.js slides.css
IMAGES = *.jpg *.png
VENDOR = slippy highlight

.PHONY: $(SLIDE_HTML)

SAMPLES = sample.py

OUTPUT = sample.out

slides: $(SLIDE_HTML)

$(SLIDE_HTML): $(OUTPUT)
	python -m cogapp -r $@

%.out: %.py
	python $*.py > $@ 2>&1

PNG_DIR = png

clean:
	rm -f *.pyc $(PX)
	rm -f $(OUTPUT)
	rm -rf __pycache__
	rm -rf $(PNG_DIR)
	rm -f $(ZIP_FILE)

sterile: clean
	python -m cogapp -x -r $(SLIDE_HTML)

pngs:
	phantomjs phantom-slippy-to-png.js $(SLIDE_HTML) $(PNG_DIR)/

PX = $(SLUG).px

px $(PX): $(SLIDE_HTML)
	python slippy_to_px.py $(SLIDE_HTML) $(PX) $(SLUG)

WEBHOME = ~/web/stellated/pages/text
WEBPREZHOME = $(WEBHOME)/$(SLUG)
WEBPIXHOME = $(WEBHOME)/$(SLUG)_pix

publish: $(PX) pngs
	mkdir -p $(WEBPREZHOME) $(WEBPIXHOME)
	cp -f $(PX) $(WEBHOME)
	cp -f $(PNG_DIR)/* $(WEBPIXHOME)
	cp -f $(SLIDE_HTML) $(WEBPREZHOME)/$(SLUG).html
	cp -f $(SUPPORT) $(WEBPREZHOME)
	cp -f $(IMAGES) $(WEBPREZHOME)
	cp -rf $(VENDOR) $(WEBPREZHOME)

ZIP_EXTRA = captioning.html

zip $(ZIP_FILE): $(SLIDE_HTML)
	zip -r $(ZIP_FILE) $(SLIDE_HTML) $(SUPPORT) $(IMAGES) $(ZIP_EXTRA) $(VENDOR)
