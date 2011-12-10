import subprocess
from django.conf import settings

def uglifyjs(name, content, arguments=None, binary=None):
    if not name.endswith('.js'):
        return content

    if binary is None:
        binary = getattr(settings, 'UGLIFYJS_PATH', 'uglifyjs')

    if arguments is None:
        arguments = getattr(settings, 'UGLIFYJS_ARGUMENTS', [])

    process = subprocess.Popen(binary, shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = process.communicate(content)

    if not process.wait() == 0:
        raise Exception('Error running UglifyJS!\n%s' % error)

    return out
