import os
import click
import subprocess
from pathlib import Path

class Docker(object):

    def __init__(self,dry_run,*args,**kwargs):
        self.dry_run = dry_run
        self.root_name = 'piroot'
        self.path = Path(self.root_name)

    def _output(self,args):
        print(" ".join(args))
        if not self.dry_run:
            subprocess.run(args)

    def for_every_file(self,cmd_prefix,include_rel_path):
        for child in self.path.rglob('*'):
            if child.is_file():
                cmd = []
                cmd.extend(cmd_prefix)
                if include_rel_path:
                    cmd.append(str(child))
                abs_path = '/' / child.relative_to(self.root_name)
                cmd.append(str(abs_path))
                self._output(cmd)

    def install(self):
        self.for_every_file(['sudo', 'cp'],include_rel_path=True)

    def uninstall(self):
        self.for_every_file(['sudo', 'rm'],include_rel_path=False)

@click.group()
@click.option('-d','--dry-run', is_flag=True)
@click.pass_context
def cli(ctx,dry_run):
    if dry_run:
        click.echo('Dry Run')

    docker = Docker(dry_run)

    ctx.ensure_object(dict)
    ctx.obj['DOCKER'] = docker

@cli.command()
@click.pass_context
def install(ctx):
    click.echo('Installing')
    ctx.obj['DOCKER'].install()

@cli.command()
@click.pass_context
def uninstall(ctx):
    click.echo('Uninstalling')
    ctx.obj['DOCKER'].uninstall()

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    cli(obj={})
