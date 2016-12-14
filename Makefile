
.PHONY: publish-pages

publish-pages:
	git subtree push --prefix html origin gh-pages
