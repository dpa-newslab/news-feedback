SERVER      := werkzeugkasten
REMOTE_HOME := /srv/newsstream-branchen
PROJECT     := newsstream-branchen


.PHONY: publish-pages publish-werkzeugkasten remote

publish-pages:
	git subtree push --prefix html origin gh-pages

publish-werkzeugkasten:
	rsync -av html/ werkzeugkasten:/srv/newsstream-branchen/newsstream-branchen



remote :
	expect -c 'spawn ssh $(SERVER); send "cd $(REMOTE_HOME);  tmux new-session -s $(PROJECT) || tmux attach -t $(PROJECT)\r"; interact '
