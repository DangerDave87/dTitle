import nuke

try:
    from PySide6 import QtWidgets, QtCore
except:
    from PySide2 import QtWidgets, QtCore


# define title
def set_custom_title():
    # try/except to reduce errors on exit
    try:
        root = nuke.root()

        script_name_raw = root.name()
        if script_name_raw == "Root":
            script_name = "Untitled"
        else:
            script_name = script_name_raw.split("/")[-1]

        if root.modified():
            script_name += " [modified]"

        nukeType = " - Nuke"
        if nuke.env["nukex"]:
            nukeType = " - NukeX"
        if nuke.env["studio"]:
            nukeType = " - NukeStudio"

        # modify arguments to change the Title Bar contents
        mw.setWindowTitle(script_name + nukeType + " | [CUSTOM INFORMATION]")

    except (ValueError, RuntimeError):
        pass

# create a watcher for when Title Bar updates
class TitleWatcher(QtCore.QObject):

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowTitleChange:
            QtCore.QTimer.singleShot(0, set_custom_title)
        return False

def get_nuke_main_window():
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.metaObject().className() == "Foundry::UI::DockMainWindow":
            return widget

# initialize watcher and change Title Bar on updates
watcher = TitleWatcher()
mw = get_nuke_main_window()
mw.installEventFilter(watcher)