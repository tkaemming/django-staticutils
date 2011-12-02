from django.core.management.base import NoArgsCommand
from optparse import make_option


class Command(NoArgsCommand):
    help = "Purges *old* versioned static files from `VERSIONED_STATIC_ROOT`. "\
           "(Files where the version *matches* the source file's current version "\
           "are not removed, unless the `--all` flag is given.)"

    option_list = NoArgsCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Removes *everything* from `VERSIONED_STATIC_ROOT`, not just '\
                 'old versions'),
        make_option('--noinput',
            action='store_true',
            dest='noinput',
            default=False,
            help='Does not prompt for confirmation when deleting.'),
    )

    def handle_noargs(self, **options):
        pass
