# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import os
import pytest
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

# https://stackoverflow.com/a/19011259
import types
import importlib.machinery
loader = importlib.machinery.SourceFileLoader(
    'beman_submodule',
    str(Path(__file__).parent.resolve().parent / 'beman-submodule'))
beman_submodule = types.ModuleType(loader.name)
loader.exec_module(beman_submodule)

def create_test_git_repository():
    tmpdir = tempfile.TemporaryDirectory()
    tmp_path = Path(tmpdir.name)

    subprocess.run(['git', 'init'], check=True, cwd=tmpdir.name, capture_output=True)
    def make_commit(a_txt_contents):
        with open(tmp_path / 'a.txt', 'w') as f:
            f.write(a_txt_contents)
        subprocess.run(
            ['git', 'add', 'a.txt'], check=True, cwd=tmpdir.name, capture_output=True)
        subprocess.run(
            ['git', '-c', 'user.name=test', '-c', 'user.email=test@example.com', 'commit',
             '--author="test <test@example.com>"', '-m', 'test'],
            check=True, cwd=tmpdir.name, capture_output=True)
    make_commit('A')
    make_commit('a')
    return tmpdir

def test_directory_compare():
    def create_dir_structure(dir_path: Path):
        bar_path = dir_path / 'bar'
        os.makedirs(bar_path)

        with open(dir_path / 'foo.txt', 'w') as f:
            f.write('foo')
        with open(bar_path / 'baz.txt', 'w') as f:
            f.write('baz')

    with tempfile.TemporaryDirectory() as dir_a, \
         tempfile.TemporaryDirectory() as dir_b:
        path_a = Path(dir_a)
        path_b = Path(dir_b)

        create_dir_structure(path_a)
        create_dir_structure(path_b)

        assert beman_submodule.directory_compare(dir_a, dir_b, [])

        with open(path_a / 'bar' / 'quux.txt', 'w') as f:
            f.write('quux')

        assert not beman_submodule.directory_compare(path_a, path_b, [])
        assert beman_submodule.directory_compare(path_a, path_b, ['quux.txt'])

