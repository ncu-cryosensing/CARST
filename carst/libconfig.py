# Class: CsvTable and ConfParams

import sys
import csv
import os
import numpy as np
import configparser
from carst.libraster import SingleRaster
from datetime import datetime
from pathlib import Path
import warnings

class CsvTable:

	"""
	Manipulating csv table which provides DEM information
	"""

	def __init__(self, fpath=None, data=[]):
		self.fpath = fpath
		self.data = data

	def get_dem(self, delimiter=','):

		"""
		Get DEMs from the contents of this csv file. Return a list of SingleRaster objects.
		"""

		dems = []
		with open(self.fpath, 'r') as csvfile:
			csvcontent = csv.reader(csvfile, skipinitialspace=True, delimiter=delimiter)
			next(csvcontent, None)    # Skip the header
			for row in csvcontent:
				dems.append(SingleRaster(*row[:3]))
		return dems

class ConfParams:

    """
    Read variables in a configuration file. The file should have the specified structure; see documentaion.
    """

    def __init__(self, fpath=None):
        self.fpath = fpath
        
    def check_fpath(self):
        """
        If self.fpath is None or does not exist, return False; otherwise return True.
        """
        if self.fpath is None:
            return False
        else:
            p = Path(self.fpath)
        if not p.exists():
            return False
        else:
            return True

    def read_params(self):

        """
        Read parameters and save them as self.xxxx
        example: if there is a section called [gdalwarp]
        and there is an option named tr = 30 30
        then self.gdalwarp['tr'] = '30 30'
        """

        if self.check_fpath():
            config = configparser.RawConfigParser()
            config.read(self.fpath)

            for section in config.sections():
                section_contents = {}
                for item in config.items(section):
                    section_contents[item[0]] = item[1]
                setattr(self, section, section_contents)

        else:
            warnings.warn('No configuration file is given. No settings are read.', UserWarning)

    def verify_path(self, pathstr):
        """
        Verify and replace a file path. (now accepting absolute and relative (to the ini file) paths)
        """
        pathobj = Path(pathstr)
        if pathobj.exists():
            return pathstr
        else:
            relative_pathobj = Path(self.fpath).parent / pathobj
            if relative_pathobj.exists():
                return str(relative_pathobj)
            else:
                raise AssertionError(f'{pathstr} or {relative_pathobj} does not exist.')

    def verify_params(self):

        """
        Verify params and modify them to proper types.
        """

        """
        Paths that need to be verified:
        demlist['csvfile']
        refgeometry['gtiff']
        xxxx -- result['picklefile']
        """
        path_categories = ['demlist', 'refgeometry'] # , 'result']
        path_arguments = ['csvfile', 'gtiff'] # , 'picklefile']
        for category, argument in zip(path_categories, path_arguments):
            if hasattr(self, category):
                category_dict = getattr(self, category)
                if argument in category_dict:
                    category_dict[argument] = self.verify_path(category_dict[argument])
                    setattr(self, category, category_dict)


        if hasattr(self, 'regression'):
            for key in self.regression:
                self.regression[key] = int(self.regression[key])
        if hasattr(self, 'pxsettings'):
            for key in self.pxsettings:
                if not self.pxsettings[key]:
                    # empty string
                    self.pxsettings[key] = None
                else:
                    self.pxsettings[key] = int(self.pxsettings[key])
            if 'size_across' not in self.pxsettings:
                self.pxsettings['size_across'] = None
            if 'size_down' not in self.pxsettings:
                self.pxsettings['size_down'] = None
            if 'gaussian_hp' in self.pxsettings:
                self.pxsettings['gaussian_hp'] = bool(int(self.pxsettings['gaussian_hp']))
            else:
                self.pxsettings['gaussian_hp'] = True
            if 'gaussian_hp_sigma' in self.pxsettings:
                self.pxsettings['gaussian_hp_sigma'] = float(self.pxsettings['gaussian_hp_sigma'])
            else:
                self.pxsettings['gaussian_hp_sigma'] = 3.0

        if hasattr(self, 'outputcontrol'):
            if 'datepair_prefix' in self.outputcontrol:
                if self.outputcontrol['datepair_prefix'] in ['false', 'f', 'no', 'n', '0']:
                    self.outputcontrol['if_generate_xyztext'] = False
                else:
                    self.outputcontrol['datepair_prefix'] = bool(int(self.outputcontrol['datepair_prefix']))
                    atime = datetime.strptime(self.imagepair['image1_date'], '%Y-%m-%d')
                    btime = datetime.strptime(self.imagepair['image2_date'], '%Y-%m-%d')
                    self.outputcontrol['label_datepair'] = atime.strftime('%Y%m%d') + '-' + btime.strftime('%Y%m%d' + '_')
            if 'output_folder' not in self.outputcontrol:
                self.outputcontrol['output_folder'] = '.'
        if hasattr(self, 'rawoutput'):
            if 'if_generate_xyztext' in self.rawoutput:
                self.rawoutput['if_generate_xyztext'] = bool(int(self.rawoutput['if_generate_xyztext']))
            else:
                self.rawoutput['if_generate_xyztext'] = False
            if 'if_generate_ampofftxt' in self.rawoutput:
                self.rawoutput['if_generate_ampofftxt'] = bool(int(self.rawoutput['if_generate_ampofftxt']))
            else:
                self.rawoutput['if_generate_ampofftxt'] = False
            if 'label_ampcor' in self.rawoutput:
                if self.outputcontrol['datepair_prefix'] not in ['false', 'f', 'no', 'n', '0']:
                    self.rawoutput['label_ampcor'] = os.path.join(self.outputcontrol['output_folder'], self.outputcontrol['label_datepair'] + self.rawoutput['label_ampcor'])
                else:
                    self.rawoutput['label_ampcor'] = os.path.join(self.outputcontrol['output_folder'], self.rawoutput['label_ampcor'])
            if 'label_geotiff' in self.rawoutput:
                if self.outputcontrol['datepair_prefix'] not in ['false', 'f', 'no', 'n', '0']:
                    self.rawoutput['label_geotiff'] = os.path.join(self.outputcontrol['output_folder'], self.outputcontrol['label_datepair'] + self.rawoutput['label_geotiff'])
                else:
                    self.rawoutput['label_geotiff'] = os.path.join(self.outputcontrol['output_folder'], self.rawoutput['label_geotiff'])
        if hasattr(self, 'velocorrection'):
            if 'label_bedrock_histogram' in self.velocorrection:
                if self.outputcontrol['datepair_prefix'] not in ['false', 'f', 'no', 'n', '0']:
                    self.velocorrection['label_bedrock_histogram'] = os.path.join(self.outputcontrol['output_folder'], self.outputcontrol['label_datepair'] + self.velocorrection['label_bedrock_histogram'])
                else:
                    self.velocorrection['label_bedrock_histogram'] = os.path.join(self.outputcontrol['output_folder'], self.velocorrection['label_bedrock_histogram'])
            if 'label_geotiff' in self.velocorrection:
                if self.outputcontrol['datepair_prefix'] not in ['false', 'f', 'no', 'n', '0']:
                    self.velocorrection['label_geotiff'] = os.path.join(self.outputcontrol['output_folder'], self.outputcontrol['label_datepair'] + self.velocorrection['label_geotiff'])
                else:
                    self.velocorrection['label_geotiff'] = os.path.join(self.outputcontrol['output_folder'], self.velocorrection['label_geotiff'])
            if 'label_logfile' in self.velocorrection:
                if self.outputcontrol['datepair_prefix'] not in ['false', 'f', 'no', 'n', '0']:
                    self.velocorrection['label_logfile'] = os.path.join(self.outputcontrol['output_folder'], self.outputcontrol['label_datepair'] + self.velocorrection['label_logfile'])
                else:
                    self.velocorrection['label_logfile'] = os.path.join(self.outputcontrol['output_folder'], self.velocorrection['label_logfile'])
            if 'refvelo_outlier_sigma' in self.velocorrection:
                self.velocorrection['refvelo_outlier_sigma'] = float(self.velocorrection['refvelo_outlier_sigma'])
            else:
                self.velocorrection['refvelo_outlier_sigma'] = 3.0
        if hasattr(self, 'noiseremoval'):
            for key in self.noiseremoval:
                self.noiseremoval[key] = float(self.noiseremoval[key])

    def get_dem(self):

        """
        Get DEMs from "csvfile" field. Return a list of SingleRaster objects.
        """

        if hasattr(self, 'demlist') and 'csvfile' in self.demlist:
            csv = CsvTable(self.demlist['csvfile'])
            return csv.get_dem()
        else:
            print('Warning: No DEM-list file is given. Nothing will run.')
            return []