from pyramid.view import view_config
from pyramid_storage.exceptions import FileNotAllowed


@view_config(route_name='home', renderer='templates/layout.jinja2')
def home(request):
    return {'project': 'phocode'}


@view_config(route_name='upload image', renderer='templates/image_uploaded.jinja2')
def upload_image(request):
    try:
        imagename = request.storage.save(request.POST['imagefile'])
    except FileNotAllowed:
        request.session.flash('Sorry, this file is not allowed')
    return {'imagename': imagename}
