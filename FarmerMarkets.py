import sys
reload(sys)
sys.setdefaultencoding("latin-1")

import arcpy, string, os, zipfile, fileinput, time, math
from datetime import date
start_time = time.time()

import json

def createFeatureClass(featureName, featureData, featureFieldList, featureInsertCursorFields):
	print "Create " + featureName + " feature class"
	featureNameNAD83 = featureName + "_NAD83"
	featureNameNAD83Path = arcpy.env.workspace + "\\"  + featureNameNAD83
	arcpy.CreateFeatureclass_management(arcpy.env.workspace, featureNameNAD83, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	# Process: Define Projection
	arcpy.DefineProjection_management(featureNameNAD83Path, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	# Process: Add Fields	
	for featrueField in featureFieldList:
		arcpy.AddField_management(featureNameNAD83Path, featrueField[0], featrueField[1], featrueField[2], featrueField[3], featrueField[4], featrueField[5], featrueField[6], featrueField[7], featrueField[8])
	# Process: Append the records
	cntr = 1
	try:
		with arcpy.da.InsertCursor(featureNameNAD83, featureInsertCursorFields) as cur:
			for rowValue in featureData:
				cur.insertRow(rowValue)
				cntr = cntr + 1
	except Exception as e:
		print "\tError: " + featureName + ": " + e.message
	# Change the projection to web mercator
	arcpy.Project_management(featureNameNAD83Path, arcpy.env.workspace + "\\" + featureName, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	arcpy.FeatureClassToShapefile_conversion([featureNameNAD83Path], OUTPUT_PATH + "\\Shapefile")
	arcpy.Delete_management(featureNameNAD83Path, "FeatureClass")
	print "Finish " + featureName + " feature class."

	
INPUT_PATH = "input"
OUTPUT_PATH = "output"
if arcpy.Exists(OUTPUT_PATH + "\\FarmerMarkets.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\FarmerMarkets.gdb /s /q")
os.system("del " + OUTPUT_PATH + "\\*FarmerMarkets*.*")
os.system("del " + OUTPUT_PATH + "\\Shapefile\\*FarmerMarkets*.*")
arcpy.CreateFileGDB_management(OUTPUT_PATH, "FarmerMarkets", "9.3")
arcpy.env.workspace = OUTPUT_PATH + "\\FarmerMarkets.gdb"

featureName = "FarmerMarkets_Features"
json_file = open("input//FarmerMarkets.json", "r")
data = json.loads(json_file.read())
#print data["columns"]
#print data["rows"]
json_file.close()

featureData = []
print len(data["rows"])
for row in data["rows"]:
	featureData.append([(row[9], row[8]), row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]])
print len(featureData)
featureFieldList = [["ID", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "ADDRESS", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "DESCRIPTION", "TEXT", "", "", "2000", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "EVENTS", "TEXT", "", "", "2000", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "HOURS", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "IMAGE_URL", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "INCLUDED_WINERIES", "TEXT", "", "", "2000", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "LANGUAGE", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "LATITUDE", "DOUBLE", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "LONGITUDE", "DOUBLE", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "MARKER", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "OWNERS", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "TITLE", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "TYPE", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "WEBSITE", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""], [  "WINEMAKERS", "TEXT", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", ""]]
featureInsertCursorFields = ("SHAPE@XY", "ID",  "ADDRESS",  "DESCRIPTION",  "EVENTS",  "HOURS",  "IMAGE_URL",  "INCLUDED_WINERIES",  "LANGUAGE",  "LATITUDE",  "LONGITUDE",  "MARKER",  "OWNERS",  "TITLE",  "TYPE",  "WEBSITE",  "WINEMAKERS")
createFeatureClass(featureName, featureData, featureFieldList, featureInsertCursorFields)



