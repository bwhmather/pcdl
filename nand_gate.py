import pcdl


def main():
    layers = pcdl.load_gif('nand.gif')
    filenames = []

    for index, layer in enumerate(layers):
        filename = f'layer{index}.svg'
        with open('build/' + filename, 'wb') as output:
            pcdl.render_layer(layer, output)
        filenames.append(filename)

    with open('build/composite.svg', 'wb') as output:
        #pcdl.render_svg([layers[3]], output)
        pcdl.render_composite(filenames, output)



if __name__ == '__main__':
    main()
