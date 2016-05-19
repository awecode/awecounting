from django.conf import settings
from django.core.servers import basehttp
from django.core.management.commands.runserver import Command as BaseCommand


class QuietWSGIRequestHandler(basehttp.WSGIRequestHandler):
    def log_message(self, format, *args):
        # Don't bother logging requests for paths under MEDIA_URL.
        # if self.path.startswith(settings.MEDIA_URL):
        #     return
        # can't use super as base is old-style class, so call method explicitly
        return basehttp.WSGIRequestHandler.log_message(self, format, *args)


def run(addr, port, wsgi_handler):
    server_address = (addr, port)
    httpd = basehttp.WSGIServer(server_address, QuietWSGIRequestHandler)
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()


class Command(BaseCommand):
    def handle(self, addrport='', *args, **options):
        # monkeypatch Django to use our quiet server
        basehttp.run = run
        return super(Command, self).handle(addrport, *args, **options)
