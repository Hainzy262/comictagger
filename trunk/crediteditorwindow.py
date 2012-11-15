"""
A PyQT4 dialog to edit credits
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


from PyQt4 import QtCore, QtGui, uic
from settings import ComicTaggerSettings
import os

class CreditEditorWindow(QtGui.QDialog):
	
	
	ModeEdit = 0
	ModeNew = 1
	
	
	def __init__(self, parent, mode, role, name ):
		super(CreditEditorWindow, self).__init__(parent)
		
		uic.loadUi(os.path.join(ComicTaggerSettings.baseDir(), 'crediteditorwindow.ui' ), self)
		
		self.mode = mode
		
		if self.mode == self.ModeEdit:
			self.setWindowTitle("Edit Credit")
		else: 
			self.setWindowTitle("New Credit")

		# Add the entries to the role combobox
		self.cbRole.addItem( "" )
		self.cbRole.addItem( "Writer" )
		self.cbRole.addItem( "Artist" )
		self.cbRole.addItem( "Penciller" )
		self.cbRole.addItem( "Inker" )
		self.cbRole.addItem( "Colorist" )
		self.cbRole.addItem( "Letterer" )
		self.cbRole.addItem( "Cover Artist" )
		self.cbRole.addItem( "Editor" )
		self.cbRole.addItem( "Other" )
		self.cbRole.addItem( "Plotter" )
		self.cbRole.addItem( "Scripter" )
		
		self.leName.setText( name )
		
		if role is not None and role != "":
			i = self.cbRole.findText( role )
			if i == -1:
				self.cbRole.setEditText( role  )
			else:	
				self.cbRole.setCurrentIndex( i )
				
	def getCredits( self ):
		return self.cbRole.currentText(), self.leName.text()
			

	def accept( self ):
		if self.cbRole.currentText() == "" or self.leName.text() == "":
			QtGui.QMessageBox.warning(self, self.tr("Whoops"), self.tr("You need to enter both role and name for a credit."))
		else:
			QtGui.QDialog.accept(self)