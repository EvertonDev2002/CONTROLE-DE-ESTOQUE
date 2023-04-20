from importlib import import_module

from dynaconf import FlaskDynaconf


def load_extensions(app):
    for extension in app.config.EXTENSIONS:
        module_name, factory = extension.split(":")
        extension = import_module(module_name)
        getattr(extension, factory)(app)


def init_app(app):
    FlaskDynaconf(app)
