import os
import subprocess
from statistics import mean
import urllib.request


def fetch_pdb(pdb_id):
    url_string = "http://files.rcsb.org/download/{0}.pdb".format(pdb_id)
    outfilename = pdb_id + ".pdb"
    try:
        urllib.request.urlretrieve(url_string, outfilename)
    except Exception as e:
        print(e)


def remove_water(pdbfile):
    base_name = pdbfile.split('.')[0]
    out_name = base_name + "_clean.pdb"
    clean_list = []
    with open(pdbfile, 'r') as inf:
        for line in inf:
            if "HOH" in line:
                pass
            else:
                clean_list.append(line)

    with open(out_name, 'w') as out:
        for line in clean_list:
            out.write(line)


def protein_preparation(pdbfile: str, outpdbqtfile: str):
    python_exe = r"C:\Users\shien\miniconda3\python.exe"
    protein_prep = os.path.join(
        r"C:\Users\shien\miniconda3\Lib\site-packages\AutoDockTools_py3-1.5.7.post1-py3.9.egg\AutoDockTools\Utilities24",
        'prepare_receptor4.py')

    # cmd list format raises errors, therefore one string
    cmd = f' "{python_exe}" "{protein_prep}" -r "{pdbfile}" -A bonds_hydrogens -e -o "{outpdbqtfile}" '
    cmd_return = subprocess.run(cmd, capture_output=False, shell=True)
    # output = cmd_return.stdout.decode('utf-8')
    # print(cmd)

    if cmd_return.returncode != 0:
        raise ValueError('Protein prep  failed')

    return True


def box_center_info(fname, extend):
    X = []
    Y = []
    Z = []
    with open(fname) as inf:
        for line in inf:
            if line.startswith('HETATM'):
                clean = line.strip()
                # print(clean.split())
                X.append(float(clean.split()[6]))
                Y.append(float(clean.split()[7]))
                Z.append(float(clean.split()[8]))
    x = mean(X)
    y = mean(Y)
    z = mean(Z)

    x_max = max(X) + extend
    x_min = min(X) - extend
    y_max = max(Y) + extend
    y_min = min(Y) - extend
    z_max = max(Z) + extend
    z_min = min(Z) - extend

    size_x = x_max - x_min
    size_y = y_max - y_min
    size_z = z_max - z_min

    return x, y, z, size_x, size_y, size_z


def config_gen(config_filename, complex_filename):
    center_x, center_y, center_z, size_x, size_y, size_z = box_center_info(complex_filename, 5)
    content = """center_x = {0}
center_y = {1}
center_z = {2}
size_x = {3}
size_y = {4}
size_z = {5}
seed = 303030
cpu = 1
num_modes = 10
energy_range = 2
exhaustiveness = 48
verbosity = 0
    """.format(center_x, center_y, center_z, size_x, size_y, size_z)
    print(content)

    with open(config_filename, 'w') as out:
        out.write(content)
    return 0


def main(pdbid):
    clean_name = pdbid + "_clean.pdb"
    config_filename = pdbid + "_config.txt"
    fetch_pdb(pdbid)
    remove_water(pdbid + ".pdb")
    config_gen(config_filename, clean_name)


main("3OG7")
