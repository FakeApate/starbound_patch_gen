import glob
import os
import shutil
import subprocess

import click
from dotenv import load_dotenv
from builder.helpers import (copy_file, create_patch_file, default_from_context,
                     set_unpacker_packer_paths)

load_dotenv()

folderOptionType = click.Path(
    exists=True, file_okay=False, dir_okay=True, resolve_path=True)


@click.group(chain=True)
@click.option('--starbound', type=folderOptionType, help="Path to Starbound directory", required=True)
@click.option('--modname', type=click.STRING, default="modcontent", help="Name of the mod, used for the packed mod file")
@click.option('--build_dir', type=click.Path(dir_okay=True, file_okay=False), default="out/", help="Build directory")
@click.pass_context
def cli(ctx, starbound, build_dir, modname):
    """
    Starbound Mod Builder CLI

    This CLI helps you build mods for Starbound by generating patch files for modified config files.
    """
    ctx.obj = {}
    ctx.obj["MOD_NAME"] = modname
    ctx.obj["BUILD_DIR"] = os.path.abspath(build_dir)
    ctx.obj["STARBOUND"] = os.path.abspath(starbound)
    ctx.obj["PACKED_ASSETS"] = os.path.abspath(
        os.path.join(starbound, 'assets/packed.pak'))
    ctx.obj["DEFAULT_ASSETS"] = os.path.abspath(
        os.path.join(ctx.obj["STARBOUND"], "_origAssets"))

    set_unpacker_packer_paths(ctx, starbound)


@click.command(help="Prepare by unpacking assets.")
@click.option("-d", "--destination", cls=default_from_context("DEFAULT_ASSETS"), type=click.Path(file_okay=False, dir_okay=True, resolve_path=True), help="Unpack location")
@click.pass_context
def prepare(ctx, destination):
    subprocess.run(args=[ctx.obj["UNPACKER"],
                   ctx.obj["PACKED_ASSETS"], destination])


@click.command(help="Build the mod by generating patch files for modified config files.")
@click.option("-s", "--source", cls=default_from_context("DEFAULT_ASSETS"), type=folderOptionType, help="Location of the original assets")
@click.option("-m", "--mod", default="_modAssets/", type=folderOptionType, help="Location of your modded assets")
@click.pass_context
def build(ctx, source, mod):
    for file in glob.iglob(os.path.join(mod, "**/*"), recursive=True):
        if os.path.isfile(file):
            _, file_extension = os.path.splitext(file)
            rel_file = os.path.relpath(file, mod)
            dst = os.path.join(ctx.obj["BUILD_DIR"], rel_file)

            if file_extension == ".config":
                create_patch_file(source, file, dst, mod)
            else:
                copy_file(file, dst)


@click.command(help="Pack the mod by creating a packed mod file.")
@click.option("-o", "--out", cls=default_from_context("MOD_NAME"), type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True), help="Packed Mod File")
@click.option("--overwrite", is_flag=True, help="Overwrite the output file if it already exists.")
@click.pass_context
def pack(ctx, out, overwrite):
    if os.path.splitext(out)[1] != ".pak":
        out = out + ".pak"

    if not os.path.exists(ctx.obj["BUILD_DIR"]):
        raise click.UsageError(f"Project is not builded. Use 'build' first.")
    if not overwrite and os.path.exists(out):
        raise click.UsageError(
            f"Output file '{out}' already exists. Use --overwrite to overwrite it.")

    subprocess.run(args=[ctx.obj["PACKER"], ctx.obj["BUILD_DIR"], out])


@click.command(help="Clean the build directory.")
@click.pass_context
def clean(ctx):
    shutil.rmtree(ctx.obj["BUILD_DIR"], ignore_errors=True)


cli.add_command(prepare)
cli.add_command(build)
cli.add_command(pack)
cli.add_command(clean)

if __name__ == "__main__":
    cli(auto_envvar_prefix='BUILDER')
