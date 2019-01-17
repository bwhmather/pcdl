import toml

import pcdl


def main():
    config = toml.load('config.toml')

    layers = pcdl.load_gif('nand.gif', config=config)

    filenames = []
    for index, layer in enumerate(layers):
        filename = f"layer{index}_{layer.name}_{layer.material}_{layer.thickness}mm.svg"
        with open('build/' + filename, 'wb') as output:
            pcdl.render_layer(layer, output)
        filenames.append(filename)

    with open('build/composite.svg', 'wb') as output:
        pcdl.render_composite(
            filenames, output,
            width=layers[0].width, height=layers[0].height,
            grid=layers[0].grid,
        )



if __name__ == '__main__':
    main()
