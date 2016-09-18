#!/usr/bin/env python

# IMPORT python base modules
import argparse

''' BEGIN FUNCTION
	Run the command line program, parse incoming arguments '''
def initialize():

    # Initialize the command line argument parser
    parser = argparse.ArgumentParser(
    	prog="BasketLauncher",
    	description="Application launcher to keep Ian's head on straight through Senior Project")

    # Add Arguments to the parser
    parser.add_argument("--show",
    	help="Define the show",
    	type=str)
    parser.add_argument("-s", "--seq",
    	required=True,
    	help="Define the sequence",
    	type=str)
    parser.add_argument("-sh", "--shot",
    	required=True,
    	help="Define the shot",
    	type=str)
    parser.add_argument("-st", "--stage",
        required=True,
    	help="Define the step of the process",
    	type=int)
    parser.add_argument("-t", "--tag",
        help="Define a specific tag to open the most recent file",
        type=str)

    # store_true means to receive no arguments, provide callback of TRUE when flag is used
    parser.add_argument("-r", "--render",
    	help="# # # NO ACTION # # #",
    	action="store_true")

    # Parse the arguments passed into the command line
    args = parser.parse_args()

# Runs if the file is run directly... NOT imported
if __name__ == "__main__":
    initialize()