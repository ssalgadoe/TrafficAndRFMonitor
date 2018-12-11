#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Attribution: Hijacked from tracservice.py by Florent Xicluna <laxyf@yahoo.fr>
# http://trac-hacks.org/wiki/WindowsServiceScript
#
# To use this class, users must do the following:
# 1. Download and install the PyWin32all package
#    (http://starship.python.net/crew/mhammond/win32/)
# 2. Edit the constants section with the proper information.
# 3. Open a command prompt with administrator rights and navigate to the directory
#    where this file is located.  Use one of the following commands to
#    install/start/stop/remove the service:
#    > django_service.py install
#    > django_service.py start
#    > django_service.py stop
#    > django_service.py remove
#    Additionally, typing "django_service.py" will present the user with all of the
#    available options.
#
# Once installed, the service will be accessible through the Services
# management console just like any other Windows Service.  All service 
# startup exceptions encountered by the DjangoWindowsService class will be 
# viewable in the Windows event viewer (this is useful for debugging
# service startup errors); all application specific output or exceptions that
# are not captured by the standard Django logging mechanism should 
# appear in the stdout/stderr logs.
#

import sys
import os
from distutils import sysconfig

import win32serviceutil
import win32service

# ==  Editable CONSTANTS SECTION  ============================================

#DJANGO_PROJECT = '%HOME%\\Docum\\django_projects\\myProject'
DJANGO_PROJECT = 'c:\\www\\monitor'

OPTS = {
    'hostname': '192.168.100.191',
    'port': '8081',
}

# ==  End of CONSTANTS SECTION  ==============================================

# Other constants
PYTHONDIR = sysconfig.get_python_lib()  # gets site-packages folder
PYTHONSERVICE_EXE=os.path.join(PYTHONDIR, 'win32', 'pythonservice.exe')
LOG_DIR = os.path.join(DJANGO_PROJECT, 'log')
SETTINGS = os.path.basename(DJANGO_PROJECT) + '.' + 'settings'

# Django Project
ARGS = [os.path.join(DJANGO_PROJECT, 'manage.py'),
        'runserver',
        '--pythonpath=' + DJANGO_PROJECT,
        '--noreload',
        OPTS['hostname'] + ':' + OPTS['port']]

