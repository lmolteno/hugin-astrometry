from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


class ControlPoint:
    def __init__(self, left: int, right: int, left_point: Point, right_point: Point, alignment='normal'):
        self.left = left
        self.right = right
        self.leftPointX = left_point.x
        self.leftPointY = left_point.y
        self.rightPointX = right_point.x
        self.rightPointY = right_point.y
        self.alignment = 't0' if alignment == 'normal' else alignment

    def __str__(self):
        return f"c n{self.left} N{self.right} x{self.leftPointX} y{self.leftPointY} X{self.rightPointX} Y{self.rightPointY} {self.alignment}"


class HuginProject:
    def __init__(self, filename: str):
        self.fn = filename
        self.file = open(filename, 'r+')
        self._get_imageindices()

    def _get_imageindices(self):
        self.file.seek(0)
        lines = self.file.readlines()
        imagelines = filter(lambda l: l.startswith('i w'), lines)
        self.images = [*map(lambda l: l.split(" ")[-1][2:-2], imagelines)]

    def add_cp(self, control_point: ControlPoint):
        self.add_cps([control_point])

    def add_cps(self, control_points: list[ControlPoint]):
        self.file.seek(0)
        text = self.file.read()
        sp = text.split("# control points\n")
        sp[1] = "# control points\n" + '\n'.join(map(lambda c: c.__str__(), control_points)) + '\n' + sp[1]
        self.file.seek(0)
        self.file.write("".join(sp))
        self.file.truncate()

    def image_index(self, filename: str):
        if type(self.images) is not list:
            raise Exception("You haven't parsed the project file to get the indices yet")

        try:
            return self.images.index(filename)
        except ValueError:
            raise ValueError(f"Image {filename} not found in this project")

    def close(self):
        self.file.close()


if __name__ == "__main__":
    proj = HuginProject('pano2.pto')
    cp = ControlPoint(0, 1, Point(10, 20), Point(20, 30))
    proj.add_cps([cp, cp, cp])
    proj.file.close()
