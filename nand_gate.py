import pcdl


filenames = [
    'layer0_base_acrylic.svg',
    'layer1_bottom_acrylic.svg',
    'layer2_wells_acrylic.svg',
    'layer3_membrane_silicone.svg',
    'layer4_top_acrylic.svg',
    'layer5_cover_acrylic.svg',
]


def main():
    layers = pcdl.load_gif('nand.gif')

    for layer, filename in zip(layers, filenames):
        with open('build/' + filename, 'wb') as output:
            pcdl.render_layer(layer, output)
        filenames.append(filename)

    with open('build/composite.svg', 'wb') as output:
        #pcdl.render_svg([layers[3]], output)
        pcdl.render_composite(filenames, output)



if __name__ == '__main__':
    main()
