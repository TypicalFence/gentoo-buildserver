FROM gentoo/stage3

# All commands run from the git repository root!
# setup repos
RUN emerge-webrsync
RUN emerge dev-vcs/git
COPY buildserver/repos.conf /etc/portage/repos.conf
RUN mkdir /root/repo
COPY buildserver/ /root
WORKDIR /root

CMD ["/bin/bash"]
