import pcdl


config = dict(
    grid=2.0,
    channels=[
        dict(
            name='routes',
            radius=0.4,
        ),
        dict(
            name='ports',
            radius=0.5,
        ),
        dict(
            name='mounting',
            radius=0.5,
        ),
    ],
    layers=[
        dict(
            name='base',
            material='acrylic',
            thickness=2.0,
        ),
        dict(
            name='bottom',
            material='acrylic',
            thickness=2.0,
        ),
        dict(
            name='wells',
            material='acrylic',
            thickness=2.0,
        ),
        dict(
            name='membrane',
            material='silicone',
            thickness=2.0,
        ),
        dict(
            name='top',
            material='acrylic',
            thickness=2.0,
        ),
        dict(
            name='cover',
            material='acrylic',
            thickness=2.0,
        ),
    ],
)


def main():
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
