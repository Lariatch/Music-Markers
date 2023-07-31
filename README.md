# Music-Markers
Blender addon to add markers to the timeline for animating to music.

## Installation
Download latest version from releases page.

https://github.com/Lariatch/Music-Markers/releases

In Blender, Edit > Preferences > Add-ons > Install > musicmarkers.zip

Functionality found in sidebar of 3D viewport. Press N to bring out.

## Usage

The format for naming markers is as follows:

  In 4/4:
  
    1, 1.2, 1.3, 1.4, 2, 2.2, 2.3, 2.4
  If set to 3/4:
  
    1, 1.2, 1.3, 2, 2.2, 2.3
  If set to 6/8:
  
    1, 1.2, 1.3, 1.4, 1.5, 1.6, 2, 2.1
    
  With markers placed every 8th note.

  Any time signature should work.
  
### Tap Tempo
Tap this button once per beat to automatically calculate a BPM value.

### BPM
The beats per minute used to calculate distance between frames.

### Time Signature:

#### Numerator
Beats per measure.

#### Denominator
Length of a beat. A value of 8 sets the length to 8th notes, 16 = 16th notes etc

### Frame Range:
This will determine the range of the timeline to set markers in. If they are set to 0 the blend files timeline range is used.

#### Start Frame
The frame the first marker is placed on.

#### End Frame
The last frame considered for placing markers.

### Framerate
Sets the framerate used to calculate marker distance. If 'Sync' is checked the scenes framerate will copy this value.

### Set markers
Sets new markers on the timeline based off of the values of the above fields. This will clear all markers on the timeline, including those not created by the addon before placing new ones.

### Clear Markers
Clears all markers on the timeline, including those not created by the addon.

## To Do
Changing BPM and time signature.
FPS to seconds switch for all fields.
