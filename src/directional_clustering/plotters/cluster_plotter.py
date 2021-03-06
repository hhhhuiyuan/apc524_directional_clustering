from directional_clustering.geometry import contour_polygons
from directional_clustering.geometry import line_tuple_to_dict
from directional_clustering.geometry import vector_lines_on_faces
from directional_clustering.geometry import line_sdl

from compas_plotters import MeshPlotter


__all__ = [
    "ClusterPlotter"
]

class ClusterPlotter(MeshPlotter):
    def __init__(self, *args, **kwargs):
        super(ClusterPlotter, self).__init__(*args, **kwargs)
        self.name = "Cluster Plotter"
    
    def draw_clusters_contours(self, centers, labels, density, method):
        mesh = self.mesh
        polygons = contour_polygons(mesh, centers, labels, density, method)
        self.draw_polylines(polygons)

    def draw_vector_field(self, tag, color, uniform, scale, width=0.5):
        mesh = self.mesh
        lines = []

        _lines = vector_lines_on_faces(mesh, tag, uniform, scale)
        _lines = [line for line in map(line_tuple_to_dict, _lines)]

        for line in _lines:
            line["width"] = width
            line["color"] = color

        lines.extend(_lines)

        self.draw_lines(lines)

    def draw_vector_field_array(self, field, color, uniform, scale, width=0.5):
        mesh = self.mesh
        lines = []

    
        _lines = []

        rows, cols = field.shape
        for fkey in range(rows):
            vector = field[fkey]
            vector = vector.tolist()

            if uniform:
                vec_length = scale
            else:
                vec_length = length_vector(vector) * scale

            pt = mesh.face_centroid(fkey)
            _lines.append(line_sdl(pt, vector, vec_length))

        _lines = [line for line in map(line_tuple_to_dict, _lines)]

        for line in _lines:
            line["width"] = width
            line["color"] = color

        lines.extend(_lines)

        self.draw_lines(lines)