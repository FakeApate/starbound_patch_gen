import os
import shutil
import jsonpatch
import json5 as json
import click
from builder import config
import platform


def create_patch_file(source, file, dst, mod):
    orig_src = os.path.join(source, os.path.relpath(file, mod))
    patch_file = dst + ".patch"
    os.makedirs(os.path.dirname(patch_file), exist_ok=True)

    with open(orig_src, "r", encoding="utf-8") as orig_file, open(file, "r", encoding="utf-8") as mod_file:
        orig_json = json.load(orig_file)
        mod_json = json.load(mod_file)
        patch_json = jsonpatch.make_patch(orig_json, mod_json)

    with open(patch_file, "w", encoding="utf-8") as patch_fs:
        patch_fs.write(patch_json.to_string())


def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)


def default_from_context(default_name):
    class OptionDefaultFromContext(click.Option):
        def get_default(self, ctx: any, call: bool = True):
            self.default = ctx.obj[default_name]
            return super(OptionDefaultFromContext, self).get_default(ctx, call)
    return OptionDefaultFromContext


def set_unpacker_packer_paths(ctx, starbound):
    system = platform.system()
    if system in config.os_paths:
        ctx.obj["UNPACKER"] = os.path.abspath(os.path.join(
            starbound, config.os_paths[system]["UNPACKER"]))
        ctx.obj["PACKER"] = os.path.abspath(os.path.join(
            starbound, config.os_paths[system]["PACKER"]))
    else:
        raise click.UsageError("System not known", ctx)
