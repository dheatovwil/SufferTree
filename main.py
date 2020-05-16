import gen
import os


class Series:
    def __init__(self):
        try:
            os.mkdir("out")
        except FileExistsError:
            os.system("rm -rf out")
        self.ctr = 0

    def add(self, root):
        gen.gen_dot(root).render(str(self.ctr).zfill(2), directory="out", cleanup=True, format="png")
        self.ctr += 1


def visualize(root):
    gen.gen_dot(root).view()