class DjangoWindowsService(win32serviceutil.ServiceFramework):
    """Django Windows Service helper class.

    The DjangoWindowsService class contains all the functionality required
    for running Django application as a Windows Service.

    For information on installing the application, please refer to the
    documentation at the end of this module or navigate to the directory
    where this module is located and type "django_service.py" from the command
    prompt.
    """

    _svc_name_ = 'Django_%s' % str(hash(DJANGO_PROJECT))
    _svc_display_name_ = 'Django project at %s' % DJANGO_PROJECT
    _exe_name_ = PYTHONSERVICE_EXE

    def SvcDoRun(self):
        """ Called when the Windows Service runs. """

        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.httpd = self.django_init()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        try:
            self.httpd.serve_forever()
        except OSError:
            sys.exit(1)

    def SvcStop(self):
        """Called when Windows receives a service stop request."""

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.httpd:
            self.httpd.server_close()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def django_init(self):
        """ Checks for the required data and initializes the application. """

        # manage.py
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS)

        # django.core.management.execute_from_command_line(argv=ARGS)
        """
        A simple method that runs a ManagementUtility.
        """
        from django.core.management import ManagementUtility
        utility = ManagementUtility(ARGS)

        # utility.execute()
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """
        from django.core.management import LaxOptionParser
        # For backwards compatibility: get_version() used to be in this module.
        from django import get_version
        from django.core.management.base import BaseCommand, handle_default_options
        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = LaxOptionParser(usage="%prog subcommand [options] [args]",
                                 version=get_version(),
                                 option_list=BaseCommand.option_list)
        utility.autocomplete()
        try:
            options, args = parser.parse_args(utility.argv)
            handle_default_options(options)
        except:
            pass # Ignore any option errors at this point.
        subcommand = utility.argv[1]
        klass = utility.fetch_command(subcommand)
        
        # klass.run_from_argv(utility.argv)        
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        from django.core.management.base import CommandError
        parser = klass.create_parser(utility.argv[0], utility.argv[1])
        options, args = parser.parse_args(utility.argv[2:])
        handle_default_options(options)

        options = options.__dict__
        # klass.execute(*args, **options.__dict__)
        """
        Try to execute this command, performing model validation if
        needed (as controlled by the attribute
        ``klass.requires_model_validation``, except if force-skipped).
        """
        from django.core.management.base import OutputWrapper
        klass.stdout = OutputWrapper(options.get('stdout', sys.stdout))
        klass.stderr = OutputWrapper(options.get('stderr', sys.stderr), klass.style.ERROR)

        #klass.can_import_settings = True
        from django.conf import settings

        saved_locale = None
        #klass.leave_locale_alone = False
        # Only mess with locales if we can assume we have a working
        # settings file, because django.utils.translation requires settings
        # (The final saying about whether the i18n machinery is active will be
        # found in the value of the USE_I18N setting)

        #klass.can_import_settings = True

        # Switch to US English, because django-admin.py creates database
        # content like permissions, and those shouldn't contain any
        # translations.
        from django.utils import translation
        saved_locale = translation.get_language()
        translation.activate('en-us')

        try:
            # Validation is called explicitly each time the server is reloaded.
            #klass.requires_model_validation = False

            addrport = args[0]
            print 'addrport %s' % addrport
            args = args[1:]
            # klass.handle(addrport='', *args, **options)
            import re
            from django.core.management.commands.runserver import naiveip_re, DEFAULT_PORT
            from django.conf import settings

            if not settings.DEBUG and not settings.ALLOWED_HOSTS:
                raise CommandError('You must set settings.ALLOWED_HOSTS if DEBUG is False.')

            klass.use_ipv6 = options.get('use_ipv6')
            if klass.use_ipv6 and not socket.has_ipv6:
                raise CommandError('Your Python does not support IPv6.')
            if args:
                raise CommandError('Usage is runserver %s' % klass.args)
            klass._raw_ipv6 = False
            if not addrport:
                klass.addr = ''
                klass.port = DEFAULT_PORT
            else:
                m = re.match(naiveip_re, addrport)
                if m is None:
                    raise CommandError('"%s" is not a valid port number '
                                       'or address:port pair.' % addrport)
                klass.addr, _ipv4, _ipv6, _fqdn, klass.port = m.groups()
                if not klass.port.isdigit():
                    raise CommandError("%r is not a valid port number." % klass.port)
                if klass.addr:
                    if _ipv6:
                        klass.addr = klass.addr[1:-1]
                        klass.use_ipv6 = True
                        klass._raw_ipv6 = True
                    elif klass.use_ipv6 and not _fqdn:
                        raise CommandError('"%s" is not a valid IPv6 address.' % klass.addr)
            if not klass.addr:
                klass.addr = '::1' if klass.use_ipv6 else '127.0.0.1'
                klass._raw_ipv6 = bool(klass.use_ipv6)

            # klass.run(*args, **options)
            """
            Runs the server, using the autoreloader if needed
            """
            #from django.utils import autoreload
            use_reloader = options.get('use_reloader')
            if use_reloader:
                # use queue and threading to start httpd
                # skip for now
                print 'reloader bypassed for Windows service'
                pass

            # klass.inner_run(*args, **options)
            import errno
            import socket
            from django.utils import six
            from django.utils.six.moves import socketserver
            from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler
            from datetime import datetime
            from django.conf import settings
            from django.utils import translation
            
            threading = options.get('use_threading')
            shutdown_message = options.get('shutdown_message', '')
            quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

            klass.stdout.write("Validating models...\n\n")
            klass.validate(display_num_errors=True)
            klass.stdout.write((
                "%(started_at)s\n"
                "Django version %(version)s, using settings %(settings)r\n"
                "Starting development server at http://%(addr)s:%(port)s/\n"
                "Quit the server with %(quit_command)s.\n"
            ) % {
                "started_at": datetime.now().strftime('%B %d, %Y - %X'),
                "version": klass.get_version(),
                "settings": settings.SETTINGS_MODULE,
                "addr": '[%s]' % klass.addr if klass._raw_ipv6 else klass.addr,
                "port": klass.port,
                "quit_command": quit_command,
            })
            # django.core.management.base forces the locale to en-us. We should
            # set it up correctly for the first request (particularly important
            # in the "--noreload" case).
            translation.activate(settings.LANGUAGE_CODE)

            try:
                handler = klass.get_handler(*args, **options)
                # run(addr=klass.addr, port=int(klass.port), wsgi_handler=handler,
                #     ipv6=klass.use_ipv6, threading=threading)
                server_address = (klass.addr, int(klass.port))
                if threading:
                    httpd_cls = type(str('WSGIServer'), (socketserver.ThreadingMixIn, WSGIServer), {})
                else:
                    httpd_cls = WSGIServer
                httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=klass.use_ipv6)
                httpd.set_app(handler)
                
            except socket.error as e:
                # Use helpful error messages instead of ugly tracebacks.
                ERRORS = {
                    errno.EACCES: "You don't have permission to access that port.",
                    errno.EADDRINUSE: "That port is already in use.",
                    errno.EADDRNOTAVAIL: "That IP address can't be assigned-to.",
                }
                try:
                    error_text = ERRORS[e.errno]
                except KeyError:
                    error_text = str(e)
                klass.stderr.write("Error: %s" % error_text)
                # Need to use an OS exit because sys.exit doesn't work in a thread
                os._exit(1)

        finally:
            if saved_locale is not None:
                translation.activate(saved_locale)
        return httpd


if __name__ == '__main__':
    # The following are the most common command-line arguments that are used
    # with this module:
    #  django_service.py install (Installs the service with manual startup)
    #  django_service.py --startup auto install (Installs the service with auto startup)    
    #  django_service.py start (Starts the service)
    #  django_service.py stop (Stops the service)
    #  django_service.py remove (Removes the service)
    #
    # For a full list of arguments, simply type "django_service.py".
    win32serviceutil.HandleCommandLine(DjangoWindowsService)
