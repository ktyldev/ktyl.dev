SRC_DIR			= src
OUT_DIR			= site

ROOT_DIR		= $(SRC_DIR)/root
INC_HTML		= $(SRC_DIR)/inc_html
INC_CSS 		= $(SRC_DIR)/inc_css

PAGES 			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.html")
HTML_INCLUDES 	= $(shell find $(INC_HTML) -name *.html)
HTML_TARGETS 	= $(PAGES:$(ROOT_DIR)/%.html=$(OUT_DIR)/%.html)

STYLES			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.css")
CSS_INCLUDES	= $(shell find $(INC_CSS) -name *.css)
CSS_TARGETS 	= $(STYLES:$(ROOT_DIR)/%.css=$(OUT_DIR)/%.css)

run: $(HTML_TARGETS) $(CSS_TARGETS)

$(OUT_DIR)/%.html: $(ROOT_DIR)/%.html $(HTML_INCLUDES)
	mkdir -p $(OUT_DIR)
	python ppp/ppp.py $< $(HTML_INCLUDES) > $@

$(OUT_DIR)/%.css: $(ROOT_DIR)/%.css $(CSS_INCLUDES)
	mkdir -p $(OUT_DIR)
	python ppp/ppp.py $< $(CSS_INCLUDES) > $@

clean: 
	rm -r $(OUT_DIR)
