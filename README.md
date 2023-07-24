# 1. Starbound Mod Builder

Starbound Mod Builder is a command-line tool that simplifies the process of building mods for Starbound. It generates patch files for modified configuration files, making it easier for modders to create and distribute their custom content.

## 1.1 Table of Contents

- [1. Starbound Mod Builder](#1-starbound-mod-builder)
  - [1.1 Table of Contents](#11-table-of-contents)
  - [1.2. Features](#12-features)
  - [1.3. Installation](#13-installation)
  - [1.4. Usage](#14-usage)
    - [1.4.1. Prepare Assets](#141-prepare-assets)
    - [1.4.2. Build the Mod](#142-build-the-mod)
    - [1.4.3. Pack the Mod](#143-pack-the-mod)
  - [1.5. Configuration](#15-configuration)
  - [1.6. Testing](#16-testing)
  - [1.7. Contributing](#17-contributing)
  - [1.8. License](#18-license)
  - [1.9. Contact](#19-contact)

## 1.2. Features

- Automatically generate patch files for modified config files.
- Pack the mod into a packed mod file for distribution.
- Unpack assets from the packed.pak file for easy access and modification.

## 1.3. Installation

You can install Starbound Mod Builder using [Poetry](https://python-poetry.org/):

```bash
poetry add starbound-patch-gen
```

Or you can install the wheel package with [pip](https://pip.pypa.io/en/stable/user_guide/)

- Download latest package here <https://github.com/FakeApate/starbound_patch_gen/releases/latest/>
- install with `pip install builder-X.X.X-py3-none-any.whl`

For ease of use add an `.env` file

```bash
BUILDER_STARBOUND="PathToStarbound"
BUILDER_MODNAME="ModName"
BUILDER_BUILD_DIR="PathToBuildDir"
```

## 1.4. Usage

### 1.4.1. Prepare Assets

Before building your mod, you need to unpack the original assets from the packed.pak file. Use the `prepare` command to do this:

```bash
builder prepare --destination /path/to/unpack/assets
```

### 1.4.2. Build the Mod

To build your mod, place your modified assets in the `_modAssets` folder and use the `build` command:

```bash
builder build --source /path/to/unpacked/assets --mod _modAssets/
```

The tool will generate patch files for the modified configuration files and copy other assets to the build directory.

### 1.4.3. Pack the Mod

Once your mod is built, you can pack it into a single mod file using the `pack` command:

```bash
builder pack -o /path/to/output/modfile.pak
```

Use the `--overwrite` flag to overwrite an existing output file.

## 1.5. Configuration

The Starbound Mod Builder uses the `config.py` module to store the OS-specific paths for the Starbound asset unpacker and packer. If the paths change in the future, you can update them in the `config.py` file.

## 1.6. Testing

I have included unit tests to ensure the correctness of the code. To run the tests, use the following command:

```bash
poetry run python -m unittest
```

## 1.7. Contributing

I welcome contributions to the Starbound Mod Builder project. If you have any ideas, bug reports, or feature requests, please open an issue or submit a pull request.

## 1.8. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 1.9. Contact

If you have any questions or need further assistance, you can create an issue in this repo.
