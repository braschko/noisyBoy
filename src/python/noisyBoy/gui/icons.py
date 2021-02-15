"""
NoisyBoy

Author  : Brian Raschko (braschko.bitbucket.io)
License : GNUAGPL (https://www.gnu.org/licenses/agpl-3.0.en.html)
Location: https://github.com/braschko/noisyBoy
"""

import os

from .util import getIcon

class Icons():
  """
  Singleton class providing QIcon instances associated with images under oneUp/_resources_/icons.
  """

  EMBLEM_32 = getIcon('emblem_32.png')
  EMBLEM_16 = getIcon('emblem_16.png')