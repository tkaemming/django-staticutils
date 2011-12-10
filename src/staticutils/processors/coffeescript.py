import subprocess
from django.conf import settings

def coffeescript(name, content, arguments=None, binary=None):
    if not name.endswith('.coffee'):
        return content

    if binary is None:
        binary = getattr(settings, 'COFFEESCRIPT_COMPILER_PATH', 'coffee')

    if arguments is None:
        arguments = getattr(settings, 'COFFEESCRIPT_COMPILER_ARGUMENTS', [])

    arguments = list(arguments) + ['-s', '-c'] # Always compile and use stdin/out.

    process = subprocess.Popen(args=arguments, executable=binary, shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = process.communicate(content)

    if not process.wait() == 0:
        raise Exception('Error compiling CoffeeScript!\n%s' % error)

    return out
