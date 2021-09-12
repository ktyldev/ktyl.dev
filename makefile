SRC_DIR			= src
OUT_DIR			= site

ROOT_DIR		= $(SRC_DIR)/root
INCLUDE_DIR		= $(SRC_DIR)/include

PAGES 			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.html")
HTML_INCLUDES 	= $(shell find $(INCLUDE_DIR) -name *.html)
HTML_TARGETS 	= $(PAGES:$(ROOT_DIR)/%.html=$(OUT_DIR)/%.html)

STYLES			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.css")
CSS_TARGETS 	= $(STYLES:$(ROOT_DIR)/%.css=$(OUT_DIR)/%.css)

run: $(HTML_TARGETS) $(CSS_TARGETS)

$(OUT_DIR)/%.html: $(ROOT_DIR)/%.html $(HTML_INCLUDES)
	mkdir -p $(OUT_DIR)
	python ppp.py $< $(HTML_INCLUDES) > $@

$(OUT_DIR)/%.css: $(ROOT_DIR)/%.css
	cp $< $@

clean: 
	rm -r $(OUT_DIR)
