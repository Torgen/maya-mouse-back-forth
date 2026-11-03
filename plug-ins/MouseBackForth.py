import maya.api.OpenMaya as om
import maya.cmds as cmds
from PySide6 import QtCore, QtWidgets

# Dict and filter setup as variables
MOUSE_BUTTONS = {
    QtCore.Qt.MouseButton.XButton1: -1,
    QtCore.Qt.MouseButton.XButton2: 1
}
MIDDLE_MOUSE = QtCore.Qt.MouseButton.MiddleButton

class MouseBackForth(QtCore.QObject):
    def eventFilter(self, obj, event):
        if not (event.type() == QtCore.QEvent.Type.MouseButtonPress and QtWidgets.QApplication.activeWindow() and event.button() in MOUSE_BUTTONS):
            return super().eventFilter(obj, event)
        frame_offset = MOUSE_BUTTONS[event.button()]
        new_time = cmds.currentTime(query=True) + frame_offset
        is_mmb_held = bool(QtWidgets.QApplication.mouseButtons() & MIDDLE_MOUSE)
        cmds.currentTime(new_time, edit=True, update=not is_mmb_held)
        return True

# Global tracking variable for the filter instance
_instance = None

def maya_useNewAPI():
    pass

def initializePlugin(plugin_obj):
    """Called explicitly by Maya when the user checks 'Loaded' in Plug-in Manager."""
    global _instance
    plugin = om.MFnPlugin(plugin_obj, "Dan Rosart", "1.0", "Any")
    
    # Attach filter to Maya main window
    qapp = QtWidgets.QApplication.instance()
    _instance = MouseBackForth()
    qapp.installEventFilter(_instance)
    
    print(f"buttons: {MOUSE_BUTTONS}")

def uninitializePlugin(plugin_obj):
    """Called explicitly by Maya when the user unchecks 'Loaded'."""
    global _instance
    qapp = QtWidgets.QApplication.instance()
    
    if _instance:
        try:
            qapp.removeEventFilter(_instance)
        except Exception:
            pass
        _mouse_filter_instance = None
