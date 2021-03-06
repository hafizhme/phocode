from pyramid.config import Configurator
from os import path

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    pyramid_storage_settings = {
        'storage.base_path': path.join('.', 'phocode', 'static', '.images'),
        'storage.extension': 'images',
    }
    config.add_settings(pyramid_storage_settings)
    config.include('pyramid_storage.local')

    config.add_static_view('static', 'static', cache_max_age=300)
    config.add_route('home', '/')
    config.add_route('upload image', '/upload-image')
    config.add_route('decompress', '/decompress')
    config.add_route('image', '/image/{filename}')
    config.add_route('operate', '/image/{filename}/{operation}')
    config.scan()

    return config.make_wsgi_app()
