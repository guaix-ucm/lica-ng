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
tools:
    uv tool install uv-publish

# Creates virtual env
init:
    uv sync

# sets the packahe version and modifies pyproject.toml
version pkg version:
    uv version --package {{pkg}} {{version}}

# Build the package
build pkg:
    #!/usr/bin/env bash
    set -exuo pipefail
    pkg={{pkg}}
    rm -fr dist/${pkg}/*
    uv build --package "${pkg}" --out-dir dist/${pkg}


test-publish pkg:
    #!/usr/bin/env bash
    set -exuo pipefail
    pkg={{pkg}}
    module="${pkg//-/_}"

    test -n "$(find "dist/${pkg}" -maxdepth 1 -type f \( -name '*.whl' -o -name '*.tar.gz' \) -print -quit)" || {
            echo "No distributions found in dist/${pkg}" >&2
            exit 1
        }

    uvx uv-publish --repository testpypi --verbose "dist/${pkg}/*"
    uv run --index "https://test.pypi.org/simple/" --with ${pkg} --no-project python -c "from ${module} import __version__; print(__version__)"

publish pkg:
    #!/usr/bin/env bash
    set -exuo pipefail
    pkg={{pkg}}
    module="${pkg//-/_}"
    uvx uv-publish ${pkg} --verbose "dist/${pkg}/*"
    uv run --with ${pkg} --no-project python -c "from ${module} import __version__; print(__version__)"
