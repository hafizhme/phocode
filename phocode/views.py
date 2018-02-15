from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_storage.exceptions import FileNotAllowed


@view_config(route_name='home', renderer='templates/layout.jinja2')
def home(request):
    return {'project': 'phocode'}


@view_config(route_name='upload image', request_method='POST')
def upload_image(request):
    file = request.POST['imagefile']

    filename = request.storage.save(file, randomize=True)
    return HTTPFound(location='/image/' + filename)


@view_config(route_name='image', renderer='templates/image.jinja2')
def image(request):
    return {
        'filename': request.matchdict['filename'],
    }


@view_config(route_name='operate')
def operate(request):
    filename = request.matchdict['filename']
    operation = request.matchdict['operation']

    # from pyramid_storage.local import LocalFileStorage
    if not request.storage.exists(filename):
        return HTTPFound(location='/')

    from PIL import Image
    original_image = Image.open(request.storage.path(filename))

    resulted_image, error = None, None

    from phocode.operator import (
        invert, grayscale,
        zoom_in, zoom_out,
        flip_vertical, flip_horizontal
    )

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

    if error is not None:
        # TODO add Exception
        pass

    resulted_filename = operation + '-' + filename
    if request.storage.exists(resulted_filename):
        request.storage.delete(resulted_filename)

    resulted_image.save(request.storage.base_path + '/' + resulted_filename)

    return HTTPFound(location='/image/' + resulted_filename)
