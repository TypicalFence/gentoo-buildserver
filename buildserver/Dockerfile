FROM gentoo/stage3

# All commands run from the git repository root!
# setup repos
RUN emerge-webrsync
RUN emerge dev-vcs/git
RUN emerge app-editors/vim
COPY buildserver/repos.conf /etc/portage/repos.conf
COPY buildserver/make.conf /etc/portage/make.conf
RUN mkdir /root/repo
COPY buildserver/ /root
WORKDIR /root

CMD ["/bin/bash"]
