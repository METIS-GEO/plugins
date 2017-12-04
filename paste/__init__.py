# -*- coding: utf-8 -*-
"""
/***************************************************************************
 coller
                                 A QGIS plugin
 Paste selected vetors to vector layer
                             -------------------
        begin                : 2017-12-01
        copyright            : (C) 2017 by gbruel/metis
        email                : g.bruel@metis-reseaux.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load coller class from file coller.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .coller import coller
    return coller(iface)
