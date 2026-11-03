import os
import sys
import maya.cmds as cmds

def onMayaDroppedPythonFile(*args, **kwargs):
    """Triggered automatically when this file is dragged into the Maya Viewport."""
    
    # Figure out exactly where this Git repo was cloned on their drive
    repo_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    
    # Locate the user's native Maya application modules folder
    # This automatically tracks user documents on Windows, macOS, or Linux
    maya_app_dir = cmds.internalVar(userAppDir=True)
    modules_dir = os.path.join(maya_app_dir, "modules").replace("\\", "/")
    
    # Create the modules directory if it doesn't exist yet
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
        
    mod_file_path = os.path.join(modules_dir, "MouseBackForth.mod")
    
    # Create and write the .mod file pointing directly to the absolute repo path
    mod_content = f"+ MouseBackForth 1.0 {repo_path}\n"
    
    try:
        with open(mod_file_path, "w") as mod_file:
            mod_file.write(mod_content)
            
        # Notify the user they need to restart to complete the hook
        cmds.confirmDialog(
            title="Installation Complete",
            message=(
                "Installation successful!\n\n"
                "Maya modules require a restart to initialize paths.\n"
                "Please restart Maya, then enable the plugin in your Plug-in Manager."
            ),
            button=["Got It"]
        )
    except Exception as e:
        cmds.confirmDialog(
            title="Installation Failed",
            message=f"Could not write configuration file:\n{e}",
            button=["OK"]
        )
