import sys

from djexp.export import export
from djexp.exceptions import DjexpCliError
from djexp import NAME, VERSION, DESCRIPTION


def get_param(args, prefix, name):
	try:
		idx = args.index(prefix)
		return args[idx + 1]
	except ValueError as _:
		raise DjexpCliError('{} parameter is required'.format(name))


def parse_args(argv):
	if len(argv) > 6:
		raise DjexpCliError('too many arguments were specified')
	root = get_param(argv, '-r', 'root directory')
	settings = get_param(argv, '-s', 'settings module')
	try:
		argv.index('--yml')
		file_format = 'yml'
	except ValueError as _:
		try:
			argv.index('--json')
		except ValueError as _:
			if len(argv) > 5:
				print('Warning: unsupported file format, serializing to json by default')
		file_format = 'json'
	return {
		'root_dir': root,
		'file_format': file_format.strip('-'),
		'settings_module': settings,
	}


def print_help():
	print("""Help:
	-h             print help
	-r             specify project root
	-s             specify an explicit name of settings module
	--json, --yml  export file format (default is json)""")


def print_info():
	print('{}, version {}\n{}'.format(NAME, VERSION, DESCRIPTION))


def cli_exec():
	if len(sys.argv) == 1:
		print_info()
		print()
		print_help()
		return
	elif len(sys.argv) == 2:
		try:
			sys.argv.index('-h')
			print_help()
			return
		except ValueError as _:
			pass
	else:
		try:
			print('Exporting...')
			export(**parse_args(sys.argv))
		except DjexpCliError as val_err:
			print('{}: {}, try \'-h\' for help'.format(NAME, val_err))
		return
	print('{}: invalid arguments were specified, try \'-h\' for help'.format(NAME))
