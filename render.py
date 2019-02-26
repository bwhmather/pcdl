import argparse
import pathlib

import toml

import pcdl


def main():
    parser = argparse.ArgumentParser(
        description="render a gif describing a pneumatic circuit to svg"
    )
    parser.add_argument(
        '--config', type=argparse.FileType('r'),
    )
    parser.add_argument(
        'description', type=argparse.FileType('rb'),
    )
    parser.add_argument(
        'output', type=pathlib.Path
    )
    args = parser.parse_args()

    config = toml.load(args.config)

    layers = pcdl.load_gif(args.description, config=config)

    args.output.mkdir(parents=True, exist_ok=True)

    filenames = []
    for index, layer in enumerate(layers):
        filename = f"layer{index}_{layer.name}_{layer.material}_{layer.thickness}mm.svg"
        with open(args.output.joinpath(filename), 'wb') as output:
            pcdl.render_layer(layer, output)
        filenames.append(filename)

    with open(args.output.joinpath('composite.svg'), 'wb') as output:
        pcdl.render_composite(
            filenames, output,
            width=layers[0].width, height=layers[0].height,
            grid=layers[0].grid,
        )


if __name__ == '__main__':
    main()
