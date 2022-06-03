SITE_NAME 		= ktyl.dev
# configured in ~/.ssh/config
HOST			= pluto
# a script on the remote server to move it on arrival
REMOTE_SCRIPT	= ./deploy-$(SITE_NAME)

SRC_DIR			= src
IMG_DIR			= img
OUT_DIR			= site

ROOT_DIR		= $(SRC_DIR)/root

BLOG_SRC_DIR	= blog/blogs
BLOG_OUT_DIR	= $(OUT_DIR)/blog
BLOG_TMP_DIR	= .blogtmp

PAGES 			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.html")
STYLES			= $(shell find $(ROOT_DIR) -wholename "$(ROOT_DIR)*.css")
BLOG_PAGES		= $(shell find $(BLOG_SRC_DIR) -wholename "$(BLOG_SRC_DIR)*.md")

IMAGES			= $(shell find $(IMG_DIR) -wholename "$(IMG_DIR)/*.png")

HTML_INCLUDES 	= $(shell find $(SRC_DIR)/inc_html -name *.html)
CSS_INCLUDES	= $(shell find $(SRC_DIR)/inc_css -name *.css)

BLOG_INDEX 			= $(OUT_DIR)/blog.html
BLOG_RSS			= $(BLOG_OUT_DIR)/index.xml
BLOG_INDEX_LINKS 	= $(BLOG_TMP_DIR)/blogindexlinks.html
BLOG_TARGETS		= $(BLOG_PAGES:$(BLOG_SRC_DIR)/%.md=$(BLOG_OUT_DIR)/%.html)

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

$(OUT_DIR)/%.html: $(ROOT_DIR)/%.html $(HTML_INCLUDES) $(BLOG_INDEX_LINKS) | $(OUT_DIR)
	python ppp/ppp.py $< $(HTML_INCLUDES) $(BLOG_INDEX_LINKS) > $@

$(OUT_DIR)/%.css: $(ROOT_DIR)/%.css $(CSS_INCLUDES) | $(OUT_DIR)
	python ppp/ppp.py $< $(CSS_INCLUDES) > $@

$(OUT_DIR):
	mkdir -p $@

blog: $(BLOG_TARGETS) $(BLOG_RSS) | $(BLOG_TMP_DIR)

$(BLOG_RSS): $(BLOG_PAGES)
	python scripts/mkblogrss.py $(BLOG_PAGES) > $@

$(BLOG_INDEX_LINKS): $(BLOG_TARGETS) | $(BLOG_TMP_DIR)
	python scripts/mkblogindex.py $(BLOG_TARGETS) > $@

$(BLOG_OUT_DIR)/%.html: $(BLOG_OUT_DIR)/%.html.tmp $(HTML_INCLUDES) $(CSS_TARGETS)
	python ppp/ppp.py $< $(HTML_INCLUDES) > $@
	cp $(CSS_TARGETS) `dirname $@`
	rm $<

$(BLOG_OUT_DIR)/%.html.tmp: $(BLOG_SRC_DIR)/%.md | $(BLOG_TMP_DIR) 
	python scripts/mkblog.py $< $@

$(BLOG_OUT_DIR): | $(OUT_DIR)
	mkdir -p $@

$(BLOG_TMP_DIR):
	mkdir -p $@


clean:
	rm -rf $(OUT_DIR) $(BLOG_TMP_DIR)

.PHONY: site