def test_parse_beman_submodule_file():
    def valid_file():
        tmpfile = tempfile.NamedTemporaryFile()
        tmpfile.write('[beman_submodule]\n'.encode('utf-8'))
        tmpfile.write(
            'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
        tmpfile.write(
            'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
        tmpfile.flush()
        module = beman_submodule.parse_beman_submodule_file(tmpfile.name)
        assert module.dirpath == Path(tmpfile.name).resolve().parent
        assert module.remote == 'git@github.com:bemanproject/infra.git'
        assert module.commit_hash == '9b88395a86c4290794e503e94d8213b6c442ae77'
    valid_file()
    def invalid_file_missing_remote():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[beman_submodule]\n'.encode('utf-8'))
            tmpfile.write(
                'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
            tmpfile.flush()
            beman_submodule.parse_beman_submodule_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_missing_remote()
    def invalid_file_missing_commit_hash():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[beman_submodule]\n'.encode('utf-8'))
            tmpfile.write(
                'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
            tmpfile.flush()
            beman_submodule.parse_beman_submodule_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_missing_commit_hash()
    def invalid_file_wrong_section():
        threw = False
        try:
            tmpfile = tempfile.NamedTemporaryFile()
            tmpfile.write('[invalid]\n'.encode('utf-8'))
            tmpfile.write(
                'remote=git@github.com:bemanproject/infra.git\n'.encode('utf-8'))
            tmpfile.write(
                'commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77\n'.encode('utf-8'))
            tmpfile.flush()
            beman_submodule.parse_beman_submodule_file(tmpfile.name)
        except:
            threw = True
        assert threw
    invalid_file_wrong_section()

def test_get_beman_submodule():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    assert beman_submodule.get_beman_submodule('foo')
    os.remove('foo/.beman_submodule')
    assert not beman_submodule.get_beman_submodule('foo')
    os.chdir(original_cwd)

def test_find_beman_submodules_in():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    beman_submodule.add_command(tmpdir.name, 'bar')
    beman_submodules = beman_submodule.find_beman_submodules_in(tmpdir2.name)
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    assert beman_submodules[0].dirpath == Path(tmpdir2.name) / 'bar'
    assert beman_submodules[0].remote == tmpdir.name
    assert beman_submodules[0].commit_hash == sha
    assert beman_submodules[1].dirpath == Path(tmpdir2.name) / 'foo'
    assert beman_submodules[1].remote == tmpdir.name
    assert beman_submodules[1].commit_hash == sha
    os.chdir(original_cwd)

def test_cwd_git_repository_path():
    original_cwd = Path.cwd()
    tmpdir = tempfile.TemporaryDirectory()
    os.chdir(tmpdir.name)
    assert not beman_submodule.cwd_git_repository_path()
    subprocess.run(['git', 'init'])
    assert beman_submodule.cwd_git_repository_path() == tmpdir.name
    os.chdir(original_cwd)

def test_clone_beman_submodule_into_tmpdir():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD^'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    beman_submodule.add_command(tmpdir.name, 'foo')
    module = beman_submodule.get_beman_submodule(Path(tmpdir2.name) / 'foo')
    module.commit_hash = sha
    tmpdir3 = beman_submodule.clone_beman_submodule_into_tmpdir(module, False)
    assert not beman_submodule.directory_compare(tmpdir.name, tmpdir3.name, ['.git'])
    tmpdir4 = beman_submodule.clone_beman_submodule_into_tmpdir(module, True)
    assert beman_submodule.directory_compare(tmpdir.name, tmpdir4.name, ['.git'])
    subprocess.run(
        ['git', 'reset', '--hard', sha], capture_output=True, check=True,
        cwd=tmpdir.name)
    assert beman_submodule.directory_compare(tmpdir.name, tmpdir3.name, ['.git'])
    os.chdir(original_cwd)

def test_beman_submodule_status():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    assert '  ' + sha + ' foo' == beman_submodule.beman_submodule_status(
        beman_submodule.get_beman_submodule(Path(tmpdir2.name) / 'foo'))
    with open(Path(tmpdir2.name) / 'foo' / 'a.txt', 'w') as f:
        f.write('b')
    assert '+ ' + sha + ' foo' == beman_submodule.beman_submodule_status(
        beman_submodule.get_beman_submodule(Path(tmpdir2.name) / 'foo'))
    os.chdir(original_cwd)

def test_update_command_no_paths():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    beman_submodule.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD^'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    subprocess.run(
        ['git', 'reset', '--hard', sha], capture_output=True, check=True,
        cwd=tmpdir.name)
    with open(Path(tmpdir2.name) / 'foo' / '.beman_submodule', 'w') as f:
        f.write(f'[beman_submodule]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    with open(Path(tmpdir2.name) / 'bar' / '.beman_submodule', 'w') as f:
        f.write(f'[beman_submodule]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    beman_submodule.update_command(tmpdir.name, None)
    assert beman_submodule.directory_compare(
        tmpdir.name, Path(tmpdir2.name) / 'foo', ['.git', '.beman_submodule'])
    assert beman_submodule.directory_compare(
        tmpdir.name, Path(tmpdir2.name) / 'bar', ['.git', '.beman_submodule'])
    os.chdir(original_cwd)

def test_update_command_with_path():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    tmpdir_copy1 = tempfile.TemporaryDirectory()
    shutil.copytree(tmpdir.name, tmpdir_copy1.name, dirs_exist_ok=True)
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    beman_submodule.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD^'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    subprocess.run(
        ['git', 'reset', '--hard', sha], capture_output=True, check=True,
        cwd=tmpdir.name)
    with open(Path(tmpdir2.name) / 'foo' / '.beman_submodule', 'w') as f:
        f.write(f'[beman_submodule]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    with open(Path(tmpdir2.name) / 'bar' / '.beman_submodule', 'w') as f:
        f.write(f'[beman_submodule]\nremote={tmpdir.name}\ncommit_hash={sha}\n')
    beman_submodule.update_command(tmpdir.name, 'foo')
    assert beman_submodule.directory_compare(
        tmpdir.name, Path(tmpdir2.name) / 'foo', ['.git', '.beman_submodule'])
    assert beman_submodule.directory_compare(
        tmpdir_copy1.name, Path(tmpdir2.name) / 'bar', ['.git', '.beman_submodule'])
    os.chdir(original_cwd)

def test_add_command():
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    sha = sha_process.stdout.strip()
    assert beman_submodule.directory_compare(
        tmpdir.name, Path(tmpdir2.name) / 'foo', ['.git', '.beman_submodule'])
    with open(Path(tmpdir2.name) / 'foo' / '.beman_submodule', 'r') as f:
        assert f.read() == f'[beman_submodule]\nremote={tmpdir.name}\ncommit_hash={sha}\n'
    os.chdir(original_cwd)

def test_status_command_no_paths(capsys):
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    beman_submodule.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    with open(Path(tmpdir2.name) / 'bar' / 'a.txt', 'w') as f:
        f.write('b')
    beman_submodule.status_command([])
    sha = sha_process.stdout.strip()
    assert capsys.readouterr().out == '+ ' + sha + ' bar\n' + '  ' + sha + ' foo\n'
    os.chdir(original_cwd)

def test_status_command_with_path(capsys):
    tmpdir = create_test_git_repository()
    tmpdir2 = create_test_git_repository()
    original_cwd = Path.cwd()
    os.chdir(tmpdir2.name)
    beman_submodule.add_command(tmpdir.name, 'foo')
    beman_submodule.add_command(tmpdir.name, 'bar')
    sha_process = subprocess.run(
        ['git', 'rev-parse', 'HEAD'], capture_output=True, check=True, text=True,
        cwd=tmpdir.name)
    with open(Path(tmpdir2.name) / 'bar' / 'a.txt', 'w') as f:
        f.write('b')
    beman_submodule.status_command(['bar'])
    sha = sha_process.stdout.strip()
    assert capsys.readouterr().out == '+ ' + sha + ' bar\n'
    os.chdir(original_cwd)

def test_check_for_git():
    tmpdir = tempfile.TemporaryDirectory()
    assert not beman_submodule.check_for_git(tmpdir.name)
    fake_git_path = Path(tmpdir.name) / 'git'
    with open(fake_git_path, 'w'):
        pass
    os.chmod(fake_git_path, stat.S_IRWXU)
    assert beman_submodule.check_for_git(tmpdir.name)

def test_parse_args():
    def plain_update():
        args = beman_submodule.parse_args(['update'])
        assert args.command == 'update'
        assert not args.remote
        assert not args.beman_submodule_path
    plain_update()
    def update_remote():
        args = beman_submodule.parse_args(['update', '--remote'])
        assert args.command == 'update'
        assert args.remote
        assert not args.beman_submodule_path
    update_remote()
    def update_path():
        args = beman_submodule.parse_args(['update', 'infra/'])
        assert args.command == 'update'
        assert not args.remote
        assert args.beman_submodule_path == 'infra/'
    update_path()
    def update_path_remote():
        args = beman_submodule.parse_args(['update', '--remote', 'infra/'])
        assert args.command == 'update'
        assert args.remote
        assert args.beman_submodule_path == 'infra/'
    update_path_remote()
    def plain_add():
        args = beman_submodule.parse_args(['add', 'git@github.com:bemanproject/infra.git'])
        assert args.command == 'add'
        assert args.repository == 'git@github.com:bemanproject/infra.git'
        assert not args.path
    plain_add()
    def add_path():
        args = beman_submodule.parse_args(
            ['add', 'git@github.com:bemanproject/infra.git', 'infra/'])
        assert args.command == 'add'
        assert args.repository == 'git@github.com:bemanproject/infra.git'
        assert args.path == 'infra/'
    add_path()
    def plain_status():
        args = beman_submodule.parse_args(['status'])
        assert args.command == 'status'
        assert args.paths == []
    plain_status()
    def status_one_module():
        args = beman_submodule.parse_args(['status', 'infra/'])
        assert args.command == 'status'
        assert args.paths == ['infra/']
    status_one_module()
    def status_multiple_modules():
        args = beman_submodule.parse_args(['status', 'infra/', 'foobar/'])
        assert args.command == 'status'
        assert args.paths == ['infra/', 'foobar/']
    status_multiple_modules()
