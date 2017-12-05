# -*- coding: utf-8 -*-
# coding: utf8
"""
/***************************************************************************
 coller
                                 A QGIS plugin
 Paste selected vetors to vector layer
                              -------------------
        begin                : 2017-12-01
        git sha              : $Format:%H$
        copyright            : (C) 2017 by gbruel/metis
        email                : g.bruel@metis-reseaux.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from coller_dialog import collerDialog
import os.path

class coller:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'coller_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&coller')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'coller')
        self.toolbar.setObjectName(u'coller')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('coller', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = collerDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/coller/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Coller'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&coller'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def getLayerFromCombo(self, boolean):
        """Active or deactive layer edit mode and active layer as current to realize qgis actions."""
        layer = False
        layers = self.iface.legendInterface().layers();
        for item in layers:
            if item.name() == self.dlg.comboBox.currentText():
                self.iface.legendInterface().setCurrentLayer(item)
                layer = item
                if boolean :
                    layer.startEditing()
        return layer

    def getComboSelection(self):
        """Action fire when user click on combobox value to display message or set layer edition mode."""
        # -- get selected object        
        idx = self.dlg.comboBox.currentIndex()        
        layers = self.iface.legendInterface().layers();
        layer = layers[idx-1]
        currLayer = self.iface.activeLayer()
        features = currLayer.selectedFeatures() # get features to paste        
        countFeatures = len(features)
        return self.getLayerFromCombo(True)        
        

    # This method will be called when you click the toolbar button or select the plugin menu item
    def run(self):
        """Run method that performs all the real work."""            
        layer_list = ["Select layers..."]
        self.dlg.comboBox.clear()
        layers = self.iface.legendInterface().layers()
        nativeLayer = self.iface.activeLayer() # get current active layer
        for layer in layers: # load combo box values        
            if layer.name() != self.iface.activeLayer().name() and layer.type() == 0:               
                 layer_list.append(layer.name())
        self.dlg.comboBox.addItems(layer_list)
        # params layer / liste [layerName]
        self.dlg.comboBox.currentIndexChanged.connect(self.getComboSelection) # set event when user click on combo value        
        self.iface.legendInterface().setCurrentLayer(nativeLayer)        
        self.iface.actionCopyFeatures().trigger() # copy features from current active layer
        features = nativeLayer.selectedFeatures()
        if len(features) > 0:
            nbFeatures = str(len(features))
            text = nbFeatures+u" objets sélectionnés";            
            self.dlg.textEdit.setText(text)
        # show the dialog
        self.dlg.show()        
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            """Merge selected features to selected layer and save modifications."""
            self.iface.actionPasteFeatures().trigger()
            self.iface.mainWindow().findChild(QAction, 'mActionMergeFeatures').trigger()
            # commit edition to layer
            layerChange = self.getLayerFromCombo(False)
            layerChange.commitChanges()            
            if nativeLayer:
                self.iface.legendInterface().setCurrentLayer(nativeLayer)  
            pass
        self.dlg.close()
