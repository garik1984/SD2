from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, HTML
from urllib.parse import urlparse
from IPython import get_ipython
from pathlib import Path
from tqdm import tqdm
import subprocess, zipfile, sys, os, re, json, shlex
import psutil


@register_line_magic
def say(line):
    args = re.findall(r'\{[^\{\}]+\}|[^\s\{\}]+', line)
    output = []
    theme = get_ipython().config.get('InteractiveShellApp', {}).get('theme', 'light')
    default_color = 'white' if theme == 'dark' else 'black'

    i = 0
    while i < len(args):
        msg = args[i]
        color = None

        if re.match(r'^\{[^\{\}]+\}$', msg.lower()):
            color = msg[1:-1]
            msg = ""
        else:
            while i < len(args) - 1 and not re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                i += 1
                msg += " " + args[i]

        if color == 'd':
            color = default_color
        elif color is None and i < len(args) - 1:
            if re.match(r'^\{[^\{\}]+\}$', args[i + 1].lower()):
                color = args[i + 1][1:-1]
                i += 1

        span_text = f"<span"
        if color:
            span_text += f" style='color:{color};'"
        span_text += f">{msg}</span>"
        output.append(span_text)
        i += 1

    display(HTML(" ".join(output)))


toket = "?token=YOUR_API_KEY"
@register_line_magic
def download(line):
    args = line.split()
    url = args[0]

    if url.endswith('.txt') and Path(url).expanduser().is_file():
        with open(Path(url).expanduser(), 'r') as file:
            for line in file:
                netorare(line)
    else:
        netorare(line)


def strip_(url):
    if any(domain in url for domain in ["civitai.com", "huggingface.co"]):
        if '?' in url:
            url = url.split('?')[0]
    return url


def get_fn(url):
    fn_fn = urlparse(url)
    if any(domain in fn_fn.netloc for domain in ["civitai.com", "drive.google.com"]):
        return None
    else:
        fn = Path(fn_fn.path).name
        return fn


def netorare(line):
    hitozuma = line.strip().split()
    url = hitozuma[0].replace('\\', '')
    chg = any(domain in url for domain in ["civitai.com", "huggingface.co", "github.com"])
    dg = "drive.google.com" in url
    path, fn = "", ""
    url = strip_(url)
    _dir = Path.cwd()

    if 'huggingface.co' in url and '/blob/' in url:
        url = url.replace('/blob/', '/resolve/')

    aria2c = (
        "aria2c --header='User-Agent: Mozilla/5.0' --allow-overwrite=true "
        "--console-log-level=error --stderr=true -c -x16 -s16 -k1M -j5"
    )

    try:
        if len(hitozuma) >= 3:
            path, fn = Path(hitozuma[1]).expanduser(), hitozuma[2]
            path.mkdir(parents=True, exist_ok=True)
            os.chdir(path)
            if chg:
                fc = f"{aria2c} {url}{toket if 'civitai.com' in url else ''} -o {fn}"
                ketsuno_ana(fc, fn)
            elif dg:
                gdrown(url, path, fn)
            else:
                fc = f"curl -#JL {url} -o {fn}"
                ketsuno_ana(fc, fn)
            
        elif len(hitozuma) >= 2:
            if '/' in hitozuma[1] or '~/' in hitozuma[1]:
                path = Path(hitozuma[1]).expanduser()
                path.mkdir(parents=True, exist_ok=True)
                os.chdir(path)
                if chg:
                    fn = get_fn(url)
                    fc = f"{aria2c} {url}{toket if 'civitai.com' in url else ''}"
                    if 'civitai.com' not in url:
                        fc += f" -o {fn}"
                    ketsuno_ana(fc, fn)
                elif dg:
                    gdrown(url, path)
                else:
                    fn = Path(urlparse(url).path).name
                    fc = f"curl -#OJL {url}"
                    ketsuno_ana(fc, fn)
            else:
                fn = hitozuma[1]
                if chg:
                    fc = f"{aria2c} {url}{toket if 'civitai.com' in url else ''} -o {fn}"
                    ketsuno_ana(fc, fn)
                elif dg:
                    gdrown(url, None, fn)
                else:
                    fc = f"curl -#JL {url} -o {fn}"
                    ketsuno_ana(fc, fn)

        else:
            if chg:
                fn = get_fn(url)
                fc = f"{aria2c} {url}{toket if 'civitai.com' in url else ''}"
                if 'civitai.com' not in url:
                    fc += f" -o {fn}"
                ketsuno_ana(fc, fn)
            elif dg:
                gdrown(url)
            else:
                fn = Path(urlparse(url).path).name
                fc = f"curl -#OJL {url}"
                ketsuno_ana(fc, fn)
    finally:
        os.chdir(_dir)


