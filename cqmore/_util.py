from typing import Iterable, cast, Tuple

from cadquery import Vector
from cadquery.cq import VectorLike


def toVectors(points: Iterable[VectorLike]) -> Tuple[Vector]:
    it = iter(points)
    if isinstance(next(it), Vector):
        return cast(Tuple[Vector], list(points))
    
    return cast(Tuple[Vector], tuple(Vector(*p) for p in points))


def toTuples(points: Iterable[VectorLike]) -> Tuple[tuple]:
    it = iter(points)
    if isinstance(next(it), tuple):
        return cast(Tuple[tuple], tuple(points))

    r = tuple(v.toTuple() for v in cast(Tuple[Vector], points))
    return cast(Tuple[tuple], r)
