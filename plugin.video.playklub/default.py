import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,datetime,os,json,base64,plugintools
import GoDev
import orig
import common,xbmcvfs,zipfile,downloader,extract
import xml.etree.ElementTree as ElementTree
reload(sys)
sys.setdefaultencoding('utf8')
SKIN_VIEW_FOR_MOVIES="515"
addonDir = plugintools.get_runtime_path()
global kontroll
background = "background.png" #background.png
defaultlogo = "logo.png" #defaultlogo.png
hometheater = "hometheater.jpg"
noposter = "noposter.jpg"
theater = "theater.jpg"
addonxml = "addon.xml"
addonpy = "default.py"
icon = "icon.png"
fanart = "fanart.jpg"
message = "UNAUTHORIZED EDIT OF ADDON!"
def run():
	global pnimi
	global televisioonilink
	global filmilink
	global andmelink
	global uuenduslink
	global lehekylg
	global LOAD_LIVE
	global uuendused
	global vanemalukk
	global version
	global showxxx
	version = int(1)
	kasutajanimi=plugintools.get_setting("Username")
	salasona=plugintools.get_setting("Password")
	if not kasutajanimi:
		kasutajanimi = "NONE"
		salasona="NONE"
	lehekylg="http://dns1.theplayersklub.host"
	pordinumber="2095"
	uuendused=plugintools.get_setting("uuendused")
	vanemalukk=plugintools.get_setting("vanemalukk")
	showxxx=plugintools.get_setting("showxxx")
	pnimi = "One View"
	LOAD_LIVE = os.path.join( plugintools.get_runtime_path() , "resources" , "art" )
	plugintools.log(pnimi+"Starting up")
	televisioonilink = "%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories"%(lehekylg,pordinumber,kasutajanimi,salasona)
	filmilink = "%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories"%(lehekylg,pordinumber,kasutajanimi,salasona)
	andmelink = "%s:%s/panel_api.php?username=%s&password=%s"%(lehekylg,pordinumber,kasutajanimi,salasona)
	uuenduslink = "https://www.dropbox.com/s/7em24wd1pddidqo/version.txt?dl=1"
	#if "One View" not in open(addonDir+"/"+"addon.xml").read():
	   #check_user()
	params = plugintools.get_params()
	
	if params.get("action") is None:
		peamenyy(params)
	else:
		action = params.get("action")
		exec action+"(params)"

	plugintools.close_item_list()

