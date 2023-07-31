# Music-Markers
Blender addon to add markers to the timeline for animating to music.

## Installation
Edit > Preferences > Add-ons > Install > musicmakers.zip
Functionality found in sidebar of 3D viewport. Press N to bring out.

## Usage

The format for naming markers is as follows:

  In 4/4:
  
    1, 1.2, 1.3, 1.4, 2, 2.2, 2.3 etc.
  If set to 3/4:
  
    1, 1.2, 1.3, 2, 2.2, 2.3 etc.
    
  Currently, changing the denominator of the time signature does not work. 1 beat is always set to a quarter note.
  
### Tap Tempo
Tap this button once per beat to automatically calculate a BPM value.

### BPM
The beats per minute used to calculate distance between frames.

### Time Signature:

#### Numerator
Beats per measure.

#### Denominator
Length of a beat. Currently this is locked to quarter notes. Changing this value does nothing at the moment.

### Frame Range:
This will determine the range of the timeline to set markers in.

#### Start Frame
The frame the first marker is placed on. If this is set to 0 than the start frame of the timeline is used.

#### End Frame
The last frame considered for placing markers.

### Set markers
Sets new markers on the timeline based off of the values of the above fields, and the FPS in Blender's 'Output Properties' tab. This will clear all markers on the timeline, including those not created by the addon before placing new ones.

### Clear Markers
Clears all markers on the timeline, including those not created by the addon.
