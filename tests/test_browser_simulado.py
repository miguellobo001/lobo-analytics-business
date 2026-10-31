"""Entrada de compatibilidade: a simulação antiga foi substituída pelo teste real."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('test_browser.py')),run_name='__main__')
