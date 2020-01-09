import os
import arcpy

def eraseFeatures(in_features,erase_features):
    arcpy.env.workspace = os.path.dirname(in_features)
    arcpy.env.overwriteOutput = True
    inName = os.path.basename(in_features)[:10].replace('.shp','') #Fields are only the first 10 characters
    eraseName = os.path.basename(erase_features)[:10].replace('.shp','') #remove .shp from the name if it's a shapefile

    unionResult = arcpy.Union_analysis([in_features,erase_features],'in_memory/union_result')
    
    inField = 'FID_{}'.format(inName)
    eraseField = 'FID_{}'.format(eraseName)
    condOI = '"{}" >= 0 AND {} < 0'.format(inField,eraseField)
    
    erasedFeatures = arcpy.Select_analysis(unionResult,'Erase_Result',condOI) #Select the features that are of interest using condOI and the field names
    
    arcpy.Delete_management('in_memory')
    
    return erasedFeatures



if __name__ == '__main__':
    inFeat = arcpy.GetParameterAsText(0)
    eraseFeat = arcpy.GetParameterAsText(1)
    
    result = eraseFeatures(inFeat,eraseFeat)
    
    arcpy.AddMessage('Script completed.')