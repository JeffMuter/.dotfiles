here be our description of the project, & how to use it.

if nix & zsh are configured properly (which, if you're here, they must not be), then you should be able to use 3 commands to control stow on our setup.

dp = dotfiles push

dl = dotfiles pull

ds = dotfiles sync

What's going on, in terms of commands happening?

Firstly, we're using Stow's command: stow -R *

-R means we're going to 're-stow' * = all of the directories. So, we're saying whatever the state of this repo is, add files into the system, rewrite them if need be. A bit intense, but it's important because if you update a file on another system, then we don't want to not update that file on this system.

Then we're using git, to pull / push.

So if you don't have access to those commands, the workflow looks like:

      dot-push() {
        echo "Syncing dotfiles from $(hostname)..."
        cd ~/.dotfiles || return 1
        stow -R * 2>/dev/null
        git add .
        git commit -m "sync: $(hostname) $(date '+%H:%M')" 2>/dev/null || echo "No changes to commit"
        git push origin master
        echo "Dotfiles pushed"
      }
      
      dot-pull() {
        echo "Pulling dotfiles to $(hostname)..."
        cd ~/.dotfiles || return 1
        git pull
        stow -R * --adopt 2>/dev/null
        git add . 2>/dev/null
        git commit -m "adopt: $(hostname) $(date '+%H:%M')" 2>/dev/null || true
        git push origin master 2>/dev/null || true
        echo "Dotfiles synced"
      }

Simple but effective.