def gdrown(url, path=None, fn=None):
    is_folder = "drive.google.com/drive/folders" in url
    cmd = "gdown --fuzzy " + url

    if path:
        path = str(Path(path).expanduser())
        os.makedirs(path, exist_ok=True)
        cwd = path
        if fn:
            fn = str(Path(path) / fn)
            cmd += " -O " + fn
    else:
        cwd = None

    if fn and not path:
        cmd += " -O " + fn

    if is_folder:
        cmd += " --folder"

    if cwd:
        get_ipython().system(f"cd {cwd} && {cmd}")
    else:
        get_ipython().system(f"{cmd}")


def ariari(fc, fn):
    qqqqq = subprocess.Popen(
        shlex.split(fc),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    result = ""
    br = False

    while True:
        lines = qqqqq.stderr.readline()
        if lines == '' and qqqqq.poll() is not None:
            break
            
        if lines:
            result += lines
            
            for outputs in lines.splitlines():
                if 'errorCode' in outputs:
                    print("  " + lines)
                    
                if re.match(r'\[#\w{6}\s.*\]', outputs):
                    print("\r" + " "*80 + "\r", end="")
                    print(f"  {outputs}", end="", flush=True)
                    br = True
                    break

    if br:
        print()

    stripe = result.find("======+====+===========")
    if stripe != -1:
        for lines in result[stripe:].splitlines():
            if "|" in lines:
                print(f"  {lines}")

    qqqqq.wait()


def curlly(fc, fn):  
    zura = subprocess.Popen(
        shlex.split(fc),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd=str(Path.cwd())
    )

    progress_pattern = re.compile(r'(\d+\.\d+)%')
    oppai = ""

    with tqdm(
        total=100,
        desc=f"{fn.ljust(58):>{58 + 2}}",
        initial=0,
        bar_format="{desc} 【{bar:20}】【{percentage:3.0f}%】",
        ascii="▷▶",
        file=sys.stdout
    ) as pbar:

        for line in iter(zura.stdout.readline, ''):
            if not line.startswith('  % Total') and not line.startswith('  % '):
                match = progress_pattern.search(line)
                if match:
                    progress = float(match.group(1))
                    pbar.update(progress - pbar.n)
                    pbar.refresh()

            oppai += line

        pbar.close()

    zura.wait()

    if zura.returncode != 0:
        if "curl: (23)" in oppai:
            print(
                f"{'':>2}^ File already exists; download skipped. "
                "Append a custom name after the URL or PATH to overwrite."
            )
        elif "curl: (3)" in oppai:
            print("")
        else:
            print(f"{'':>2}^ Error: {oppai}")
    else:
        pass


def ketsuno_ana(fc, fn):
    try:
        if "aria2c" in fc:
            ariari(fc, fn)
        else:
            curlly(fc, fn)

    except KeyboardInterrupt:
        print(f"{'':>2}^ Canceled")

        
@register_line_magic
def clone(line):
    path = Path(line.strip()).expanduser()

    if not path.exists():
        print(f"Error: File not found - {path}")
        return

    with open(path, 'r') as file:
        #print("\n  Cloning Extension:")
        
        for ext in map(str.strip, file):
            cmd = shlex.split(ext)

            url = None
            for repo in cmd:
                if re.match(r'https?://', repo):
                    url = repo
                    break

            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )

            while True:
                output = proc.stdout.readline()

                if not output and proc.poll() is not None:
                    break

                if output:
                    output = output.strip()

                    if output.startswith("Cloning into"):
                        name = output.replace("Cloning into", "")
                        name = output.split("'")[1]
                        print(f"{'':>2}{name} -> {url}")

            proc.wait()


