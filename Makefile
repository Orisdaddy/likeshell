test:
	coverage run --omit="tests/*" -p -m unittest tests/test_alias.py -v
	coverage run --omit="tests/*" -p -m unittest tests/test_basic.py -v
	coverage run --omit="tests/*" -p -m unittest tests/test_ignore.py -v
	coverage run --omit="tests/*" -p -m unittest tests/test_options.py -v
	coverage run --omit="tests/*" -p -m unittest tests/test_params.py -v
	coverage run --omit="tests/*" -p -m unittest tests/test_input.py -v
	coverage run --omit="tests/*" -p -m unittest tests/test_complex.py -v
