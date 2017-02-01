SERVER      := werkzeugkasten
REMOTE_HOME := /srv/newsstream-branchen
PROJECT     := newsstream-branchen
HTPASSWD    := /etc/nginx/newsstream-branchen.htpasswd

.PHONY: publish-pages publish-werkzeugkasten remote

publish-pages:
	git subtree push --prefix html origin gh-pages

publish-werkzeugkasten:
	rsync -av html/ werkzeugkasten:/srv/newsstream-branchen/newsstream-branchen


list-users: 
	ssh $(SERVER) sudo cat $(HTPASSWD)

set-password:
	$(call check_defined, HTTP_USER, 'Use HTTP_USER=xxxx to change password for user xxxx')
	ssh $(SERVER) sudo htpasswd $(HTPASSWD) $(HTTP_USER)


remote :
	expect -c 'spawn ssh $(SERVER); send "cd $(REMOTE_HOME);  tmux new-session -s $(PROJECT) || tmux attach -t $(PROJECT)\r"; interact '


bundles :
	python newsbundle-generator/sector_newscrawl.py
	python newsbundle-generator/sector_dpa.py

# call like this:
# $(call check_defined, DB_HOST DB_USER DB_PASSWORD DB_DATABASE, 'Not all DB parameters defined.')
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
        $(error Undefined $1$(if $2, ($2))$(if $(value @), \
                required by target `$@')))
