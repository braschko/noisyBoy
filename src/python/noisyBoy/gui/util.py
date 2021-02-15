"""
NoisyBoy

Author  : Brian Raschko (braschko.bitbucket.io)
License : GNUAGPL (https://www.gnu.org/licenses/agpl-3.0.en.html)
Location: https://github.com/braschko/noisyBoy
"""

import os

from PySide2.QtGui import QIcon

def getIcon(resource):
  """
  Return the desired icon resource given its file name.

  Parameters:
    - image str: Target file name

  Returns:
    QImage: The desired icon resource
  """

  # Send back the desired icon resource: No checks are done to ensure this resource exists
  return QIcon( os.path.join( os.path.dirname(__file__), '..', '_resources_', 'icons', resource) )