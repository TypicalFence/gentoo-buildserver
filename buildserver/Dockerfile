FROM gentoo/stage3

# All commands run from the git repository root!
# setup repos
RUN emerge-webrsync
RUN emerge dev-vcs/git
COPY buildserver/repos.conf /etc/portage/repos.conf

# copy repositry root to the repo folder
COPY . /var/db/repos/gentoo-buildserver 
RUN ./var/db/repos/gentoo-buildserver/buildserver/sync_custom_repos.sh

CMD ["/bin/bash"]
