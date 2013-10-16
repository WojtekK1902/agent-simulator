#http://docs.python.org/library/profile.html
#run: python -m cPython -o profile main.py
import pstats
p = pstats.Stats('profile')
p.sort_stats('cumulative').print_stats()
#p.sort_stats('time').print_stats()