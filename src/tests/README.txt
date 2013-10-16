How to launch tests?
(without ValueError: Attempted relative import in non-package does not occur)

1. The first way is to ensure that the parent directory of our package is in sys.path.
2. The second, imho cleaner way is to call scripts from the proper position in 
directory hierarchy:

python -m module-name
	Searches sys.path for the named module and runs the corresponding .py file as a script.

So:
In src call e.g.:
python -mtests.AgentTest

Further notes:
http://stackoverflow.com/questions/3616952/how-to-properly-use-relative-or-absolute-imports-in-python-modules
http://stackoverflow.com/questions/1112618/import-python-package-from-local-directory-into-interpreter
http://stackoverflow.com/questions/463643/python-doing-absolute-imports-from-a-subfolder
http://schettino72.wordpress.com/2008/01/19/11/