def peamenyy(params):
	plugintools.log(pnimi+"Main Menu"+repr(params))
	load_channels()
	if not lehekylg:
	   plugintools.open_settings_dialog()
	if uuendused == "true":
	   kontrolli_uuendusi()
	channels = kontroll()
	if channels == 1 and orig.mode != 5:
	   plugintools.log(pnimi+"Login Success")
	   plugintools.add_item( action="security_check",  title="[COLOR gold][B][I]PLAYERS LIVE[/I][/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,"livetv.png") , fanart=os.path.join(LOAD_LIVE,"background.png") , folder=True )
	   orig.AddDir('[COLOR deepskyblue][B]VOD/RETRO/CATCH UP[/B][/COLOR]','ExtraMenu',5,orig.Images + 'movies.png',orig.Images + 'background.png')
	   orig.AddDir('[COLOR red][B]RED LIGHT[/B][/COLOR]','wizard3',10,orig.Images + 'adt.png',orig.Images + 'background.png')
	   plugintools.addItem('[COLOR orange][B]Launch PVR[/B][/COLOR]','pvr',12,orig.Images + 'extras.png',orig.Images + 'background.png')
	   orig.AddDir('[COLOR teal][B]Clear Cache[/B][/COLOR]','Clear Cache',7,orig.Images + 'clear.png')
	   plugintools.add_item( action="license_check", title="[COLOR orangered][B][I]Settings[/I][/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,"logo.png") , fanart=os.path.join(LOAD_LIVE,"background.png"), folder=False )
	   plugintools.addItem('[COLOR limegreen][B][I]Click to Setup PVR SIMPLE CLIENT[/I][/B][/COLOR]','pvr',11,orig.Images + 'extras.png',orig.Images + 'background.png')
	   
	   
	elif orig.mode != 5:
	   plugintools.add_item( action="license_check",  title="[COLOR yellow][B]Click here to enter login[/B][/COLOR]" , thumbnail=os.path.join(LOAD_LIVE,"logo.png") , fanart=os.path.join(LOAD_LIVE,"background.png") , folder=False )

	   orig.AddDir('[COLOR yellow][B]Click here to refresh after login details have been entered[/B][/COLOR]','Clear Cache',7,orig.Images + 'logo.png')
	if plugintools.get_setting("improve")=="true":
		tseaded = xbmc.translatePath("special://userdata/advancedsettings.xml")
		if not os.path.exists(tseaded):
			file = open( os.path.join(plugintools.get_runtime_path(),"resources","advancedsettings.xml") )
			data = file.read()
			file.close()
			file = open(tseaded,"w")
			file.write(data)
			file.close()
			plugintools.message(pnimi, "New advanced streaming settings added.")



def license_check(params):
	plugintools.log(pnimi+"Settings menu"+repr(params))
	plugintools.open_settings_dialog()
def security_check(params):
	plugintools.log(pnimi+"Live Menu"+repr(params))
	request = urllib2.Request(televisioonilink, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall("channel"):
		kanalinimi = channel.find("title").text
		kanalinimi = base64.b64decode(kanalinimi)
		a = ''
		if showxxx == "false":
		  if any(s in kanalinimi for s in a):
			return
		kategoorialink = channel.find("playlist_url").text
		plugintools.add_item( action="stream_video", title=kanalinimi , url=kategoorialink , thumbnail=os.path.join(LOAD_LIVE,"logo.png") , fanart="" , folder=True )
	plugintools.set_view( plugintools.LIST )
def detect_modification(params):
	plugintools.log(pnimi+"VOD Menu "+repr(params))		
	request = urllib2.Request(filmilink, headers={"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall(channel):
		filminimi = channel.find("title").text
		filminimi = base64.b64decode(filminimi)
		kategoorialink = channel.find("playlist_url").text
		plugintools.add_item( action="get_myaccount", title=filminimi , url=kategoorialink , thumbnail = "" , fanart=os.path.join(LOAD_LIVE,"theater.jpg") , folder=True )
	plugintools.set_view( plugintools.LIST )
def stream_video(params):
	alreadyinput = False
	plugintools.log(pnimi+"Live Channels Menu "+repr(params))
	#if "One View" not in open(addonDir+"/"+"addon.xml").read():
	   #check_user()
	#if vanemalukk == "true":
	 #  pealkiri = params.get("title")
	  # vanema_lukk(pealkiri)
	url = params.get("url")
	request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0',"Accept" : "application/xml"})
	u = urllib2.urlopen(request)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	for channel in tree.findall("channel"):
		kanalinimi = channel.find("title").text
		kanalinimi = base64.b64decode(kanalinimi)
		kanalinimi = kanalinimi.partition("[")
		striimilink = channel.find("stream_url").text
		pilt = channel.find("desc_image").text
		kava = kanalinimi[1]+kanalinimi[2]
		kava = kava.partition("]")
		kava = kava[2]
		kava = kava.partition("   ")
		kava = kava[2]
		shou = get_live("JXM=")%(kanalinimi[0]+kanalinimi[1]+kanalinimi[2])
		kirjeldus = channel.find("description").text
		if kirjeldus:
		   kirjeldus = base64.b64decode(kirjeldus)
		   nyyd = kirjeldus.partition("(")
		   nyyd = "NOW: " +nyyd[0]
		   jargmine = kirjeldus.partition(")\n")
		   jargmine = jargmine[2].partition("(")
		   jargmine = "NEXT: " +jargmine[0]
		   kokku = nyyd+jargmine
		else:
		   kokku = ""
		a = ''
		if vanemalukk == "true":
		  if alreadyinput != True:
			if any(s in shou for s in a):
				xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock Enabled!", "Channels may contain adult content", 2000)'))
				dialog = xbmcgui.Dialog()
				text = dialog.input("Parental-Lock: Please enter your Parental Code", type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
				if text!=plugintools.get_setting("vanemakood"):
					xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock Error!", "Incorrect code!", 3000)'))
					return
				else:
					alreadyinput = True
		if pilt:
		   plugintools.add_item( action="run_cronjob", title=shou , url=striimilink, thumbnail=pilt, plot=kokku, fanart=os.path.join(LOAD_LIVE,"hometheater.jpg"), extra="", isPlayable=True, folder=False )
		else:
		   plugintools.add_item( action="run_cronjob", title=shou , url=striimilink, thumbnail=os.path.join(LOAD_LIVE,"logo.png") , plot=kokku, fanart=os.path.join(LOAD_LIVE,"hometheater.jpg") , extra="", isPlayable=True, folder=False )
	if sync_data('Y2F0X2lkPTM=') in url:
	  plugintools.set_view( plugintools.MOVIES )
	else:
	  plugintools.set_view( plugintools.LIST )
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
def get_myaccount(params):
		plugintools.log(pnimi+"VOD channels menu "+repr(params))
		#if vanemalukk == "true":
		   #pealkiri = params.get("title")
		   #vanema_lukk(pealkiri)
		purl = params.get("url")
		request = urllib2.Request(purl, headers={"Accept" : "application/xml"})
		u = urllib2.urlopen(request)
		tree = ElementTree.parse(u)
		rootElem = tree.getroot()
		for channel in tree.findall("channel"):
			pealkiri = channel.find("title").text
			pealkiri = base64.b64decode(pealkiri)
			pealkiri = pealkiri.encode("utf-8")
			striimilink = channel.find("stream_url").text
			pilt = channel.find("desc_image").text
			kirjeldus = channel.find("description").text
			if kirjeldus:
			   kirjeldus = base64.b64decode(kirjeldus) 
			if pilt:
			   plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=pilt, plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,"theater.jpg") , extra="", isPlayable=True, folder=False )
			else:
			   plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=os.path.join(LOAD_LIVE,"noposter.jpg"), plot=kirjeldus, fanart="" , extra="", isPlayable=True, folder=False )
		plugintools.set_view( plugintools.MOVIES )
		xbmc.executebuiltin('Container.SetViewMode(515)')


def run_cronjob(params):
	extend=plugintools.get_setting("extend")
	plugintools.log(pnimi+"PLAY_LIVE"+repr(params))
	#if vanemalukk == "true":
	   #pealkiri = params.get("title")
	   #vanema_lukk(pealkiri)
	lopplink = params.get("url")
	lopplink = lopplink.replace('.ts','.%s'%extend)
	plugintools.play_resolved_url( lopplink )
	
def run_cronjobxxx(params):
	kasutajanimi=plugintools.get_setting("Username")
	salasona=plugintools.get_setting("Password")
	lopplink = params.get("url")
	if "http://"  not in lopplink: 
		lopplink = "http://otttv.ga:2095/live/%s/%s/%s"%(kasutajanimi,salasona,lopplink)
		lopplink = lopplink[:-2]
		lopplink = lopplink + "m3u8"
	listitem = xbmcgui.ListItem(path=lopplink)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)




def sync_data(channel):
	video = base64.b64decode(channel)
	return video


def restart_service(params):
	lopplink = params.get("url")
	plugintools.play_resolved_url( lopplink )



def grab_epg():
	req = urllib2.Request(andmelink)
	req.add_header("User-Agent" , "Kodi plugin by MikkM")
	response = urllib2.urlopen(req)
	link=response.read()
	jdata = json.loads(link.decode('utf8'))
	response.close()
	if jdata:
	   plugintools.log(pnimi+"jdata loaded ")
	   return jdata
def kontroll():
	randomstring = grab_epg()
	kasutajainfo = randomstring["user_info"]
	kontroll = kasutajainfo["auth"]
	return kontroll
def get_live(channel):
	video = base64.b64decode(channel)
	return video
def execute_ainfo(params):
	plugintools.log(pnimi+"My account Menu "+repr(params))
	andmed = grab_epg()
	kasutajaAndmed = andmed["user_info"]
	seis = kasutajaAndmed["status"]
	aegub = kasutajaAndmed["exp_date"]
	if aegub:
	   aegub = datetime.datetime.fromtimestamp(int(aegub)).strftime('%d/%m/%Y %H:%M')
	else:
	   aegub = "Never"
	leavemealone = kasutajaAndmed["max_connections"]
	polarbears = kasutajaAndmed["username"]
	plugintools.add_item( action="",   title="[COLOR = white]User: [/COLOR]"+polarbears , thumbnail=os.path.join(LOAD_LIVE,"livetv.png") , fanart=os.path.join(LOAD_LIVE,"theater.jpg") , folder=False )
	plugintools.add_item( action="",   title="[COLOR = white]Status: [/COLOR]"+seis , thumbnail=os.path.join(LOAD_LIVE,"livetv.png") , fanart=os.path.join(LOAD_LIVE,"theater.jpg") , folder=False )
	plugintools.add_item( action="",   title="[COLOR = white]Expires: [/COLOR]"+aegub , thumbnail=os.path.join(LOAD_LIVE,"livetv.png") , fanart=os.path.join(LOAD_LIVE,"theater.jpg") , folder=False )
	plugintools.add_item( action="",   title="[COLOR = white]Max connections: [/COLOR]"+leavemealone , thumbnail=os.path.join(LOAD_LIVE,"livetv.png") , fanart=os.path.join(LOAD_LIVE,"theater.jpg") , folder=False )
	plugintools.add_item( action="",   title="Sign up at FutureStreams.tk" , thumbnail=os.path.join(LOAD_LIVE,vod_channels("bXlhY2MucG5n")) , fanart=os.path.join(LOAD_LIVE,"theater.jpg") , folder=False )
	
	plugintools.set_view( plugintools.LIST )
def vanema_lukk(name):
		plugintools.log(pnimi+"Parental lock ")
		a = ''
		if any(s in name for s in a):
		   xbmc.executebuiltin((u'XBMC.Notification("Parental-Lock", "Channels may contain adult content", 2000)'))
		   text = plugintools.keyboard_input(default_text="", title="Parental-Lock: Please enter your Parental Code")
		   if text==plugintools.get_setting("vanemakood"):
			  return
		   else:
			  exit()
		else:
		   name = ""
def kontrolli_uuendusi():
		req = urllib2.Request(uuenduslink)
		req.add_header("User-Agent" , "Kodi plugin by MikkM")
		response = urllib2.urlopen(req)
		repoversion=response.read()
		repoversion = repoversion.partition("\n")
		iversion = repoversion[1]
		global dlink
		dlink = repoversion[2]
		response.close()
		if iversion <> version:
		   update = " "
		else:
		   if plugintools.message_yes_no(pnimi,"New update is available!","Do you want to update plugin now?"):
			  plugintools.log( pnimi+"Trying to update plugin...")
			  try:
				  destpathname = xbmc.translatePath(os.path.join("special://","home/addons/"))
				  local_file_name = os.path.join( plugintools.get_runtime_path() , "update.zip" )
				  plugintools.log(pnimi+local_file_name)
				  urllib.urlretrieve(dlink, local_file_name )
				  DownloaderClass(dlink,local_file_name)
				  plugintools.log(pnimi+"Extracting update...")
				  import ziptools
				  unzipper = ziptools.ziptools()
				  #destpathname = xbmc.translatePath(os.path.join('special://','home'))
				  plugintools.log(pnimi+destpathname)
				  unzipper.extract( local_file_name , destpathname )
				  os.remove(local_file_name)
				  xbmc.executebuiltin((u'XBMC.Notification("Updated", "The add-on has been updated", 2000)'))
				  #import updater
				  xbmc.executebuiltin( "Container.Refresh" )
				  plugintools.log(pnimi+"Update success")
			  except:
				  plugintools.log(pnimi+"Update failed")
				  xbmc.executebuiltin((u'XBMC.Notification("Not updated", "An error causes the update to fail", 2000)'))
def DownloaderClass(url,dest):
	dp = xbmcgui.DialogProgress()
	dp.create("Getting update","Downloading")
	urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
def check_user():
	plugintools.message("ERROR","UNAUTHORIZED EDIT OF ADDON!")
	sys.exit()
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		print percent
		dp.update(percent)
	except:
		percent = 100
		dp.update(percent)
	if dp.iscanceled(): 
		print "DOWNLOAD CANCELLED" # need to get this part working
		dp.close()
def load_channels():
	statinfo = os.stat(LOAD_LIVE+"/"+"background.png")

def vod_channels(channel):
	video = base64.b64decode(channel)
	return video
run()