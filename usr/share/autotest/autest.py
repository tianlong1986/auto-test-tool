#!/usr/bin/python
# -*- coding: utf-8 -*-
#author: tom
#update: 2012.09.20
#version: 1.1.1
#description:
#This is a test tool
#
#changelog:
#
import gtk, gobject
import ConfigParser
import MySQLdb
import test
import os
import commands
import pickle
import pango

#script_path="/tmp/autotest/"
script_path="/usr/share/autotest/"
status,user_name=commands.getstatusoutput('whoami') 
result_file="".join("/home/%s/.cache/autotest.txt" % (user_name))
all_sel_item_file="/tmp/.all_item"
config_file="/tmp/autotest.cfg"
#finish_file,if have test complete.
finish_file="/tmp/.atFinish"
#the window forground color,the every value is 0-65535
#win_fg_color=gtk.gdk.Color(red=0, green=0, blue=0, pixel=0)
win_fg_color=gtk.gdk.Color(60, 55500, 33,63000)
win_bg_color=gtk.gdk.Color(60000, 65000, 55003, 60000)
button_bg_color=gtk.gdk.Color(60000, 65000, 30003, 60000)
finish_text_color=gtk.gdk.Color(60000, 5000, 30003, 60000)
win_bg_image="/usr/share/autotest/bg/1.jpg"

TEXT_NEXT="  Save  "
TEXT_BACK="  Back  "
TEXT_SKIP="  Skip  "

#button size
BTN_WIDTH=80
BTN_HEIGHT=35
#main window size
WIN_WIDTH=680
WIN_HEIGHT=640
class MainUI(gtk.Window):
	def __init__(self):
		super(MainUI,self).__init__()
		self.check_user()
		self.set_title("Linpus test tool")
		self.set_size_request(WIN_WIDTH,WIN_HEIGHT)
		self.set_position(gtk.WIN_POS_CENTER)
		self.vbox=gtk.VBox(False, 2)
		self.add(self.vbox)
		self.show_hk_tip = False
		#if this is first run,show select test item
		self.set_bg_image(self, win_bg_image)
		if self.need_recover():
			self.get_tc_from_file()
			if self.nowItem >= self.allSelItem:
				self.nowItem = self.allSelItem
			if self.is_complete():
				self.remove(self.vbox)
				self.show_test_result()
			else:
				if self.tcInfo[self.nowItem-2][1].find("Hotkey") != -1:
					self.show_hk_tip = True
				self.show_test()
				#self.show_all()
				
				#print self.tcInfo[self.nowItem-1][4]
				#if self.tcInfo[self.nowItem-1][4] != 1:
				#	self.next_button.hide()
				#	self.auto_button.show()
				#else:
				#	self.next_button.show()
				#	self.auto_button.hide()
				#self.show_result_when_back()
				#if self.nowItem == self.allSelItem:
				#	self.next_button.set_label("Save")
				#	self.next_button.show()
				#	self.auto_button.hide()
				#else :
				#	self.next_button.set_label(TEXT_NEXT)
		else:
			self.showSelect()
			print "don't need to recovery"
			cmd="".join("echo [test_result]> %s" % (result_file))
			print cmd
			os.system(cmd)
			self.show_all()
	                cmd="sudo bash -c \"echo /tmp/autotest/autest.py >> /etc/rc.d/slim/nowait.sh\""
                	os.system(cmd)

			
		self.modify_window_color()
		self.connect("destroy", gtk.main_quit)

	def modify_window_color(self):
		self.modify_fg(gtk.STATE_NORMAL, win_fg_color)
		self.modify_fg(gtk.STATE_ACTIVE, win_fg_color)
		self.modify_fg(gtk.STATE_PRELIGHT, win_fg_color)
		self.modify_fg(gtk.STATE_SELECTED, win_fg_color)
	
		self.modify_bg(gtk.STATE_NORMAL, win_bg_color)
		self.modify_bg(gtk.STATE_ACTIVE, win_bg_color)
		self.modify_bg(gtk.STATE_PRELIGHT, win_bg_color)
		self.modify_bg(gtk.STATE_SELECTED, win_bg_color)
		self.set_opacity(0.9)
		self.set_decorated(True)

	# set widget background image
	def set_bg_image(self,widget,filename):

		style = widget.get_style().copy()
		img_pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
		img_pixmap = img_pixbuf.render_pixmap_and_mask()[0]
		for state in (gtk.STATE_NORMAL, gtk.STATE_ACTIVE, gtk.STATE_PRELIGHT,
                	gtk.STATE_SELECTED, gtk.STATE_INSENSITIVE):
			style.bg_pixmap[state] = img_pixmap
			widget.set_style(style)
			
		
	def con_db(self):
		config = ConfigParser.ConfigParser()
		config.readfp(open(config_file), "rb");
		strHost = config.get("database", "host")
		strUser = config.get("database", "user")
		strPasswd = config.get("database", "password")
		#strPasswd=""
		strDb = config.get("database", "db_name")
		try:
                	self.conn = MySQLdb.Connect(host=strHost, user=strUser, passwd=strPasswd, db=strDb,charset='utf8')
