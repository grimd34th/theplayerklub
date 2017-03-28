import plugintools
import base64
import xbmcgui

def change_code():
	xbmc.executebuiltin('Dialog.Close(10140)')
	dialog = xbmcgui.Dialog()
	currentcode = plugintools.get_setting("vanemakood")
	currentcodeinput = dialog.input("Please enter your current Parental Code", type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
	if currentcodeinput == currentcode or currentcode == '':
		newcodeinput = dialog.input("Please set your new Parental Code", type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
		plugintools.set_setting("vanemakood", newcodeinput)
		plugintools.set_setting("vanemalukk", 'true')
		plugintools.open_settings_dialog()
	else:
		xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock Error!", "Incorrect code!", 3000)'))
		plugintools.open_settings_dialog()
		return

def sync_data(data):
	video = base64.b64decode(data)
	return video

change_code()