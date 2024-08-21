'''	main.py
	author: FrankenMullet
	
	CLI interface for performing functions on loaded CSV files '''


import argparse
from argparse import ArgumentParser
from categories import categories
from os import listdir
import colorama as clr


class Main:
	def __init__(self):
		'''Called Immediately when class instance is called
			... entails the high-level work flow of the class' functionality '''
		
		#Set Default Variables
		self.directory = "./"
		self.delimiter = ","
		
		#Data Repository
		#Keys: <str> filename | values: <list<list>> file contents by line
		self.files = {}
		
		#Router for calling functions from operations specified in termial
		self.router_build()
		
		#Get CLI arguments
		self.parser = self.build_parser()
		args = self.parser.parse_args()
		
		#Process CLI args
		if args.directory:
			self.directory = args.directory[0]		#changes search directory
		
		if args.delimiter:
			self.delimiter = args.delimiter[0]		#changes delimiter
		
		#If specific files specified
		if args.files:
			self.load_files(args.files)				#load specified files
			self.run_operations(args.operation)		#runs operations
		
		#Otherwise, processes ALL csvs in directory
		elif ".csv" in ",".join(listdir(self.directory)):
			files = [ f for f in listdir(self.directory) if '.csv' in f ]
			self.load_files(files)
			if files != []:
				self.run_operations(args.operation)		
			else:
				self.error("No files provided")
		else:
			self.error("No CSVs in specified Directory")
				
				
				
	def build_parser(self):
		'''Setting up the Command-Line Interface'''
		description = '''Tool to graph and organize bank statement CSVs'''
		parser = ArgumentParser(description=description)
		
		#To specify desired folder to search in [OPTIONAL]
		parser.add_argument('-d', '--directory',
							type=str, nargs = 1,
							help = 'Target directory for specified files. defaults to current working directory "./" .')	
		#To specify desired files to load [OPTIONAL]
		parser.add_argument('-f', '--files',
							type=str, nargs = '+',
							help = 'If user desires only specific files to be processed. Otherwise, all CSVs in the given directory will be processed. ')				
		#To specify desired delimiter to parse CSV [OPTIONAL]
		parser.add_argument('-D', '--delimiter',
							type=str, nargs = 1,
							help = 'Changes the delimter for parsing CSVs. Default: ","')				
		#To specify what will be done with loaded data [REQUIRED]
		parser.add_argument('-o', '--operation',
							required=True,
							type=str, nargs = '+',
							help = 'User specifies which processes will be performed on data')				

		return parser
	
	
	
	def error(self, message):
		'''prints colorized error message '''
		print(f"{clr.Fore.LIGHTRED_EX}Error: {clr.Style.RESET_ALL}{message}")
		
	def exampleOperation(self):
		'''Gives a preview of each CSVs contents'''
		print("called")
		for csv, contents in self.files.items():
			print(f"\n{clr.Fore.LIGHTGREEN_EX}---- {csv} ----{clr.Style.RESET_ALL}")
			size = len(contents)
			if size > 3:
				contents = contents[:3] + ['...\n']
			for c in contents:
				print(f"\t{c}")
		
		
	def load_files(self, files):
		'''loades files specified in terminal when program was initiated'''
		if files:
			#Search specified directory for specified files
			matches = [ f for f in files if f in listdir(self.directory) and f[-4:] == '.csv' ]
			
			#Load ea. CSV file
			for m in matches:
				path = self.directory + m
				with open( path, 'r') as file:
					
					#Removes "\n" at end of each line string
					#... then, turns line string into list, based on desire delimiter
					fileContents = [ line.replace("\n","").split( self.delimiter ) for line in file]
					file.close()
				
				#Updates repository of CSV files
				self.files[m] = fileContents
		else:
			#Display Error Message
			self.error("No csv files found")
	
	def run_operations(self, operations):
		'''Runs all operations specified on CLI'''
		if operations:
			for o in operations:
				if o in self.router.keys():
					self.router[o]()			#calls function to process files
				else:
					self.error(f"operation {clr.Fore.YELLOW}{o}{clr.Style.RESET_ALL} not found")
		else:
			self.error("No operation provided")
		
	def router_build(self):
		'''Sets up the means by which CLI specified operations call class functions
			... simply add to the dictionary 'self.router' below,
			... remember not to call the function with () in the dictionary, or it will activate on creation'''
		self.router = {
			#example:
			'operationName' : self.exampleOperation,
		}
		

if __name__== "__main__":
	Main()
			
