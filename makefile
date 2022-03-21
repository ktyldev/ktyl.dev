SITE_NAME 		= ktyl.dev
# configured in ~/.ssh/config
HOST			= pluto
# a script on the remote server to move it on arrival
REMOTE_SCRIPT	= ./deploy-$(SITE_NAME)

SRC_DIR			= src
IMG_DIR			= img
OUT_DIR			= site

ROOT_DIR		= $(SRC_DIR)/root

PAGES 			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.html")
STYLES			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.css")

IMAGES			= $(shell find $(IMG_DIR) -wholename "$(IMG_DIR)/*.png")

HTML_INCLUDES 	= $(shell find $(SRC_DIR)/inc_html -name *.html)
CSS_INCLUDES	= $(shell find $(SRC_DIR)/inc_css -name *.css)

HTML_TARGETS 	= $(PAGES:$(ROOT_DIR)/%.html=$(OUT_DIR)/%.html)
CSS_TARGETS 	= $(STYLES:$(ROOT_DIR)/%.css=$(OUT_DIR)/%.css)
PNG_TARGETS		= $(IMG_DIR)/%.png=$(OUT_DIR)/%.png

site: $(HTML_TARGETS) $(CSS_TARGETS)
	cp $(IMG_DIR)/*.png $(OUT_DIR)/

run: site

deploy: site
	cp -r $(OUT_DIR) $(SITE_NAME)
	rsync -rP $(SITE_NAME) $(HOST):~
	rm -r $(SITE_NAME)
	ssh $(HOST) "sudo $(REMOTE_SCRIPT)"

$(OUT_DIR)/%.html: $(ROOT_DIR)/%.html $(HTML_INCLUDES)
	mkdir -p $(OUT_DIR)
	python ppp/ppp.py $< $(HTML_INCLUDES) > $@

$(OUT_DIR)/%.css: $(ROOT_DIR)/%.css $(CSS_INCLUDES)
	mkdir -p $(OUT_DIR)
	python ppp/ppp.py $< $(CSS_INCLUDES) > $@

clean: 
	rm -r $(OUT_DIR)

.PHONY: site