#			return True
		except Exception, e:
			print e
			self.msg_box("Connect to server failed, please check the network status.\nEnsure that the network is connected,and then try again.")
#			return False
	def close_db(self):
		self.cursor.close()
		self.conn.close()

	def get_type_from_db(self):

                self.cursor = self.conn.cursor()
		self.cursor.execute('select tc_type, count(*) from autotest group by tc_type')
		self.alltype = self.cursor.fetchall()
		self.selected = [0,0,[]]



	#Show all test type 	
	def showSelect(self):
		selLabel=gtk.Label("Please select the test items")
		scrollWin=gtk.ScrolledWindow()
		scrollWin.set_size_request(300,400)
		scrollWin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		self.vbox.pack_start(selLabel, False,False, 20)
		store = gtk.ListStore(gobject.TYPE_STRING,
                                         gobject.TYPE_BOOLEAN,
					 gobject.TYPE_INT )
		self.con_db()
		self.get_type_from_db()
		self.typeNum = 0
		#self.get_kblayout()
                for item in self.alltype:
                	store.append((item[0], None, item[1]))
			self.typeNum += 1
				
		treeView = gtk.TreeView(store)
		cell2 = gtk.CellRendererToggle()
        	cell2.set_property('activatable', True)
       		cell2.connect( 'toggled', self.on_item_clicked, store)
	        cell1 = gtk.CellRendererText()
        	cell1.set_property( 'editable', False )
        	#cell1.connect( 'edited', self.col0_edited_cb, store )

		column1 = gtk.TreeViewColumn("Test type\t\t\t\t\t\t\t", cell1, text=0)
        	column2 = gtk.TreeViewColumn("\t\t\t\t\tSelect", cell2 )
        	column2.add_attribute( cell2, "active", 1)


		#cell.connect("toggled", self.on_item_clicked)
                treeView.append_column(column1)
                treeView.append_column(column2)
		treeView.columns_autosize()
		scrollWin.add(treeView)
		#select all
		chkAll = gtk.CheckButton("Check All")
		chkAll.set_active(False)
		chkAll.unset_flags(gtk.CAN_FOCUS)
		chkAll.connect("clicked", self.on_chkAll_clicked, store)
		#total select label
		self.selMsgLabel = gtk.Label()
		hbox1 = gtk.HBox()
		hbox1.pack_end(self.selMsgLabel, False, False,5)	

		#start button
		startBtn = gtk.Button("Start")
		startBtn.connect("clicked", self.start_test_clicked, store)
		startBtn.set_size_request(100, 30)
		startBtn.set_tooltip_text("Click me,start test")
		self.set_button_bg_color(startBtn, button_bg_color)
		hbox2 = gtk.HBox()
		hbox2.pack_start(startBtn, True, False, 0)
		startBtn.set_size_request(100, 30)
		treeView.set_rules_hint(True)
		self.vbox.pack_start(scrollWin, False,False, 2)
		self.vbox.pack_start(hbox1, False,False, 0)
		self.vbox.pack_start(chkAll, False,False, 20)
		self.vbox.pack_start(hbox2, False,False, 20)
	def on_chkAll_clicked(self, widget, model):
		i = 0
		bCheck = widget.get_active()
		self.selected = [0,0,[]]
		while i < self.typeNum:
			self.check_item(model, i, bCheck)
			i += 1
		self.selMsgLabel.set_label("".join("Total select %d types (%d  items)" % (self.selected[0] , self.selected[1])))	
	def check_item(self,model,path,bCheck):
		print model[path][1],bCheck
		model[path][1] = bCheck
		if model[path][1]:
			self.selected[0]+=1
			self.selected[1]+=model[path][2]
			self.selected[2].append(model[path][0])
		else:
		#	self.selected[0]-=1
		#	self.selected[1]-=model[path][2]
		#	self.selected[2].remove(model[path][0])
			self.selected = [0,0,[]]

	def on_item_clicked(self, widget, path, model):
	        """
        	Sets the toggled state on the toggle button to true or false.
        	"""
        	model[path][1] = not model[path][1]
        	print "path=%s,Toggle '%s' to: %s" % (path,model[path][0], model[path][1],)
		if model[path][1]:
			self.selected[0]+=1
			self.selected[1]+=model[path][2]
			self.selected[2].append(model[path][0])
		else:
			self.selected[0]-=1
			self.selected[1]-=model[path][2]
			self.selected[2].remove(model[path][0])
		self.selMsgLabel.set_label("".join("Total select %d types (%d items)" % (self.selected[0] , self.selected[1])))	
			
        	return

    	def col0_edited_cb( self, cell, path, new_text, model ):
        	"""
        	Called when a text cell is edited.  It puts the new text
        	in the model so that it is displayed properly.
        	"""
        	print "Change '%s' to '%s'" % (model[path][0], new_text)
        	model[path][0] = new_text
        	return
	def start_test_clicked(self, widget, model):
		self.set_title("Testing")
		self.get_tc_from_db()
		self.nowItem = 1
		self.show_test();
	def get_tc_from_file(self):
		f = file(all_sel_item_file, 'r')
		self.tcInfo = pickle.load(f)
		self.allSelItem = len(self.tcInfo)
		f.close()
		
	def get_tc_from_db(self):
		sql = "select tc_id, tc_type,tc_step, tc_biaozhun, tc_level,tc_script,tc_sn, tc_item from autotest where tc_type in ("
		tmp = 0
		print sql
		for i in self.selected[2]:
			print sql
			if not tmp:
				sql = sql + "".join("'%s'" % i)
			else:
				sql = sql + "".join(", '%s'" % i)
			tmp = tmp + 1
		sql = sql + "".join(")")
		
		print sql
		self.allSelItem = self.cursor.execute(sql)
		self.tcInfo = self.cursor.fetchall();
		cmd = "".join("sudo rm -rf %s" % all_sel_item_file)
		os.system(cmd)
		#save select items to file
		f = file(all_sel_item_file, 'w')
		pickler = pickle.Pickler(f)
		pickler.dump(self.tcInfo)
		f.close()
		self.close_db()


	def show_test(self):
		self.testVbox=gtk.VBox()
		print self.nowItem
		label="".join("%s           (%d/%d)" %(str(self.tcInfo[self.nowItem-1][1]).decode('utf-8'), self.nowItem,self.allSelItem))
		self.title_label = gtk.Label(label)
		#hbox item
		strItem="".join("%s : %s" %(str(self.tcInfo[self.nowItem-1][6]).decode('utf-8'),str(self.tcInfo[self.nowItem-1][7]).decode('utf-8')))
		self.item_label = gtk.Label(strItem)
		hbox1 = gtk.HBox(False, 2)
                hbox1.pack_start(self.item_label, False, False, 2)
		self.check_hk_tip()
		cmd="".join("echo %d > /tmp/.nowItem" % self.nowItem) 	
		os.system(cmd)
		
		#the file result to 
		if not os.path.isfile(result_file):
			os.system("".join("echo [test_result] > %s" % result_file))
		self.rsConfig = ConfigParser.ConfigParser()
		self.rsConfig.readfp(open(result_file), "rw")
		if not self.rsConfig.has_section("test_result"):
			self.add_section(section)


		# test step
		stepLabel=gtk.Label("test step:")
                self.step_buffer = gtk.TextBuffer()
                self.step_buffer.set_text(self.tcInfo[self.nowItem -1][2].decode('utf-8'))
                stepScrolledWin=gtk.ScrolledWindow()
                stepTextView = gtk.TextView(self.step_buffer)
                stepTextView.set_editable(False)
                stepTextView.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(514, 5140, 5140))
                stepTextView.set_cursor_visible(False)
                stepTextView.set_wrap_mode (gtk.WRAP_CHAR);
                stepTextView.set_size_request(100, 150)
		stepScrolledWin.add(stepTextView)
		stepScrolledWin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		# test biaozhun
		stdLabel = gtk.Label("standard:")
                self.std_buffer = gtk.TextBuffer()
                self.std_buffer.set_text(self.tcInfo[self.nowItem -1][3].decode('utf-8'))
                stdScrolledWin=gtk.ScrolledWindow()
                stdTextView = gtk.TextView(self.std_buffer)
                stdTextView.set_editable(False)
                stdTextView.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(514, 220, 50))
                stdTextView.set_cursor_visible(False)
                stdTextView.set_wrap_mode (gtk.WRAP_CHAR);
                stdTextView.set_size_request(100, 150)
		stdScrolledWin.add(stdTextView)
		stdScrolledWin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
	
		# comment
		commentLabel = gtk.Label("comment:")
                self.comment_buffer = gtk.TextBuffer()
                #self.comment_buffer.set_text(self.tcInfo[0][3].decode('utf-8'))
                commentScrolledWin=gtk.ScrolledWindow()
                commentTextView = gtk.TextView(self.comment_buffer)
                commentTextView.set_editable(True)
                commentTextView.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(514, 220, 50))
                commentTextView.set_cursor_visible(True)
                commentTextView.set_wrap_mode (gtk.WRAP_CHAR);
                commentTextView.set_size_request(100, 75)
		commentScrolledWin.add(commentTextView)
		commentScrolledWin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)



                self.radio_pass = gtk.RadioButton()
                self.radio_pass.set_label("PASS")
                self.radio_fail = gtk.RadioButton(self.radio_pass, "FAIL", True)
                self.next_button = gtk.Button(TEXT_NEXT)
		self.next_button.set_size_request(BTN_WIDTH,BTN_HEIGHT)
                self.next_button.connect("clicked", self.on_next_click)
                self.back_button = gtk.Button(TEXT_BACK)
		self.back_button.set_size_request(BTN_WIDTH,BTN_HEIGHT)
                self.back_button.connect("clicked", self.on_back_click)
                self.auto_button = gtk.Button("Auto test")
                self.auto_button.connect("clicked", self.on_auto_click)
		self.auto_button.set_size_request(BTN_WIDTH,BTN_HEIGHT)
		self.skip_button = gtk.Button(TEXT_SKIP)
		self.skip_button.connect("clicked", self.on_skip_click)
		self.skip_button.set_size_request(BTN_WIDTH,BTN_HEIGHT)
	
		#self.set_widget_icon(self.next_button,"/home/tom/test/python/icon.png" )
		#self.set_widget_icon(self.back_button,"/home/tom/test/python/start-here.png" )
		#self.set_bg_image(self.skip_button,"/home/tom/Media/bg/4.jpg" )
		hbox = gtk.HBox(False, 2)
                hbox.pack_start(self.back_button, True, False, 15)
                hbox.pack_start(self.radio_pass, True, False, 30)
                hbox.pack_start(self.radio_fail, True, False, 20)
                hbox.pack_start(self.next_button, True, False, 30)
                hbox.pack_start(self.auto_button, True, False, 30)
                hbox.pack_start(self.skip_button, True, False, 30)
		#pack the three label to hbox 
		stepHbox = gtk.HBox()
		stepHbox.pack_start(stepLabel, False, False, 2)
		stdHbox = gtk.HBox()
		stdHbox.pack_start(stdLabel, False, False, 2)
		commentHbox = gtk.HBox()
		commentHbox.pack_start(commentLabel, False, False, 2)
		#pack to vbox
		self.testVbox.pack_start(self.title_label, False, False, 2)
		self.testVbox.pack_start(hbox1, False, False, 2)
                self.testVbox.pack_start(stepHbox, False, False, 2)
                self.testVbox.pack_start(stepScrolledWin, True, True, 2)
                self.testVbox.pack_start(stdHbox, False, False, 5)
                self.testVbox.pack_start(stdScrolledWin, True, True, 2)
                self.testVbox.pack_start(commentHbox, False, False, 5)
                self.testVbox.pack_start(commentScrolledWin, True, True, 2)
                self.testVbox.pack_start(hbox, False, False, 5)

		self.remove(self.vbox)
		self.set_button_bg_color(self.next_button, button_bg_color)
		self.set_button_bg_color(self.auto_button, button_bg_color)
		#self.set_button_bg_color(self.back_button, button_bg_color)
		#self.set_button_bg_color(self.skip_button, button_bg_color)
		self.set_button_bg_color(self.radio_pass, button_bg_color)
		self.set_button_bg_color(self.radio_fail, button_bg_color)
		self.set_button_bg_color(self.testVbox, button_bg_color)
		self.add(self.testVbox)
		self.modify_window_color()
		#stdTextView.setBackgroundColor(Color.argb(255, 0, 255, 0)); #set Alpha
		#stdScrolledWin.get_window().set_opacity(0.80)
		#stdTextView.get_window(gtk.TEXT_WINDOW_WIDGET).set_opacity(0.80)
		#self.set_bg_image(self,"/home/tom/Media/icon/1.jpg")
		#self.set_bg_image(self.skip_button,"/home/tom/test/python/icon.png")
		#self.set_widget_icon(self.back_button, "/home/tom/test/python/icon.png")
		#self.skip_button.window.set_opacity(0.5)

		self.show_all()
		self.judge_show_button()

	def set_blend (color1, color2, weight = 0.5):
		    return gtk.gdk.Color (
        			color1.red_float   * weight + color2.red_float   * (1 - weight),
        			color1.green_float * weight + color2.green_float * (1 - weight),
        			color1.blue_float  * weight + color2.blue_float  * (1 - weight))
	def set_button_bg_color(self, widget, color):
		widget.modify_bg(gtk.STATE_NORMAL, color)
		widget.modify_bg(gtk.STATE_ACTIVE, color)
		widget.modify_bg(gtk.STATE_PRELIGHT, color)
		
		widget.modify_fg(gtk.STATE_NORMAL, color)
		widget.modify_fg(gtk.STATE_ACTIVE, color)
		widget.modify_fg(gtk.STATE_PRELIGHT, color)

	def set_widget_icon(self, widget, imgfile):
    		image = gtk.Image()
		image.set_from_file(imgfile)
		self.back_button.set_image(image)
		widget.show()

        def on_next_click(self, widget):
		if not self.nextFromAuto:
			if self.radio_pass.get_active():
				rs='P'
			else:
				rs='F'
			self.rsConfig.readfp(open(result_file), "rw")
			self.rsConfig.set("test_result", "".join("item_%d" % (self.tcInfo[self.nowItem-1][0])), rs)
			print self.comment_buffer.get_text(self.comment_buffer.get_start_iter(), self.comment_buffer.get_end_iter())
			self.rsConfig.set("test_result", "".join("item_%d_comment" % (self.tcInfo[self.nowItem-1][0])),\
					 self.comment_buffer.get_text(self.comment_buffer.get_start_iter(), 				
									self.comment_buffer.get_end_iter()))
			self.rsConfig.write(open(result_file, "w"))
		self.nextFromAuto=False
		self.comment_buffer.set_text("")
		self.back_button.show()
		self.nowItem = self.nowItem + 1
		cmd="".join("echo %d > /tmp/.nowItem" % self.nowItem) 	
		os.system(cmd)
		
		if self.nowItem == self.allSelItem :
			print self.nowItem+1000
			#widget.hide()	
			widget.set_label("Save")
		elif self.nowItem > self.allSelItem:
			cmd="".join("echo %d > /tmp/.nowItem" % self.allSelItem) 	
			self.on_finish()
			return
			
		#self.show_result_when_back()
		print self.nowItem+1000
		if  self.tcInfo[self.nowItem-1]:
			print self.nowItem
			print self.allSelItem
			label="".join("%s           (%d/%d)" %(str(self.tcInfo[self.nowItem-1][1]).decode('utf-8'),\
								 self.nowItem,self.allSelItem))
               		self.title_label.set_label(label)
			strItem="".join("%s : %s" \
					%(str(self.tcInfo[self.nowItem-1][6]).decode('utf-8'),\
					str(self.tcInfo[self.nowItem-1][7]).decode('utf-8')))
			self.item_label.set_label(strItem)
	               	self.step_buffer.set_text(str(self.tcInfo[self.nowItem-1][2]).decode('utf-8'))
        	       	self.std_buffer.set_text(str(self.tcInfo[self.nowItem-1][3]).decode('utf-8'))
			self.judge_show_button()
			self.check_hk_tip()
		else:
			print "have finished"
 	def on_back_click(self, widget):
		self.nowItem = self.nowItem - 1
		self.judge_show_button()
		cmd="".join("echo %d > /tmp/.nowItem" % self.nowItem) 	
		os.system(cmd)
		if self.nowItem <= 1:
			widget.hide()
		if  self.tcInfo[self.nowItem-1]:
			print self.nowItem
			print self.allSelItem
			label="".join("%s           (%d/%d)" %(str(self.tcInfo[self.nowItem-1][1]).decode('utf-8'), \
								self.nowItem, self.allSelItem))
               		self.title_label.set_label(label)
			strItem="".join("%s : %s" %(str(self.tcInfo[self.nowItem-1][6]).decode('utf-8'),\
							str(self.tcInfo[self.nowItem-1][7]).decode('utf-8')))
			self.item_label.set_label(strItem)
	               	self.step_buffer.set_text(str(self.tcInfo[self.nowItem-1][2]).decode('utf-8'))
        	       	self.std_buffer.set_text(str(self.tcInfo[self.nowItem-1][3]).decode('utf-8'))
			self.show_result_when_back()
		else:
			print "have finished"
		self.get_all_result()
	def on_auto_click(self, widget):
		print "run the autotest script"
		testscript="".join("%s%s %d" % (script_path,str(self.tcInfo[self.nowItem-1][5]).decode('utf-8'),\
								 self.tcInfo[self.nowItem-1][0]))
		print testscript
		self.set_title("Now auto testting,please wait")
		os.system(testscript)
		self.set_title("Linpus test tool")
		label="".join("%s           (%d/%d)" %(str(self.tcInfo[self.nowItem-1][1]).decode('utf-8'), self.nowItem,self.allSelItem))
		self.title_label = gtk.Label(label)
		if self.nowItem != self.allSelItem:
			self.nextFromAuto=True
			self.next_button.clicked();
		else:
			self.next_button.set_label("Save")
			self.next_button.show()
			self.auto_button.hide()

		return
	def on_skip_click(self, widget):
		self.nextFromAuto = True
		self.next_button.clicked()
		
	def on_finish(self):
		msg = "All test items have test finish,now upload the test result to DB,Please ensure that the network is connected"
		cmd="".join("echo Y > %s" % finish_file)
		os.system(cmd)

		self.remove(self.testVbox)
		self.show_test_result()
	#	self.msg_box(msg)
	#	self.upload_result()
