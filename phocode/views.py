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