@register_line_magic
def pull(line):
    inputs = line.split()
    if len(inputs) != 3:
        return

    repo, tarfold, despath = inputs

    print(
    f"\n{'':>2}{'pull':<4} : {tarfold}",
    f"\n{'':>2}{'from':<4} : {repo}",
    f"\n{'':>2}{'into':<4} : {despath}\n")

    path = Path(despath).expanduser()
    opts = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE, 'check': True}
    subs = subprocess.run
    cmd1 = f'git clone -n --depth=1 --filter=tree:0 {repo}'
    subs(shlex.split(cmd1), cwd=str(path), **opts)
    repofold = path / Path(repo).name.rstrip('.git')
    cmd2 = f'git sparse-checkout set --no-cone {tarfold}'
    subs(shlex.split(cmd2), cwd=str(repofold), **opts)
    cmd3 = 'git checkout'
    subs(shlex.split(cmd3), cwd=str(repofold), **opts)

    zipin = repofold / 'ui' / tarfold
    zipout = path / f'{tarfold}.zip'
    
    with zipfile.ZipFile(str(zipout), 'w') as zipf:
        for root in zipin.rglob('*'):
            if root.is_file():
                arcname = str(root.relative_to(zipin))
                zipf.write(str(root), arcname=arcname)

    cmd4 = f'unzip -o {str(zipout)}'
    subs(shlex.split(cmd4), cwd=str(path), **opts)
    zipout.unlink()
    cmd5 = f'rm -rf {str(repofold)}'
    subs(shlex.split(cmd5), cwd=str(path), **opts)


@register_line_magic
def tempe(line):
    tmp = [
        "/tmp/ckpt",
        "/tmp/lora",
        "/tmp/controlnet",
        "/tmp/svd",
        "/tmp/z123"
    ]

    for path in tmp:
        Path(path).mkdir(parents=True, exist_ok=True)


