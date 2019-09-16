
""""
  D0 = GPIO16;
  D1 = GPIO5;
  D2 = GPIO4;
  D3 = GPIO0;
  D4 = GPIO2;
  D5 = GPIO14;
  D6 = GPIO12;
  D7 = GPIO13;
  D8 = GPIO15;
  D9 = GPIO3;
  D10 = GPIO1;
  LED_BUILTIN = GPIO16
"""
from connectivity import Connectivity


sv = Connectivity()

if not sv.backup():
  sv.server()
  sv.update()
sv.wifi()

gc.collect()
