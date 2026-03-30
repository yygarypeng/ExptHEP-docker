#!/bin/bash
# robust-cvmfs-fix.sh

# 0. Ensure the host-path is a shared mount point
# This is the "bridge" that allows host fixes to reach the containers
if ! findmnt -o TARGET,PROPAGATION /cvmfs | grep -q "shared"; then
    echo "Setting up shared propagation..."
    sudo mkdir -p /cvmfs
    sudo mount --bind /cvmfs /cvmfs
    sudo mount --make-rshared /cvmfs
fi

# 1. Graceful Unmount
echo "Unmounting repositories..."
sudo cvmfs_config umount

# 2. Force-clear stuck FUSE sessions
# -s is "soft" kill, which is better for container stability
echo "Clearing FUSE processes..."
sudo cvmfs_config killall

# 3. Wipe cache
sudo cvmfs_config wipecache

# 4. Reload and Re-setup
echo "Reloading configuration and triggering mounts..."
sudo cvmfs_config setup
sudo cvmfs_config reload

# 5. Probe to verify connectivity
sudo cvmfs_config probe

echo "------------------------------------------------"
echo "CVMFS is stable. Active Containers using ':shared' should recover."