#		self.clean()
	#	gtk.main_quit()
	def upload_result(self):
		status,os_ver=commands.getstatusoutput('cat /etc/linpus-subversion') 
		status,test_date=commands.getstatusoutput('date +%Y-%m-%d') 
		self.rsConfig.readfp(open(result_file), "rw")
		rsArray = self.rsConfig.items("test_result")
		status,lan_mac = commands.getstatusoutput("ifconfig |grep HWaddr|grep -v wlan|awk '{print $5}'")
		if not lan_mac:
			self.msg_box("No lan mac address found,Error,exit 1")
			exit
		sql="".join("select hw_id from hwinfo where upper(lan_mac)='%s'" % lan_mac)
		print sql
		self.con_db()
                self.cursor = self.conn.cursor()
		self.cursor.execute(sql)
		tmp = self.cursor.fetchall()
		if not tmp:
			self.msg_box("No this is machine in database")
			return
		self.hw_id=tmp[0][0]
		print self.hw_id
		
		i = 0
		sql1 = "insert into test_result ("
		sql2 = "values ("
		while i < self.allSelItem:
			strItem="".join("item_%d" % self.tcInfo[i][0])
			strItemComment="".join("item_%d_comment" % self.tcInfo[i][0])
			try:
				rsItem = self.rsConfig.get("test_result", strItem)
				rsItemComment = self.rsConfig.get("test_result", strItemComment)
			except ConfigParser.NoOptionError, e:
   				print e
				rsItem = None
				rsItemComment = None
			sql="".join("""insert into atresult (hw_id, tc_id, result, comment,os_ver, test_date)	
				values ('%s', '%s','%s','%s','%s','%s')""" \
				% (self.hw_id, self.tcInfo[i][0],rsItem,rsItemComment, os_ver,test_date))
			print sql
			self.cursor.execute(sql)
			i += 1
			
		self.conn.commit()
		self.close_db()
		self.msg_box("The test result has upload to server, the program will exit.")
		return
	def msg_box(self,msg):
		md = gtk.MessageDialog(self,
		gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
			gtk.BUTTONS_OK, 
			msg)
		md.run()
		md.destroy()
	def clean(self):
		cl_cmd="sudo sed -i '/autest.py/d' /etc/rc.d/slim/nowait.sh"
		os.system(cl_cmd)
		os.system("rm -f /tmp/.nowItem")
		os.system("rm -f /tmp/.hotkey_tip")
		cl_cmd="".join("rm -f %s"% finish_file)
		os.system(cl_cmd)
	def need_recover(self):
		status,nowItem = commands.getstatusoutput('cat /tmp/.nowItem') 
		print status, nowItem
		if status == 0:
			self.nowItem = int(nowItem)
			return True
		else:
			return False	
	def judge_show_button(self):
		print "tomm mmmmmmmmmmmmmmm 0=", self.tcInfo[self.nowItem-1][4]
		if self.tcInfo[self.nowItem-1][4] == 3:
			print "tomm mmmmmmmmmmmmmmm 1"
			print self.tcInfo[self.nowItem-1][4]
			self.next_button.hide()
			self.auto_button.show()
			self.nextFromAuto=True
		elif self.tcInfo[self.nowItem-1][4] == 2:
			print "tomm mmmmmmmmmmmmmmm 2"
			print self.tcInfo[self.nowItem-1][4]
			self.next_button.hide()
			self.auto_button.show()
			self.nextFromAuto=True
		else:
			self.next_button.show()
			print "tomm mmmmmmmmmmmmmmm 3"
			print self.tcInfo[self.nowItem-1][4]
			self.auto_button.hide() 
			self.nextFromAuto=False
		print "nowItem=",self.nowItem, "allselItem=",self.allSelItem
	#	if self.nowItem == self.allSelItem:
			#	self.next_button.set_label("Save")
	#	else:
	#		self.next_button.set_label(TEXT_NEXT)

	#when click back,show the right result
	def show_result_when_back(self):
		rsConfig = ConfigParser.ConfigParser()
		rsConfig.readfp(open(result_file), "r")
		strItem="".join("item_%d" % self.tcInfo[self.nowItem-1][0])
		strItemComment="".join("item_%d_comment" % self.tcInfo[self.nowItem-1][0])
		try:
			rsItem = rsConfig.get("test_result", strItem)
			rsItemComment = rsConfig.get("test_result", strItemComment)
		except ConfigParser.NoOptionError, e:
   			print e
			rsItem = ""
			rsItemComment = ""
			
		if rsItem == "F":
			self.radio_fail.set_active(True)	
		else:
			self.radio_pass.set_active(True)
		self.comment_buffer.set_text(rsItemComment)
	def get_kblayout(self):
		cmd="".join("%s%s" %(script_path, "machine_type.py"))
		print cmd;
		os.system(cmd)
		status,mtype = commands.getstatusoutput('cat /tmp/.machine_type.log|grep -v ^$') 
		if status == 0:
			self.mtype = mtype
		else:
			self.mtype = ""
		
	def check_user(self):
		if os.geteuid() == 0:
			self.msg_box("This is the root user. Please use the ordinary user to run this program")
			gtk.main_quit()
	def check_hk_tip(self):
		#show the hotkey tip dialog
		print str(self.tcInfo[self.nowItem-1][1]).decode('utf-8')
		print self.show_hk_tip
		if self.tcInfo[self.nowItem-1][1].find("Hotkey") != -1 and not self.show_hk_tip :
			self.show_hk_tip = True;
			cmd="".join("sh %scheckhw.sh 2>/dev/null" %(script_path))
			os.system(cmd)
			status,msg=commands.getstatusoutput('cat /tmp/.hotkey_tip')
			print status
			print  msg
			if status == 0:
				self.msg_box(msg)
		
	def show_test_result(self):
		idLabel = gtk.Label("ID")
		itemLabel = gtk.Label("Test Item")
		rsLabel = gtk.Label("Result")
		self.rsVbox = gtk.VBox()
	        self.rs_buffer = gtk.TextBuffer()
                rsScrolledWin=gtk.ScrolledWindow()
                rsTextView = gtk.TextView(self.rs_buffer)
                rsTextView.set_editable(False)
                rsTextView.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(514, 5140, 5140))
                rsTextView.set_cursor_visible(False)
                rsTextView.set_wrap_mode (gtk.WRAP_CHAR);
                rsTextView.set_size_request(300, 490)
		rsScrolledWin.add(rsTextView)
		rsScrolledWin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)

		rslist = self.get_all_result()	
		i = 0
		count = len(rslist[0])
		print "count============",count
		rsText=""
		while i < count:
			strid="".join("%-10s" % rslist[0][i])
			stritem="".join("%-80s" % rslist[1][i])
			#tmp=rsText+"".join("%-15.30s %-80.90s %20s\n" %(rslist[0][i], rslist[1][i], rslist[2][i]))	
			if str(rslist[2][i]).find("P") != -1:
				strrs="P"
			elif str(rslist[2][i]).find("F") != -1:
				strrs="Fail"
			else:
				strrs=""
			rsText = rsText + "".join("   %10s\t%5s\t\t%-80s\t\n" %(strid, strrs, stritem))
			i = i+1
	        self.rs_buffer.set_text(rsText)
		strSucc="  Congratulations!\n You have completed all the test items, the following is a summary of the test results.\n Click 'submit' to upload the result."
		succLabel = gtk.Label(strSucc)
		succLabel.set_line_wrap(True)
                #succLabel.set_wrap_mode (gtk.WRAP_CHAR);
		succLabel.modify_text(gtk.STATE_NORMAL,finish_text_color)
		fontdesc = pango.FontDescription("Purisa 10")
		succLabel.modify_font(fontdesc)
		attr = pango.AttrList()
                fg_color = pango.AttrForeground(6, 60000, 0, 0, 300)
		size = pango.AttrSize(15000, 0, 18)
		attr.insert(fg_color)
		attr.insert(size)
		succLabel.set_attributes(attr)
		succLabel.set_size_request(WIN_WIDTH-20, 60)

		hbox1 = gtk.HBox();
		hbox1.pack_start(succLabel,False,False, 5)

		hbox2 = gtk.HBox();
		hbox2.pack_start(idLabel,False,False, 20)
		hbox2.pack_start(rsLabel,False,False, 40)
		hbox2.pack_start(itemLabel,False,False, 40)
	
		hbox3 = gtk.HBox();
                submit_button = gtk.Button("Submit")
		submit_button.set_size_request(BTN_WIDTH,BTN_HEIGHT)
                submit_button.connect("clicked", self.on_submit_click)
                exit_button = gtk.Button("Exit")
		exit_button.set_size_request(BTN_WIDTH,BTN_HEIGHT)
                exit_button.connect("clicked", self.on_exit_click)
	
		self.saveCheck = gtk.CheckButton("Delete test results when exit.")
		self.saveCheck.set_active(False)

		hbox3.pack_start(submit_button,True,False, 100)
		hbox3.pack_start(exit_button,True,False, 5)
		hbox3.pack_start(self.saveCheck,True,True, 5)
		
		self.rsVbox.pack_start(hbox1, False, False, 2)
		self.rsVbox.pack_start(hbox2, False, False, 2)
		self.rsVbox.pack_start(rsScrolledWin, True, True, 5)
		self.rsVbox.pack_start(hbox3, False, False, 5)
		self.rsVbox.show_all()
		#self.remove(self.testVbox)
		self.add(self.rsVbox)
		self.show_all()

		return
	def is_complete(self):
		cmd="".join("cat %s" % finish_file)
		status,bOK=commands.getstatusoutput(cmd) 
		if status == 0 and bOK.find("Y") != -1:
			return True
		else:
			return False
		
	def on_submit_click(self,widget):
		self.upload_result()
		return	
	def on_exit_click(self, widget):
		if self.saveCheck.get_active():
			print "clean--------------dddd"
			self.clean()
		gtk.main_quit()
		
	def get_all_result(self):
		rsConfig = ConfigParser.ConfigParser()
		rsConfig.readfp(open(result_file), "r")
		rsList = [[],[],[],[]]
		i = 0
		while i < self.allSelItem:
			strItem="".join("item_%d" % self.tcInfo[i][0])
			strItemComment="".join("item_%d_comment" % self.tcInfo[i][0])
			try:
				rsItem = rsConfig.get("test_result", strItem)
				rsItemComment = rsConfig.get("test_result", strItemComment)
				rsList[0].append(self.tcInfo[i][6])
				rsList[1].append(self.tcInfo[i][7])
				rsList[2].append(rsItem)
				rsList[3].append(rsItemComment)
			except ConfigParser.NoOptionError, e:
   				print e
				rsItem = ""
				rsItemComment = ""
				rsList[0].append(self.tcInfo[i][6])
				rsList[1].append(self.tcInfo[i][7])
				rsList[2].append(rsItem)
				rsList[3].append(rsItemComment)
			i+=1	
		return rsList	
		

MainUI()
gtk.main()