@register_line_magic
def delete(line):
    if 'LD_PRELOAD' in os.environ:
        del os.environ['LD_PRELOAD']
        
    del_input = line.strip() if line else '/home/studio-lab-user'
    del_list = [
        '/tmp/*',
        '/tmp',
        '/asd',
        '/forge',
        '/ComfyUI',
        '/.cache/*',
        '/.config/*',
        '/.conda/*',
        '/.local/share/jupyter/runtime/*',
        '/.ipython/profile_default/*']

    del_cmd = [
        f"rm -rf {' '.join([del_input + t for t in del_list])}",
        f"find {del_input} -type d -name '.ipynb_checkpoints' -exec rm -rf {{}} +"
    ]

    for cmd_del in del_cmd:
        subprocess.run(
            shlex.split(cmd_del), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    is_nb = False
    try:
        nb_find = f"find {del_input} -type d -name '.*' -prune -o -type f -name '*.ipynb' -print"
        nb_files = subprocess.check_output(shlex.split(nb_find), text=True).strip().split('\n')
        
        for nb_path in nb_files:
            if nb_path:
                nb_clear(nb_path)
                is_nb = True
                
    except subprocess.CalledProcessError:
        pass

    if is_nb:
        print("Now, Please Restart JupyterLab.")


def nb_clear(nb_path):
    try:
        with open(nb_path, 'r') as f:
            nb_contents = json.load(f)

        nb_contents['metadata'] = {
            "language_info": {
                "name": ""
            },
            "kernelspec": {
                "name": "",
                "display_name": ""
            }
        }
        
        with open(nb_path, 'w') as f:
            json.dump(nb_contents, f, indent=1, sort_keys=True)

    except:
        pass


@register_line_magic
def storage(path):
    get_ipython().system("rm -rf /home/studio-lab-user/.cache/*")

    path = Path(path)

    def size1(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    def size2(size_in_kb):
        if size_in_kb == 0:
            return "0 KB"

        base = 1024
        size_in_bytes = size_in_kb * base
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < base:
                if unit in ['B', 'KB']:
                    return f"{size_in_bytes:.0f} {unit}"
                else:
                    return f"{size_in_bytes:.1f} {unit}"
            size_in_bytes /= base

    usage = psutil.disk_usage(path)
    size_str = size1(usage.total)
    used_str = size1(usage.used)
    free_str = size1(usage.free)

    used_percentage = f"{usage.percent:.1f}%".ljust(6)
    free_percentage = f"{100 - usage.percent:.1f}%".ljust(6)

    print(f"Size = {size_str:>8}")
    print(f"Used = {used_str:>8} | {used_percentage}")
    print(f"Free = {free_str:>8} | {free_percentage}")
    print()

    du_process = subprocess.Popen(['du', '-h', '-k', '--max-depth=1', str(path)], stdout=subprocess.PIPE)
    du_output = du_process.communicate()[0].decode()
    lines = du_output.split('\n')
    paths = [Path(line.split('\t')[1]) for line in lines if line]
    sizes_kb = [int(line.split('\t')[0]) for line in lines if line]

    for path, size_kb in zip(paths, sizes_kb):
        formatted_size = size2(size_kb)
        base_path = path.name

        if base_path != 'studio-lab-user':
            padding = " " * max(0, 9 - len(formatted_size))
            print(f"/{base_path:<25} {padding}{formatted_size}")


@register_cell_magic
def zipping(line, cell):
    lines = cell.strip().split('\n')

    input_path = None
    output_path = None

    for line in lines:
        soup = line.split('=')
        
        if len(soup) == 2:
            arg_name = soup[0].strip()
            arg_value = soup[1].strip().strip("'")

            if arg_name == 'input_folder':
                input_path = arg_value
                
            elif arg_name == 'output_folder':
                output_path = arg_value

    if not os.path.exists(input_path):
        print(f"Error: '{input_path}' does not exist.")
        return

    def zip_folder(
        input_path,
        output_path,
        max_size_mb=20):
        
        os.makedirs(
            output_path,
            exist_ok=True)
        
        all_files = []
        
        for root, dirs, files in os.walk(input_path):
            
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)

        zip_number = 1
        current_zip_size = 0
        current_zip_name = os.path.join(
            output_path,
            f"part_{zip_number}.zip")

        with tqdm(
            total=len(all_files),
            desc='zipping : ',
            bar_format='{desc}[{bar:26}] [{n_fmt}/{total_fmt}]',
            ascii="▷▶",
            file=sys.stdout) as pbar:
            
            with zipfile.ZipFile(
                current_zip_name,
                'w',
                compression=zipfile.ZIP_DEFLATED) as current_zip:
                
                for file_path in all_files:
                    file_size = os.path.getsize(file_path)

                    if current_zip_size + file_size > max_size_mb * 1024 * 1024:
                        current_zip.close()
                        
                        zip_number += 1
                        
                        current_zip_name = os.path.join(
                            output_path,
                            f"part_{zip_number}.zip")
                        
                        current_zip = zipfile.ZipFile(
                            current_zip_name,
                            'w',
                            compression=zipfile.ZIP_DEFLATED)
                        
                        current_zip_size = 0

                    current_zip.write(
                        file_path,
                        os.path.relpath(
                            file_path,
                            input_path))
                    
                    current_zip_size += file_size
                    pbar.update(1)

    max_size_mb = 200
    zip_folder(input_path, output_path, max_size_mb)