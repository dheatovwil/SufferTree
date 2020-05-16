import gen
import os


class Series:
    def __init__(self):
        try:
            os.mkdir("out")
        except FileExistsError:
            os.system("rm -rf out")
        self.ctr = 0
        self.higher = {
            "created": []
        }

    def add(self, root):
        attr = [("ratio", "0.57"), ("viewport", "1280,720,1,ROOT")]
        gen.gen_dot(root, self.higher, attr).render(str(self.ctr).zfill(2), directory="out", cleanup=True, format="png")
        self.ctr += 1


def visualize(root):
    gen.gen_dot(root).view()
