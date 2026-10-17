# To install just on a per-project basis
# 1. Activate your virtual environemnt
# 2. uv add --dev rust-just
# 3. Use just within the activated environment

#drive_uuid := "77688511-78c5-4de3-9108-b631ff823ef4"
drive_uuid := "8425-155D"

user :=  file_stem(home_dir())
def_drive := join("/media", user, drive_uuid)
project := file_stem(justfile_dir())
local_env := join(justfile_dir(), ".env")


# list all recipes
default:
    just --list

# --------------------
# Workspace management
# --------------------

init:
    uv sync

version pkg version:
    uv version --package {{pkg}} {{version}}

# Build the package
build pkg="":
    #!/usr/bin/env bash
    set -exuo pipefail
    pkg={{pkg}}
    if [ "${pkg}" != "" ]; then
         uv build --package ${pkg}
    else
         uv build --all-packages
    fi
