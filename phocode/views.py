from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_storage.exceptions import FileNotAllowed


@view_config(route_name='home', renderer='templates/layout.jinja2')
def home(request):
    return {'project': 'phocode'}


@view_config(route_name='upload image', request_method='POST')
def upload_image(request):
    filename = request.storage.save(request.POST['imagefile'])
    return HTTPFound(location='/image/'+filename)


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

    from phocode.operator import invert
    if operation == 'invert':
        resulted_image, error = invert.invert(original_image)

    if error is not None:
        # TODO add Exception
        pass

    resulted_filename = operation + '-' + filename
    if request.storage.exists(resulted_filename):
        request.storage.delete(resulted_filename)

    resulted_image.save(request.storage.base_path + '/' + resulted_filename)

    return HTTPFound(location='/image/' + resulted_filename)
