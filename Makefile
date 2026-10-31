THEME_NAME := minima
DESTDIR ?=
PREFIX ?= /usr
THEMES_DIR ?= $(DESTDIR)$(PREFIX)/share/plymouth/themes/$(THEME_NAME)

.PHONY: all assets install uninstall preview

all: assets

assets:
	@python3 scripts/generate_assets.py

install:
	@install -d -m 755 $(THEMES_DIR)
	@install -d -m 755 $(THEMES_DIR)/assets
	@install -m 644 $(THEME_NAME).plymouth $(THEMES_DIR)/
	@install -m 644 $(THEME_NAME).script $(THEMES_DIR)/
	@install -m 644 assets/* $(THEMES_DIR)/assets/
	@if command -v plymouth-set-default-theme >/dev/null 2>&1; then \
		plymouth-set-default-theme -R $(THEME_NAME); \
	fi

uninstall:
	@rm -rf $(THEMES_DIR)

preview:
	@sudo ./scripts/preview.sh 6
