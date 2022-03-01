# cqMore 1.0

cqMore aims to add more fundamental API to CadQuery. It's based on CadQuery 2.1 and Python 3.9.

![cqMore](images/superellipsoids.JPG)

## Installation

Please use `conda` to install CadQuery and its dependencies (see [Getting started](https://github.com/CadQuery/cadquery#getting-started) of CadQuery).
* TLDR `conda install -c conda-forge -c cadquery cadquery=2.1`

	
To install cqMore directly from GitHub, run the following `pip` command:
* Install git if you don't already have it `conda install git`
*  ~~pip install git+git://github.com/JustinSDK/cqMore.git~~
* SSH: ```python -m pip install git+ssh://git@github.com/nikolarobottesla/cqmore.git```
* HTTPS: ```python -m pip install https://github.com/nikolarobottesla/cqmore.git```

## Dependencies

This plugin has no dependencies other than the cadquery library. The [examples](examples) list their own dependencies in the first comment, if any.

## Usage

You may simply use `cqmore.Workplane` to replace `cadquery.Workplane`. For example:

    from cqmore import Workplane

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

You may also attach methods of `cqmore.Workplane` to `cadquery.Workplane`, such as:

    from cadquery import Workplane
    import cqmore
    cqmore.extend(Workplane)

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

## API Reference

- [`cqmore.Workplane`](docs/workplane.md)
- [`cqmore.polygon`](docs/polygon.md)
- [`cqmore.polyhedron`](docs/polyhedron.md)
- [`cqmore.curve`](docs/curve.md)
- [`cqmore.matrix`](docs/matrix.md)
