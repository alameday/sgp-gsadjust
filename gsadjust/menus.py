#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
menus.py
===============

Menus for GSadjust
--------------------------------------------------------------------------------------------------------------------

This software is preliminary, provisional, and is subject to revision. It is being provided to meet the need for
timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related
material nor shall the fact of release constitute any such warranty. The software is provided on the condition that
neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or
unauthorized use of the software.
"""
from PyQt5 import QtWidgets, QtGui

import gsa_plots
from gui_objects import AboutDialog


class Menus:
    def __init__(self, mainProg):
        self.mainProg = mainProg
        """
        Menu creation
        """
        #######################################################################
        # File Menu:
        #######################################################################
        self.mnFile = self.mainProg.menuBar().addMenu("&File")
        # for file opening
        self.mnFileOpenScintrexFile = self.create_action("&Load raw CG-3/CG-5 data...",
                                              shortcut="Ctrl+o",
                                              slot=lambda meter='Scintrex':
                                              self.mainProg.open_file_dialog('Scintrex'),
                                              tip="Open data file",
                                              enabled=True)
        self.mnFileOpenBurrisFile = self.create_action("Load raw &Burris data...",
                                              shortcut="Ctrl+b",
                                              slot=lambda meter='Burris':
                                              self.mainProg.open_file_dialog('Burris'),
                                              tip="Open data file",
                                              enabled=True)
        self.mnFileOpenCG6File = self.create_action("Load raw CG-6 data...",
                                              shortcut="Ctrl+6",
                                              slot=lambda meter='CG6': self.mainProg.open_file_dialog('CG6'),
                                              tip="Open data file",
                                              enabled=True)
        self.mnFileOpenCG6FileTsoft = self.create_action("Load raw CG-6 data (Tsoft format)...",
                                              slot=lambda meter='CG6Tsoft': self.mainProg.open_file_dialog('CG6Tsoft'),
                                              tip="Open data file",
                                              enabled=True)
        self.mnFileOpenCsvFile = self.create_action("Import csv data...",
                                              shortcut="Ctrl+7",
                                              slot=lambda meter='csv': self.mainProg.open_file_dialog('csv'),
                                              tip="Open comma-separated value data file",
                                              enabled=True)
        self.mnFileAppendSurvey = self.create_action("Append survey to campaign...",
                                              slot=lambda meter='choose': self.mainProg.open_file_dialog('choose'),
                                              enabled=False)
        self.mnFileAppendLoop = self.create_action("Append loop to current survey...",
                                              slot=lambda meter='choose':
                                              self.mainProg.open_file_dialog('chooseloop'),
                                              enabled=False)
        self.mnFileAppendWorkspace = self.create_action("Append workspace...",
                                              slot=self.mainProg.workspace_append,
                                              enabled=False)
        self.mnFileClearWorkspace = self.create_action("Clear workspace",
                                              slot=self.mainProg.workspace_clear,
                                              enabled=True)
        self.mnFileSaveWorkspace = self.create_action("Save workspace",
                                              shortcut="Ctrl+s",
                                              slot=self.mainProg.workspace_save,
                                              enabled=False)
        self.mnFileSaveWorkspaceAs = self.create_action("Save workspace as...",
                                              shortcut="F12",
                                              slot=self.mainProg.workspace_save_as,
                                              enabled=False)
        self.mnFileLoadWorkspaceAction = self.create_action("Open workspace (.p format)...",
                                              slot=self.mainProg.workspace_open_getfile)
        self.mnFileLoadJSONAction = self.create_action("Open workspace...",
                                              slot=self.mainProg.workspace_open_getjson)
        self.mnFileExitAction = self.create_action("&Exit",
                                              shortcut="Alt+F4",
                                              slot=self.mainProg.close,
                                              tip="Exit App")

        # add actions to menu
        self.add_actions(self.mnFile, (self.mnFileOpenScintrexFile,
                                       self.mnFileOpenCG6File,
                                       self.mnFileOpenCG6FileTsoft,
                                       self.mnFileOpenBurrisFile,
                                       self.mnFileOpenCsvFile,
                                       None,
                                       self.mnFileAppendSurvey,
                                       self.mnFileAppendLoop,
                                       self.mnFileAppendWorkspace,
                                       None,
                                       self.mnFileSaveWorkspace,
                                       self.mnFileSaveWorkspaceAs,
                                       self.mnFileLoadJSONAction,
                                       self.mnFileLoadWorkspaceAction,
                                       self.mnFileClearWorkspace,
                                       None,
                                       self.mnFileExitAction))

        #######################################################################
        # Process Menu:
        #######################################################################
        self.mnEdit = self.mainProg.menuBar().addMenu("&Edit")
        self.mnEditTideCorrection = self.create_action("&Tide correction...",
                                                       shortcut="Ctrl+T", slot=self.mainProg.dialog_tide_correction,
                                                       tip="Choose tide correction method", enabled=False)
        self.mnEditOceanLoadingCorrectionAction = self.create_action("&Ocean loading correction",
                                              shortcut="Ctrl+L",
                                              slot=self.mainProg.correction_ocean_loading,
                                              tip="Ocean loading corrections", enabled=False)
        self.mnEditAtmosphericCorrectionAction = self.create_action("&Atmospheric correction",
                                              shortcut="Ctrl+P",
                                              slot=self.mainProg.correction_atmospheric,
                                              tip="Apply atmospheric correction by loading a data file",
                                              enabled=False)
        self.mnEditShowCoordinates = self.create_action("Show station coordinates...",
                                                        slot=self.mainProg.dialog_station_coordinates,
                                                        enabled=False)
        self.mnEditLoadCoordinates = self.create_action("Load station coordinates",
                                              slot=self.mainProg.load_station_coordinates,
                                              enabled=False)
        self.mnEditCorrectRecordedTimeAction = self.create_action("&Correct recorded time...",
                                                                  slot=self.mainProg.correct_recorded_time,
                                                                  tip="Correct recorded time", enabled=False)
        self.mnEditVerticalGradientIntervalAction = self.create_action("&Vertical gradient interval...",
                                              slot=self.mainProg.set_vertical_gradient_interval,
                                              enabled=True)
        self.mnEditVerticalGradientWriteAction = self.create_action("Write vertical gradient file...",
                                              slot=self.mainProg.vertical_gradient_write,
                                              enabled=True)
        self.mnEditAddTareDialog = self.create_action("Add tare...",
                                              slot=self.mainProg.add_tare,
                                              enabled=True)
        self.mnEditLoops = self.create_action("Divide selected loop...",
                                              slot=self.mainProg.get_loop_threshold,
                                              enabled=True)
        # add actions to menu
        self.add_actions(self.mnEdit,
                         (self.mnEditTideCorrection,
                          self.mnEditCorrectRecordedTimeAction,
                          None,
                          self.mnEditShowCoordinates,
                          #self.mnEditLoadCoordinates,
                          None,
                          self.mnEditLoops,
                          self.mnEditAddTareDialog,
                          None,
                          self.mnEditVerticalGradientIntervalAction,
                          self.mnEditVerticalGradientWriteAction))

        #######################################################################
        # Adjust Menu
        #######################################################################
        self.mnAdj = self.mainProg.menuBar().addMenu("&Adjustment")
        self.mnAdjtype = self.mnAdj.addMenu('Adjustment type')
        actiongroup_adjustmenttype = QtWidgets.QActionGroup(self.mainProg, exclusive=True)

        self.mnAdjPyLSQ = actiongroup_adjustmenttype.addAction(self.create_action('Numpy least squares', checkable=True))
        self.mnAdjtype.addAction(self.mnAdjPyLSQ)
        self.mnAdjGravnet = actiongroup_adjustmenttype.addAction(self.create_action('Gravnet', checkable=True))
        self.mnAdjtype.addAction(self.mnAdjGravnet)
        self.mnAdjPyLSQ.setChecked(True)

        self.mnAdjOptions = self.create_action("Adjustment options...",
                                               slot=self.mainProg.dialog_adjustment_properties,
                                               enabled=True)
        self.mnAdjAdjustCurrent = self.create_action("&Adjust current survey",
                                              shortcut="Ctrl+2", slot=lambda: self.mainProg.adjust_network('current'),
                                              tip="Adjust current survey", enabled=False,
                                              icon=QtGui.QIcon('./gsadjust/resources/ac.png'))
        self.mnAdjAdjust = self.create_action("&Adjust all surveys",
                                              shortcut="Ctrl+1", slot=lambda:self.mainProg.adjust_network('all'),
                                              tip="Adjust all surveys", enabled=False,
                                              icon=QtGui.QIcon('./gsadjust/resources/aa.png'))
        self.mnAdjUpdateDeltas = self.create_action("&Populate delta table - all surveys",
                                              shortcut="Ctrl+A",
                                              slot=lambda: self.mainProg.populate_deltamodel('all'),
                                              enabled=False)
        self.mnAdjUpdateDeltasCurrentSurvey = self.create_action("Populate delta table - selected survey",
                                              slot=lambda:
                                              self.mainProg.populate_deltamodel('selectedsurvey'),
                                              enabled=False)
        self.mnAdjUpdateDeltasCurrentLoop = self.create_action("Populate delta table - selected loop(s)",
                                              slot=lambda:
                                              self.mainProg.populate_deltamodel('selectedloop'),
                                              enabled=False)
        self.mnAdjClearDeltaTable = self.create_action("Clear delta table",
                                              slot=self.mainProg.clear_delta_model,
                                              enabled=False)
        self.mnAdjAdd = self.create_action("Add datum observation...",
                                           shortcut="Ctrl+D",
                                           slot=self.mainProg.dialog_add_datum,
                                           enabled=True)
        self.mnAdjImportAbsSimple = self.create_action("Import abs. g (simple)...",
                                                       slot=self.mainProg.menu_import_abs_g_simple,
                                                       enabled=True)
        self.mnAdjImportAbsFull = self.create_action("Import abs. g (complete)...",
                                                     slot=self.mainProg.menu_import_abs_g_complete,
                                                     enabled=True)
        self.mnAdjImportAbsDatabase = self.create_action("Import abs. g from project files...",
                                                         slot=self.mainProg.dialog_import_abs_g_direct,
                                                         enabled=True)
        self.mnAdjClearDatumTable = self.create_action("Clear datum table",
                                              slot=self.mainProg.clear_datum_model,
                                              enabled=False)

        self.mnAdjPlotHist = self.create_action("Plot residual histogram",
                                              shortcut="Ctrl+H", slot=mainProg.plot_histogram,
                                              enabled=True)
        self.mnAdjPlotCompareDatum = self.create_action("Plot adjusted datum vs. measured",
                                              slot=self.mainProg.plot_datum_vs_adjusted,
                                              enabled=False)
        self.mnAdjPlotObservedAdjustedAbs = self.create_action("Plot adjusted datum vs. measured (time series)",
                                              slot=gsa_plots.plot_datum_comparison_timeseries,
                                              enabled=False)
        # self.mnAdjCompareAllDatum = self.create_action("Plot absolute vs. relative offset",
        #                                                slot=self.mainProg.plot_compare_datum_all,
        #                                                enabled=True)

        self.add_actions(self.mnAdj, (self.mnAdjOptions,
                                      self.mnAdjAdjustCurrent,
                                      self.mnAdjAdjust,
                                      None,
                                      self.mnAdjUpdateDeltas,
                                      self.mnAdjUpdateDeltasCurrentSurvey,
                                      self.mnAdjUpdateDeltasCurrentLoop,
                                      self.mnAdjClearDeltaTable,
                                      None,
                                      self.mnAdjAdd,
                                      self.mnAdjImportAbsSimple,
                                      self.mnAdjImportAbsFull,
                                      self.mnAdjImportAbsDatabase,
                                      self.mnAdjClearDatumTable,
                                      None,
                                      self.mnAdjPlotHist,
                                      self.mnAdjPlotCompareDatum,
                                      self.mnAdjPlotObservedAdjustedAbs,
                                      ))

        #######################################################################
        # Tools Menu
        #######################################################################
        self.mnTools = self.mainProg.menuBar().addMenu('&Tools')
        self.mnToolsNGCircular = self.create_action('Network graph - circular',
                                              slot=self.mainProg.plot_network_graph_circular)
        self.mnToolsNGMap = self.create_action('Network graph - map view',
                                              slot=self.mainProg.plot_network_graph_map)
        self.mnToolsWriteMetadataText = self.create_action('Write metadata text',
                                              slot=self.mainProg.write_metadata_text)
        self.mnToolsWriteTabularOutput = self.create_action('Write tabular data',
                                              slot=self.mainProg.write_tabular_data)
        self.mnToolsWriteSummary = self.create_action('Write adjustment summary',
                                              slot=self.mainProg.write_summary_text)
        self.mnToolsComputeGravityChangeAction = self.create_action("&Compute gravity change",
                                              slot=self.mainProg.show_gravity_change_table,
                                              tip="Compute gravity change", enabled=False)
        self.mnToolsLOO = self.create_action("Adjusted vs. observed datum...",
                                              slot=self.mainProg.adjusted_vs_observed_datum_analysis,
                                              enabled=False)

        self.add_actions(self.mnTools, (self.mnToolsNGCircular,
                                        self.mnToolsNGMap,
                                        None,
                                        self.mnToolsComputeGravityChangeAction,
                                        # self.mnToolsLOO,
                                        None,
                                        self.mnToolsWriteMetadataText,
                                        self.mnToolsWriteTabularOutput,
                                        self.mnToolsWriteSummary))

        #######################################################################
        # Help Menu
        #######################################################################
        self.mnHelp = self.mainProg.menuBar().addMenu('&Help')
        self.mnHelpHelp = self.create_action('Help',
                                              slot=self.mainProg.show_help)
        self.mnHelpAbout = self.create_action('About',
                                              slot=AboutDialog)
        self.mnHelpCheckForUpdates = self.create_action('Check for updates...',
                                              slot=self.mainProg.check_for_updates)

        self.add_actions(self.mnHelp, (self.mnHelpHelp,
                                       self.mnHelpAbout,
                                       None,
                                       self.mnHelpCheckForUpdates))

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False,
                      signal="triggered()", enabled=True):
        """
        Simplify action creation
        """
        action = QtWidgets.QAction(text, self.mainProg)
        if icon is not None:
            action.setIcon(icon)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        if enabled is not True:
            action.setEnabled(False)
        return action

    def add_actions(self, target, actions):
        """
        Add actions to a target
        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
