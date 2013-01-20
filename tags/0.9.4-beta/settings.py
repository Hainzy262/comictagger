"""
Settings class for comictagger app
"""

"""
Copyright 2012  Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#import sys
import os
import sys
import ConfigParser
import platform

import utils

class ComicTaggerSettings:

	@staticmethod
	def getSettingsFolder():
		if platform.system() == "Windows":
			return os.path.join( os.environ['APPDATA'], 'ComicTagger' )
		else:
			return os.path.join( os.path.expanduser('~') , '.ComicTagger')

	@staticmethod
	def baseDir():
		if platform.system() == "Darwin" and getattr(sys, 'frozen', None):
			return sys._MEIPASS
		else:
			#print "ATB basename", os.path.dirname( os.path.abspath( sys.argv[0] ) )
			return os.path.dirname( os.path.abspath( sys.argv[0] ) )
		
	def setDefaultValues( self ):

		# General Settings
		self.rar_exe_path = ""
		self.unrar_exe_path = ""
		self.allow_cbi_in_rar = True
		
		# automatic settings
		self.last_selected_data_style = 0
		self.last_opened_folder = ""
		self.last_main_window_width = 0
		self.last_main_window_height = 0
		self.last_main_window_x = 0
		self.last_main_window_y = 0
		
		# identifier settings
		self.id_length_delta_thresh = 5
		self.id_publisher_blacklist = "Panini Comics, Abril, Scholastic Book Services"
		
		# Show/ask dialog flags
		self.ask_about_cbi_in_rar = True
		self.show_disclaimer = True
		
		# Comic Vine settings
		self.use_series_start_as_volume = False
		
		# CBL Tranform settings
		
		self.assume_lone_credit_is_primary = False
		self.copy_characters_to_tags = False
		self.copy_teams_to_tags = False
		self.copy_locations_to_tags = False
		self.copy_notes_to_comments = False
		self.copy_weblink_to_comments = False
		self.apply_cbl_transform_on_cv_import = False
		self.apply_cbl_transform_on_bulk_operation = False

		# Rename settings
		self.rename_template = "%series% #%issue% (%year%)"
		self.rename_issue_number_padding = 3
		self.rename_use_smart_string_cleanup = True
		

	def __init__(self):
		
		self.settings_file = ""
		self.folder = ""
		self.setDefaultValues()

		self.config = ConfigParser.RawConfigParser()
		self.folder = ComicTaggerSettings.getSettingsFolder()
		
		if not os.path.exists( self.folder ):
			os.makedirs( self.folder )
		
		self.settings_file = os.path.join( self.folder, "settings")
		
		# if config file doesn't exist, write one out
		if not os.path.exists( self.settings_file ):
			self.save()
		else:
			self.load()
		
		# take a crack at finding rar exes, if not set already
		if self.rar_exe_path == "":
			if platform.system() == "Windows":
				# look in some likely places for windows machine
				if os.path.exists( "C:\Program Files\WinRAR\Rar.exe" ):
					self.rar_exe_path = "C:\Program Files\WinRAR\Rar.exe"
				elif os.path.exists( "C:\Program Files (x86)\WinRAR\Rar.exe" ):
					self.rar_exe_path = "C:\Program Files (x86)\WinRAR\Rar.exe"
			else:
				# see if it's in the path of unix user
				if utils.which("rar") is not None:
					self.rar_exe_path = utils.which("rar")
			if self.rar_exe_path != "":
				self.save()
					
		if self.unrar_exe_path == "":
			if platform.system() != "Windows":
				# see if it's in the path of unix user
				if utils.which("unrar") is not None:
					self.unrar_exe_path = utils.which("unrar")
			if self.unrar_exe_path != "":
				self.save()

	def reset( self ):
		os.unlink( self.settings_file )
		self.__init__()
		
	def load(self):
		
		self.config.read( self.settings_file )
		
		self.rar_exe_path =    self.config.get( 'settings', 'rar_exe_path' )
		self.unrar_exe_path =  self.config.get( 'settings', 'unrar_exe_path' )
    
		if self.config.has_option('auto', 'last_selected_data_style'):
			self.last_selected_data_style =  self.config.getint( 'auto', 'last_selected_data_style' )
		if self.config.has_option('auto', 'last_opened_folder'):
			self.last_opened_folder =        self.config.get( 'auto', 'last_opened_folder' )
		if self.config.has_option('auto', 'last_main_window_width'):
			self.last_main_window_width =    self.config.getint( 'auto', 'last_main_window_width' )
		if self.config.has_option('auto', 'last_main_window_height'):
			self.last_main_window_height =   self.config.getint( 'auto', 'last_main_window_height' )
		if self.config.has_option('auto', 'last_main_window_x'):
			self.last_main_window_x =   self.config.getint( 'auto', 'last_main_window_x' )
		if self.config.has_option('auto', 'last_main_window_y'):
			self.last_main_window_y =   self.config.getint( 'auto', 'last_main_window_y' )

		if self.config.has_option('identifier', 'id_length_delta_thresh'):
			self.id_length_delta_thresh =   self.config.getint( 'identifier', 'id_length_delta_thresh' )
		if self.config.has_option('identifier', 'id_publisher_blacklist'):
			self.id_publisher_blacklist =   self.config.get( 'identifier', 'id_publisher_blacklist' )

		if self.config.has_option('dialogflags', 'ask_about_cbi_in_rar'):
			self.ask_about_cbi_in_rar =        self.config.getboolean( 'dialogflags', 'ask_about_cbi_in_rar' )		
		if self.config.has_option('dialogflags', 'show_disclaimer'):
			self.show_disclaimer =        self.config.getboolean( 'dialogflags', 'show_disclaimer' )
			
		if self.config.has_option('comicvine', 'use_series_start_as_volume'):
			self.use_series_start_as_volume =        self.config.getboolean( 'comicvine', 'use_series_start_as_volume' )		

		if self.config.has_option('cbl_transform', 'assume_lone_credit_is_primary'):
			self.assume_lone_credit_is_primary =         self.config.getboolean( 'cbl_transform', 'assume_lone_credit_is_primary' )		
		if self.config.has_option('cbl_transform', 'copy_characters_to_tags'):
			self.copy_characters_to_tags =               self.config.getboolean( 'cbl_transform', 'copy_characters_to_tags' )		
		if self.config.has_option('cbl_transform', 'copy_teams_to_tags'):
			self.copy_teams_to_tags =                    self.config.getboolean( 'cbl_transform', 'copy_teams_to_tags' )		
		if self.config.has_option('cbl_transform', 'copy_locations_to_tags'):
			self.copy_locations_to_tags =                self.config.getboolean( 'cbl_transform', 'copy_locations_to_tags' )		
		if self.config.has_option('cbl_transform', 'copy_notes_to_comments'):
			self.copy_notes_to_comments =                self.config.getboolean( 'cbl_transform', 'copy_notes_to_comments' )		
		if self.config.has_option('cbl_transform', 'copy_weblink_to_comments'):
			self.copy_weblink_to_comments =              self.config.getboolean( 'cbl_transform', 'copy_weblink_to_comments' )		
		if self.config.has_option('cbl_transform', 'apply_cbl_transform_on_cv_import'):
			self.apply_cbl_transform_on_cv_import =      self.config.getboolean( 'cbl_transform', 'apply_cbl_transform_on_cv_import' )		
		if self.config.has_option('cbl_transform', 'apply_cbl_transform_on_bulk_operation'):
			self.apply_cbl_transform_on_bulk_operation = self.config.getboolean( 'cbl_transform', 'apply_cbl_transform_on_bulk_operation' )		
			
		if self.config.has_option('rename', 'rename_template'):
			self.rename_template =                  self.config.get( 'rename', 'rename_template' )		
		if self.config.has_option('rename', 'rename_issue_number_padding'):
			self.rename_issue_number_padding =      self.config.getint( 'rename', 'rename_issue_number_padding' )		
		if self.config.has_option('rename', 'rename_use_smart_string_cleanup'):
			self.rename_use_smart_string_cleanup =  self.config.getboolean( 'rename', 'rename_use_smart_string_cleanup' )		
			

	def save( self ):

		if not self.config.has_section( 'settings' ):
			self.config.add_section( 'settings' )
			
		self.config.set( 'settings', 'rar_exe_path',   self.rar_exe_path )
		self.config.set( 'settings', 'unrar_exe_path', self.unrar_exe_path )

		if not self.config.has_section( 'auto' ):
			self.config.add_section( 'auto' )

		self.config.set( 'auto', 'last_selected_data_style', self.last_selected_data_style )
		self.config.set( 'auto', 'last_opened_folder', self.last_opened_folder )
		self.config.set( 'auto', 'last_main_window_width', self.last_main_window_width )
		self.config.set( 'auto', 'last_main_window_height', self.last_main_window_height )
		self.config.set( 'auto', 'last_main_window_x', self.last_main_window_x )
		self.config.set( 'auto', 'last_main_window_y', self.last_main_window_y )

		if not self.config.has_section( 'identifier' ):
			self.config.add_section( 'identifier' )

		self.config.set( 'identifier', 'id_length_delta_thresh', self.id_length_delta_thresh )
		self.config.set( 'identifier', 'id_publisher_blacklist', self.id_publisher_blacklist )

		if not self.config.has_section( 'dialogflags' ):
			self.config.add_section( 'dialogflags' )

		self.config.set( 'dialogflags', 'ask_about_cbi_in_rar', self.ask_about_cbi_in_rar )
		self.config.set( 'dialogflags', 'show_disclaimer', self.show_disclaimer )

		if not self.config.has_section( 'comicvine' ):
			self.config.add_section( 'comicvine' )
			
		self.config.set( 'comicvine', 'use_series_start_as_volume', self.use_series_start_as_volume )

		if not self.config.has_section( 'cbl_transform' ):
			self.config.add_section( 'cbl_transform' )

		self.config.set( 'cbl_transform', 'assume_lone_credit_is_primary', self.assume_lone_credit_is_primary )
		self.config.set( 'cbl_transform', 'copy_characters_to_tags', self.copy_characters_to_tags )
		self.config.set( 'cbl_transform', 'copy_teams_to_tags', self.copy_teams_to_tags )
		self.config.set( 'cbl_transform', 'copy_locations_to_tags', self.copy_locations_to_tags )
		self.config.set( 'cbl_transform', 'copy_notes_to_comments', self.copy_notes_to_comments )
		self.config.set( 'cbl_transform', 'copy_weblink_to_comments', self.copy_weblink_to_comments )
		self.config.set( 'cbl_transform', 'apply_cbl_transform_on_cv_import', self.apply_cbl_transform_on_cv_import )
		self.config.set( 'cbl_transform', 'apply_cbl_transform_on_bulk_operation', self.apply_cbl_transform_on_bulk_operation )

		if not self.config.has_section( 'rename' ):
			self.config.add_section( 'rename' )

		self.config.set( 'rename', 'rename_template', self.rename_template )
		self.config.set( 'rename', 'rename_issue_number_padding', self.rename_issue_number_padding )
		self.config.set( 'rename', 'rename_use_smart_string_cleanup', self.rename_use_smart_string_cleanup )
		
		with open( self.settings_file, 'wb') as configfile:
			self.config.write(configfile)    
