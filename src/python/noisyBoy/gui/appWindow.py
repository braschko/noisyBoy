"""
NoisyBoy

Author  : Brian Raschko (braschko.bitbucket.io)
License : GNUAGPL (https://www.gnu.org/licenses/agpl-3.0.en.html)
Location: https://github.com/braschko/noisyBoy
"""

from maya import cmds

from PySide2.QtWidgets import QSizePolicy, QWidget, QSpinBox, QDoubleSpinBox, QLabel, QPushButton, QGroupBox, QLayout, QGridLayout
from PySide2.QtCore    import Qt

from . import Icons

class AppWindow(QWidget):
  """
  Application window for NoiseBoy to allow for noise application setup and processing.
  """

  def __init__(self, parent = None):
    """
    Create a new Application Window instance

    Parameters:
      - parent QWidget: Controlling parent reference
    """
    QWidget.__init__(self, parent, f = Qt.Dialog)

    # Apply window options:
    self.setMinimumWidth(300            )
    self.setWindowIcon  (Icons.EMBLEM_16)
    self.setWindowTitle ('NoisyBoy'     )

    # Value variance input
    self.__varianceInput = QDoubleSpinBox()

    # Frame range input elements:
    self.__startFrameInput = QSpinBox()
    self.__endFrameInput   = QSpinBox()
    self.__frameStepInput  = QSpinBox()

    # Trigger buttons for processing:
    self.__refreshButton  = QPushButton('Refresh'         )
    self.__addNoiseButton = QPushButton('Make Some Noise!')

    # Perform post init interface configuration
    self.__doInterface()

  def __doInterface(self):
    """
    Configure, arrange, and connect interface components required for this window to function.
    """

    # The allowable input values need to be modified:
    self.__varianceInput.setRange  (    0.0, 999999.0)
    self.__startFrameInput.setRange(-999999, 999999  )
    self.__endFrameInput.setRange  (-999999, 999999  )
    self.__frameStepInput.setRange (      1, 999999  )

    # The initial variance value should be .5 units (for a small bit of wobble)
    self.__varianceInput.setValue(.5)

    # Allow input expansion so category labels remain static:
    self.__varianceInput.setSizePolicy  (QSizePolicy.Expanding, QSizePolicy.Preferred)
    self.__startFrameInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    self.__endFrameInput.setSizePolicy  (QSizePolicy.Expanding, QSizePolicy.Preferred)
    self.__frameStepInput.setSizePolicy (QSizePolicy.Expanding, QSizePolicy.Preferred)

    # Allow the refresh button to expand in height
    self.__refreshButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    # Register click for the refresh button to perform frange range update
    self.__refreshButton.clicked.connect(self.__refresh)

    # Primary layout for root interface elements
    rootLayout = QGridLayout(self)

    # Fix the root layout si this window may not be resized
    rootLayout.setSizeConstraint(QLayout.SetFixedSize)

    # Sub widget and layout to contain Frame Options:
    rangeControlFrame = QGroupBox  ('Frame Options:' )
    rangeLayout       = QGridLayout(rangeControlFrame) 

    # Fix the minimum width of the range group box to 300px for esthetics so things don't look so "square"
    rangeControlFrame.setMinimumWidth(300)

    # Label counterparts to input fields:
    varianceLabel   = QLabel('Variance:'   )
    startFrameLabel = QLabel('Start Frame:')
    endFrameLabel   = QLabel('End Frame:'  )
    frameStepLabel  = QLabel('Frame Step:' )

    # Arrange frame range elements within the group layout:
    rangeLayout.addWidget(startFrameLabel       , 0, 0, 1, 1, Qt.AlignRight)
    rangeLayout.addWidget(self.__startFrameInput, 0, 1, 1, 1               )
    rangeLayout.addWidget(endFrameLabel         , 1, 0, 1, 1, Qt.AlignRight)
    rangeLayout.addWidget(self.__endFrameInput  , 1, 1, 1, 1               )
    rangeLayout.addWidget(self.__refreshButton  , 0, 2, 2, 1               )
    rangeLayout.addWidget(frameStepLabel        , 3, 0, 1, 1, Qt.AlignRight)
    rangeLayout.addWidget(self.__frameStepInput , 3, 1, 1, 2               )

    # Arrange root level elements:
    rootLayout.addWidget(varianceLabel        , 0, 0, 1, 1)
    rootLayout.addWidget(self.__varianceInput , 0, 1, 1, 1)
    rootLayout.addWidget(rangeControlFrame    , 1, 0, 1, 2)
    rootLayout.addWidget(self.__addNoiseButton, 2, 0, 1, 2)

  def __onNoiseButtonClicked(self, func):
    """
    EVENT HANDLER: When the user clicks on the "Make Sone Noise!" button to add channel noise

    Paramters:
      - func callable: Function to process channel noise
    """

    # Disable interface before processing
    self.__setInterfaceEnabled(False)

    # Perform noise bake:
    func(
      self.__startFrameInput.value(),
      self.__endFrameInput.value(),
      self.__frameStepInput.value(),
      self.__varianceInput.value()
    )

    # Processing complete, enable interface
    self.__setInterfaceEnabled(True)

  def __refresh(self):
    """
    Refresh the Start and End frame ranges based on current Time Slider values
    """

    # Grab the visible start and end time slider values and apply respectively:
    self.__startFrameInput.setValue( cmds.playbackOptions(query = True, min = True) )
    self.__endFrameInput.setValue  ( cmds.playbackOptions(query = True, max = True) )

  def __setInterfaceEnabled(self, isEnabled):
    """
    Enable or disable all interface buttons and inputs 

    Parameters:
      - isEnabled bool: If interface components are enabled
    """
    
    # Toggle input availability:
    self.__varianceInput.setEnabled  (isEnabled)
    self.__startFrameInput.setEnabled(isEnabled)
    self.__endFrameInput.setEnabled  (isEnabled)
    self.__frameStepInput.setEnabled (isEnabled)

    # Toggle trigger button availability:
    self.__refreshButton.setEnabled (isEnabled)
    self.__addNoiseButton.setEnabled(isEnabled)

  def registerActions(self, addNoise):
    """
    Register internal button actions with function handlers responsible for said actions.

    Parameters:
      - addNoise callable: Functions to add noise to the selected channels: returns bool
    """
    
    self.__addNoiseButton.clicked.connect(lambda: self.__onNoiseButtonClicked(addNoise))

  #Override
  def show(self):
    """
    Refresh internal control values and show this application window
    """

    # Refresh the frame range input values to match current time slider values
    self.__refresh()

    # Show this window
    QWidget.show(self)