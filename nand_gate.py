import pcdl


cfg = dict(
    grid=3.0,
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
    layers = pcdl.load_gif('nand.gif')

    filenames = []
    for index, (layer, layer_cfg) in enumerate(zip(layers, cfg['layers'])):
        filename = f"layer{index}_{layer_cfg['name']}_{layer_cfg['material']}_{layer_cfg['thickness']}.svg"
        with open('build/' + filename, 'wb') as output:
            pcdl.render_layer(layer, output)
        filenames.append(filename)

    with open('build/composite.svg', 'wb') as output:
        #pcdl.render_svg([layers[3]], output)
        pcdl.render_composite(filenames, output)



if __name__ == '__main__':
    main()
