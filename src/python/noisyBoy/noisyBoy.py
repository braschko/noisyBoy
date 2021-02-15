"""
NoisyBoy

Author  : Brian Raschko (braschko.bitbucket.io)
License : GNUAGPL (https://www.gnu.org/licenses/agpl-3.0.en.html)
Location: https://github.com/braschko/noisyBoy
"""

from random import uniform as rand

from maya import cmds
from maya import OpenMayaUI as omui 

from PySide2.QtWidgets import QWidget
from shiboken2         import wrapInstance

from .gui import AppWindow

class NoisyBoy():
  """
  Utility to add random noise to selected channels.
  """

  # Primary application window reference
  __window = None

  @staticmethod
  def __clampValue(minValue, maxValue, value):
    """
    Clamp the given value so it remains within an applicable range set.

    Parameters:
      - minValue float: Minimum clamp value
      - maxValue float: Maximum clamp value
      - value    float: Value to check against

    Returns:
      float: New value clamped appropriately
    """

    # Perform minimum and maximum clamp if required:
    if minValue != None: value = min(minValue, value)
    if maxValue != None: value = max(maxValue, value)

    # Send back the new value
    return value

  @staticmethod
  def __getRange(node, attribute):
    """
    Return a value range for the given object's attribute.

    Parameters:
      - node      str: Note to access
      - attribute str: Attribute to check against

    Returns:
      list[float, float]: Minimum and maximum range values, None for either if not available.
    """

    # By default no range is available for the given node
    range = [None, None]

    # Save the minimum value if one is present:
    if cmds.attributeQuery(attribute, node = node, minExists = True): range[0] = cmds.attributeQuery(attribute, node = node, min = True)[0]

    # Save the maximum value if one is given:
    if cmds.attributeQuery(attribute, node = node, maxExists = True): range[1] = cmds.attributeQuery(attribute, node = node, max = True)[0]

    # Send back n' attributes value range.
    return range

  @classmethod
  def addNoise(cls, startFrame, endFrame, frameStep = 1, unitVariance = 0.5):
    """
    Add noise to the selected object(s) channels.

    Parameters:
      - startFrame   int  : Start frame range
      - endFrame     int  : End frame range
      - frameSetp    int  : How many frames to move by for the given frame range
      - unitVariance float: How much change for the current attribute value >= 0

    Returns:
      bool: If noise is added
    """

    # Grab the current frame for reset after processing (+1 to offset 0 based index)
    originFrame = cmds.currentTime(query = True)

    # Build a range iterator based on the frame bake options
    frameRange = range(startFrame, endFrame + 1, frameStep)

    # Grab the selected nodes and associated selected channels:
    selectedNodes    = cmds.ls        (selection = True                                             )
    selectedChannels = cmds.channelBox('mainChannelBox', query = True, selectedMainAttributes = True)

    # If there are selected channels which also defines if there are selected objects..
    if selectedChannels != None:

      # Collection of channels to modify
      channelSet = {}

      # Pass 01: Begin collecting channels to modify for each node
      for selectedNode in selectedNodes:

        # For each of the selected channels, determined by the last object selected..
        for selectedChannel in selectedChannels:

          # If the current object has the above attribute (Which it might not) ...
          if cmds.attributeQuery(selectedChannel, node = selectedNode, exists = True):

            # Add a new channel set:
            # object.channel: { value range, slot for frame/value segments }
            channelSet['%s.%s' % (selectedNode, selectedChannel)] = {'range': cls.__getRange(selectedNode, selectedChannel), 'frameSet': []}

      # Pass 02: Calculate new channel values for each target frame
      for frame in frameRange:

        # Move the the target frame
        cmds.currentTime(frame, edit = True)

        # Run through each collected channel
        for channel, channelData in channelSet.items():

          # Split out the available channel range
          minValue, maxValue = channelData['range']

          # Access this channel's current value for the target frame and randomly adjust and clamp.
          currentVal = cmds.getAttr(channel)
          currentVal = cls.__clampValue(minValue, maxValue, rand(currentVal - unitVariance, currentVal + unitVariance))

          # Add a new key segment (frame, new value) to the current channel set.
          # Value clamped to ensire it remains within bounds of the target channel unless no range is available.
          channelSet[channel]['frameSet'].append((frame, currentVal))

      # Pass 03: Channels have been collected, values set, apply those values
      for channel, channelData in channelSet.items():

        # Split out the channel name so we can use its references with setKey
        node, nodeAttr = channel.split('.')

        # For each frame chunk in in this channel..
        for frame in channelData['frameSet']:

          # Get this set's time marker and random value for simplicity
          time, value = frame

          # Add a new keyframe at n' time for n' value for the active object channel
          cmds.setKeyframe(node, attribute = nodeAttr, time = [time, time], value = value)

      # Reset back to the original frame poaition before call
      cmds.currentTime(originFrame, edit = True)

      # Success: Noise added
      return True

    # Error: Nothing selected
    else: cmds.warning('NoisyBoy: Please select one or more animation channels.')

    # Noise not added
    return False

  @classmethod
  def show(cls):
    """
    Show the NoisyBoy interface window
    """

    # If the applicaitin window has yet to be instanced..
    if cls.__window == None:

      # Create that instance and ..
      cls.__window = AppWindow(wrapInstance(int(omui.MQtUtil.mainWindow()), QWidget))

      # Register the only action needed, which is to add noise
      cls.__window.registerActions(addNoise = cls.addNoise)

    # Show the application window
    cls.__window.show()