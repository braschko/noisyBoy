"""
NoisyBoy

Author  : Brian Raschko (braschko.bitbucket.io)
License : GNUAGPL (https://www.gnu.org/licenses/agpl-3.0.en.html)
Location: https://github.com/braschko/noisyBoy
"""

import os
from   maya import cmds

def onMayaDroppedPythonFile(*args):

  result = cmds.confirmDialog(
    title         = 'NoisyBoy Installer',
    message       = 'The NoisyBoy Installer will now create a shelf button under the "Custom" category, is that ok?',
    button        = ['Yes','No'],
    defaultButton = 'Yes',
    cancelButton  = 'No',
    dismissString = ''
  )

  if result == 'Yes':

    cmds.shelfButton(
      parent     = 'Custom',
      annotation = 'Show NoisyBoy',
      style      = 'iconOnly',
      image1     = os.path.join(os.path.dirname(__file__), 'noisyBoy', '_resources_', 'icons', 'emblem_32.png'),
      sourceType = 'python',
      command    = 'from noisyBoy import NoisyBoy\n\n# Show the NoisyBoy interface\nNoisyBoy.show()'
    )

    try: 
      
      os.remove(__file__               )
      os.remove((__file__)[:-2] + 'pyc')

    except: cmds.warning('Cleanp attept failed te remove installer files.')