# new prompt of PS1
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "

# Other alias
alias cc='clear'
alias data='cd ~/data/'
alias work='cd ~/work/'
alias home='cd ~'

bind 'set show-all-if-ambiguous on'
bind 'set completion-ignore-case on'
bind 'TAB:menu-complete'

if [ -f /opt/conda/etc/profile.d/conda.sh ]; then
     . /opt/conda/etc/profile.d/conda.sh
fi

conda activate torch
cd ~/work/
