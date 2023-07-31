import bpy
import time

bl_info = {
    "name": "Music Markers",
    "author": "Husam Staubmann",
    "category": "Animation",
    "location": "View3D > Sidebar > Music Markers",
    "description": "Add BPM markers to the timeline.",
    "support": "COMMUNITY",
    "version": (1, 2, 1),
    "blender": (2, 80, 0),
}

# Global variable to store tap tempo times
tap_tempo_times = []

def update_framerate(self, context):
    if self.music_markers_sync_framerate:
        context.scene.render.fps = self.music_markers_framerate

class MusicMarkersProperties(bpy.types.PropertyGroup):
    music_markers_bpm: bpy.props.FloatProperty(
        name="BPM",
        description="Beats Per Minute",
        default=120,
        min=1,
        step=1
    )

    music_markers_time_sig_numerator: bpy.props.IntProperty(
        name="Numerator",
        description="Beats per measure",
        default=4,
        min=1,
        step=1
    )

    music_markers_time_sig_denominator: bpy.props.IntProperty(
        name="Denominator",
        description="Beat length. Measured in notes. 8 = 8th notes",
        default=4,
        min=2,
        step=1
    )

    music_markers_start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="Start Frame. 0 to use timeline start",
        default=0,
        min=0,
        step=1
    )

    music_markers_end_frame: bpy.props.IntProperty(
        name="End Frame",
        description="End Frame. 0 to use timeline end",
        default=0,
        min=0,
        step=1
    )

    # Add custom property for framerate
    music_markers_framerate: bpy.props.IntProperty(
        name="Framerate",
        description="Custom framerate for markers",
        default=24,  # Set a default value (change this to the desired default framerate)
        min=1,
        step=1,
        update=update_framerate  # Call the update_framerate function when the property changes
    )

    # Add custom property to synchronize scene's framerate with the custom framerate value
    music_markers_sync_framerate: bpy.props.BoolProperty(
        name="Sync Framerate",
        description="Synchronize the scene's framerate with this field",
        default=True,
        update=update_framerate  # Call the update_framerate function when the property changes
    )

def get_default_framerate(self):
    return bpy.context.scene.render.fps

class MUSIC_MARKERS_PT_Panel(bpy.types.Panel):
    bl_label = "Music Markers"
    bl_idname = "MUSIC_MARKERS_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Music Markers"

    def draw(self, context):
        layout = self.layout
        props = context.scene.music_markers_props

        # Display a button for tap tempo
        layout.operator("scene.tap_tempo", text="Tap Tempo")

        # Display an input field for the 'BPM' value
        layout.prop(props, "music_markers_bpm")

        # Display input fields for the time signature
        box = layout.box()
        box.label(text="Time Signature:")
        row = box.row()
        row.prop(props, "music_markers_time_sig_numerator", text="Numerator")
        row.prop(props, "music_markers_time_sig_denominator", text="Denominator")

        # Display input fields for the start and end frame times
        box = layout.box()
        box.label(text="Frame Range:")
        row = box.row()
        row.prop(props, "music_markers_start_frame", text="Start Frame")
        row.prop(props, "music_markers_end_frame", text="End Frame")

        # Display a field for the framerate
        row = layout.row(align=True)
        row.prop(props, "music_markers_framerate", text="Framerate")

        # Display a tickbox to synchronize scene's framerate with the custom framerate value
        row.prop(props, "music_markers_sync_framerate", text="Sync")

        # Display a button to set the markers
        layout.operator("scene.set_music_markers", text="Set Markers")

        # Display a button to clear the markers
        layout.operator("scene.clear_music_markers", text="Clear Markers")

class SCENE_OT_ClearMusicMarkers(bpy.types.Operator):
    bl_idname = "scene.clear_music_markers"
    bl_label = "Clear Music Markers"
    bl_description = "Clears ALL markers from the timeline"
    
    def execute(self, context):
        # Call the function to clear all markers
        clear_markers()

        return {'FINISHED'}

class SCENE_OT_SetMusicMarkers(bpy.types.Operator):
    bl_idname = "scene.set_music_markers"
    bl_label = "Set Music Markers"
    bl_description = "Clears ALL markers and places new ones"
    
    def execute(self, context):
        # Get the BPM value from the custom property group
        props = context.scene.music_markers_props
        BPM = props.music_markers_bpm

        # Get the time signature values from the custom properties
        time_sig_numerator = props.music_markers_time_sig_numerator
        time_sig_denominator = props.music_markers_time_sig_denominator

        # Get the start and end frame times from the custom properties
        start_frame = props.music_markers_start_frame
        end_frame = props.music_markers_end_frame

        # Use Blender's start and end frame values if the input fields are set to 0
        if start_frame == 0:
            start_frame = bpy.context.scene.frame_start
        if end_frame == 0:
            end_frame = bpy.context.scene.frame_end

        # Calculate the marker distance based on the formula md = (60 * FPS) / BPM
        frame_distance = (60 * bpy.context.scene.render.fps) / (BPM * time_sig_denominator / 4)

        # Call the function to clear existing markers and set new markers with the specified distance
        set_markers(frame_distance, start_frame, end_frame, BPM, time_sig_numerator, time_sig_denominator)

        return {'FINISHED'}

class SCENE_OT_TapTempo(bpy.types.Operator):
    bl_idname = "scene.tap_tempo"
    bl_label = "Tap Tempo"
    bl_description = "Tap tempo for BPM"

    def execute(self, context):
        global tap_tempo_times

        # Get the current time
        current_time = time.time()

        # Append the current time to the list of tap tempo times
        tap_tempo_times.append(current_time)

        # Keep only the last 4 tap times
        tap_tempo_times = tap_tempo_times[-4:]

        # Calculate the BPM based on the time difference between taps
        if len(tap_tempo_times) > 1:
            average_time_diff = sum(tap_tempo_times[i] - tap_tempo_times[i-1] for i in range(1, len(tap_tempo_times))) / (len(tap_tempo_times) - 1)
            BPM = 60 / average_time_diff
        else:
            BPM = 120  # Default BPM if there's only one tap

        # Store the updated BPM in the custom property group
        context.scene.music_markers_props.music_markers_bpm = BPM

        return {'FINISHED'}

def set_markers(frame_distance, start_frame, end_frame, BPM, time_sig_numerator, time_sig_denominator):
    # Clear all existing markers
    clear_markers()

    # Set new markers with the calculated frame distance
    current_measure = 1
    current_beat = 1
    beats_per_measure = time_sig_numerator

    for frame in range(start_frame, end_frame, round(frame_distance)):
        # Set marker name based on time signature format
        marker_name = f"{current_measure}"
        if current_beat > 1:
            marker_name += f".{current_beat}"

        bpy.context.scene.timeline_markers.new(name=marker_name, frame=frame)

        # Update current beat and measure
        current_beat += 1
        if current_beat > beats_per_measure:
            current_beat = 1
            current_measure += 1

def clear_markers():
    # Clear all timeline markers
    bpy.context.scene.timeline_markers.clear()

classes = (
    MusicMarkersProperties,
    MUSIC_MARKERS_PT_Panel,
    SCENE_OT_SetMusicMarkers,
    SCENE_OT_TapTempo,
    SCENE_OT_ClearMusicMarkers,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.music_markers_props = bpy.props.PointerProperty(type=MusicMarkersProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.music_markers_props
