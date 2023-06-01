import subprocess


class Dock:
    def __init__(self, vina_exe, receptor_file, ligand_file, config_filename):
        self.vina_exe = vina_exe
        self.receptor_file = receptor_file
        self.ligand_file = ligand_file
        self.config_filename = config_filename

    def config_file_generation(self,
                               center_x,
                               center_y,
                               center_z,
                               size_x,
                               size_y,
                               size_z):
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

        with open(self.config_filename, 'w') as out:
            out.write(content)

    def do_dock(self, out_filename):
        cmd = "{0} --ligand {1} --receptor {2} --config {3} --out {4}".format(self.vina_exe,self.ligand_file, self.receptor_file, self.config_filename, out_filename)
        cmd_return = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output: str = cmd_return.stdout.decode('utf-8')

        return output


def main():
    dock = Dock("vina.exe", "ligand.pdbqt", "receptor.pdbqt", "test_config.txt")
    dock.config_file_generation(5, 5, 5, 20, 20, 20)
    dock.do_dock("out.pdbqt")


main()
