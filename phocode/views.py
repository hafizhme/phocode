from PIL import Image
from matplotlib import pyplot
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from os import path


@view_config(route_name='home', renderer='templates/layout.jinja2')
def home(request):
    return {'project': 'phocode'}


@view_config(route_name='upload image', request_method='POST')
def upload_image(request):
    file = request.POST['imagefile']

    filename = request.storage.save(file, randomize=True)
    return HTTPFound(location='/image/' + filename)


@view_config(route_name='decompress', request_method='POST')
def decompress(request):
    from phocode.operator import compression
    from os import path
    import uuid
    resulted_image, error = compression.rle_decompress(request.POST['file'].file)
    filename = str(uuid.uuid4()) + '.png'
    filepath = path.join(
        '.', 'phocode', 'static', '.images',
        filename
    )
    resulted_image.save(filepath)
    return HTTPFound(location='/image/' + filename)


@view_config(route_name='image', renderer='templates/image.jinja2')
def image(request):
    filename = request.matchdict['filename']
    im = Image.open(
        request.storage.path(filename)
    )
    size = im.size
    im.close()

    return {
        'filename': filename,
        'size': size
    }


@view_config(route_name='operate')
def operate(request):
    filename = request.matchdict['filename']
    operation = request.matchdict['operation']

    # from pyramid_storage.local import LocalFileStorage
    if not request.storage.exists(filename):
        return HTTPFound(location='/')

    original_image = Image.open(request.storage.path(filename))

    resulted_image, error = None, None

    from phocode.operator import (
        invert, grayscale,
        zoom_in, zoom_out,
        flip_vertical, flip_horizontal,
        brightness,
        crop,
        convolution,
        rotate,
        histogram,
        noise_reduction,
        segmentation,
        morphology,
        compression
    )

    resulted_filename = operation + '-' + filename
    resulted_filepath = path.join(request.storage.base_path, resulted_filename)

    if operation == 'invert':
        resulted_image, error = invert.invert(original_image)
    elif operation == 'grayscale':
        resulted_image, error = grayscale.do(original_image)
    elif operation == 'zoom_in':
        resulted_image, error = zoom_in.do(original_image)
    elif operation == 'zoom_out':
        resulted_image, error = zoom_out.do(original_image)
    elif operation == 'flip_vertical':
        resulted_image, error = flip_vertical.do(original_image)
    elif operation == 'flip_horizontal':
        resulted_image, error = flip_horizontal.do(original_image)
    elif operation == 'brightness':
        factor = float(request.GET['factor'])
        resulted_image, error = brightness.do(original_image, factor)
    elif operation == 'crop':
        fr = (int(request.GET['frx']), int(request.GET['fry']))
        to = (int(request.GET['tox']), int(request.GET['toy']))
        resulted_image, error = crop.do(original_image, fr, to)
    elif operation == 'convolution':
        if request.GET['kernel'] == 'sharpen':
            resulted_image, error = convolution.sharpen(original_image)
        elif request.GET['kernel'] == 'gaussian_blur_3':
            resulted_image, error = convolution.gaussian_blur_3(original_image)
        elif request.GET['kernel'] == 'edge_detection':
            resulted_image, error = convolution.edge_detection(original_image)
    elif operation == 'rotate':
        degree = int(request.GET['degree'])
        resulted_image, error = rotate.do(original_image, degree)
    elif operation == 'histogram':
        resulted_image, error = histogram.do(original_image)
    elif operation == 'noise_reduction':
        resulted_image, error = noise_reduction.do(
            original_image,
            request.GET['method']
        )
    elif operation == 'srg':
        seed = (int(request.GET['sex']), int(request.GET['sey']))
        threshold = int(request.GET['th'])
        resulted_image, error = segmentation.seed_region_growth(
            original_image,
            seed,
            threshold
        )
    elif operation == 'thr':
        r_range = range(int(request.GET['trl']), int(request.GET['trh']))
        g_range = range(int(request.GET['tgl']), int(request.GET['tgh']))
        b_range = range(int(request.GET['tbl']), int(request.GET['tbh']))
        resulted_image, error = segmentation.threshold(
            im=original_image,
            r_range=r_range,
            g_range=g_range,
            b_range=b_range
        )
    elif operation == 'morphology':
        if request.GET['type'] == 'dilation':
            resulted_image, error = morphology.dilation(original_image)
        elif request.GET['type'] == 'erosion':
            resulted_image, error = morphology.erosion(original_image)
    elif operation == 'compress':
        resulted_image, error = compression.rle_compress(original_image)

    if error is not None:
        # TODO add Exception
        pass

    if request.storage.exists(resulted_filename):
        request.storage.delete(resulted_filename)

    if resulted_image == pyplot:
        resulted_image.savefig(resulted_filepath)
    elif type(resulted_image) == str:
        return HTTPFound(location='/static/.compression/' + resulted_image)
    else:
        resulted_image.save(resulted_filepath)

    return HTTPFound(location='/image/' + resulted_filename)
