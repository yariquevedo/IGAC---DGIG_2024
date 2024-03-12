# Desarrollo de Inconsistencias Ortofoto 
# Semillero de Investigación y Desarrollo (2024)
# Yaritza Quevedo - Michael Rojas

import arcpy
import os

GDB_Entrada = arcpy.GetParameterAsText(0)  # Inconsistencias de MDT u Ortofo
Ruta_Salida = arcpy.GetParameterAsText(1)  # Ruta de salida
Limite = arcpy.GetParameterAsText(2)  # Límites del proyecto
Marcos_Control = arcpy.GetParameterAsText(3)
LIM = arcpy.GetParameterAsText(4)
MARC = arcpy.GetParameterAsText(5)

# Creando GDB y FC para almacenar conteos
gdb_temporal = arcpy.management.CreateFileGDB(Ruta_Salida, "GDB_Temporal")
fc_temporal = arcpy.management.CreateFeatureclass(gdb_temporal, "errores_temp", "POLYGON", spatial_reference=arcpy.SpatialReference(9377))
arcpy.management.AddField(fc_temporal,"Tipo_Error", "TEXT")
arcpy.env.workspace = GDB_Entrada
# CREANDO ERRORES ORTO --------------------------------------------------------------------------
sql_orto1 = "Tipo_Error = '1'"
sql_orto2 = "Tipo_Error = '2'"
sql_orto3 = "Tipo_Error = '3'"
sql_orto4 = "Tipo_Error = '4'"
sql_orto5 = "Tipo_Error = '5'"
sql_orto6 = "Tipo_Error = '6'"
#Listando Datasets de la GDB de entrada
featuredatasets = arcpy.ListDatasets()
with open(os.path.join(Ruta_Salida, "Reporte de porcentaje de errores.txt"), "w") as file:
    file.write (f"--------------------------------------------------------------------------------------------\n")
    file.write (f"REPORTE DE % DE ÁREAS DE INCONSISTENCIAS\n")
    file.write (f"\n")
    file.write (f"--------------------------------------------------------------------------------------------\n")
    for ds in featuredatasets:
        featureclasses = arcpy.ListFeatureClasses(feature_dataset=ds)
        #Listando Feature classes de la GDB
        for fc in featureclasses: 
                
            if fc.endswith("Orto"):
                file.write (f"## REPORTE PARA INCONSISTENCIAS DE ORTOIMAGEN ## -----------------------------------------------------\n")
                file.write (f"\n")
                arcpy.AddMessage ("Validando inconsistencias para ortoimagen en la capa: {0}".format(str(fc)))
                            
                ## Si se realiza el calculo con el limite del proyecto para ORTO ----------------------------------------------------------------------------------------------
                if LIM.lower() == 'true':
                 #Crea una capa temporal
                    file.write (f"-#- REPORTE PARA INCONSISTENCIAS DE ORTOIMAGEN CALCULANDO CON LÍMITE DEL PROYECTO -#-\n")
                    file.write (f"\n")
                    arcpy.MakeFeatureLayer_management(os.path.join(Limite), "capa_temporal")
                    # Itera sobre cada elemento en la capa  
                    with arcpy.da.SearchCursor("capa_temporal", ["SHAPE@"]) as cursor:
                        for a in cursor:
                            #Reproyectar a origen unico nacional
                            a[0].projectAs('9377')
                            # Obtiene el área en metros cuadrados y la convierte a hectáreas (1 m² = 0.0001 ha)
                            area_hectareas = round(a[0].area * 0.0001,2)                  
                    file.write (f"- ÁREA TOTAL DEL LÍMITE DEL PROYECTO: --- {(area_hectareas)} hectáreas ---\n")
                    file.write (f"\n")
                                                                        
                    #CURSOR PARA CALCULAR EL ÁREA DE LOS ELEMENTOS EN INCONSISTENCIAS MDT 
                    arcpy.AddMessage ("Calculando área de inconsistencias por límite del proyecto")
                    inconsistencias = arcpy.analysis.Intersect([Limite,fc], "Inconsistencias_Limite")           
                            
                    with arcpy.da.SearchCursor(inconsistencias, ['SHAPE@','Tipo_Error']) as sCur:
                        with arcpy.da.InsertCursor(os.path.join(str(gdb_temporal),str(fc_temporal)),['SHAPE@','Tipo_Error']) as iCur:
                            for row in sCur:
                                row_list= list(row)
                                row_list[0]= row[0].projectAs('9377')
                                row_list[0]=row[0]
                                row_list[1]=row[1]
                                row=tuple(row_list)
                                iCur.insertRow(row)

                    #PARA TIPO DE ERROR 1 = Error de modelo digital de terreno
                    conteo_area= 0
                    with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto1) as cursor:
                        for area in cursor:
                            conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                    file.write (f"- Área total de Error de modelo digital de terreno {(conteo_area)} hectareas\n")
                    ErrorORTO1 = round((conteo_area/area_hectareas)*100,2)
                    file.write (f"- Error porcentual de modelo digital de terreno {(ErrorORTO1)} %\n")
                    file.write (f"\n")
                                
                    #PARA TIPO DE ERROR 2 = Error de línea de costura
                    conteo_area= 0
                    with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto2) as cursor:
                        for area in cursor:
                            conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                    file.write (f"- Área total de Error por línea de costura {(conteo_area)} hectareas\n")
                    ErrorORTO2 = round((conteo_area/area_hectareas)*100,2)
                    file.write (f"- Error porcentual por línea de costura {(ErrorORTO2)} %\n")
                    file.write (f"\n")

                    #PARA TIPO DE ERROR 3 = Error de fundido
                    conteo_area= 0
                    with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto3) as cursor:
                        for area in cursor:
                            conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                    file.write (f"- Área total de Error de fundido {(conteo_area)} hectareas\n")
                    ErrorORTO3 = round((conteo_area/area_hectareas)*100,2)
                    file.write (f"- Error porcentual por Error de fundido {(ErrorORTO3)} %\n")
                    file.write (f"\n")
                            
                    #PARA TIPO DE ERROR 4 = Error de radiometría
                    conteo_area= 0
                    with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto4) as cursor:
                        for area in cursor:
                            conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                    file.write (f"- Área total de Error por radiometría {(conteo_area)} hectareas\n")
                    ErrorORTO4 = round((conteo_area/area_hectareas)*100,2)
                    file.write (f"- Error porcentual por radiometría {(ErrorORTO4)} %\n")
                    file.write (f"\n")
                                
                    #PARA TIPO DE ERROR 5 = Error de desplazamiento zonificado
                    conteo_area= 0
                    with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto5) as cursor:
                        for area in cursor:
                            conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                    file.write (f"- Área total de Error de desplazamiento zonificado {(conteo_area)} hectareas\n")
                    ErrorORTO5 = round((conteo_area/area_hectareas)*100,2)
                    file.write (f"- Error porcentual por desplazamiento zonificado {(ErrorORTO5)} %\n")
                    file.write (f"\n")
                                
                    #PARA TIPO DE ERROR 6 = Error de omisión
                    conteo_area= 0
                    with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto6) as cursor:
                        for area in cursor:
                            conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                    file.write (f"- Área total de Error de omisión {(conteo_area)} hectareas\n")
                    ErrorORTO6 = round((conteo_area/area_hectareas)*100,2)
                    file.write (f"- Error porcentual por Error de omisión {(ErrorORTO6)} %\n")
                    file.write (f"\n")
                                 
                    ## SI SE REALIZA EL CÁLCULO PARA MARCOS DE CONTROL EN ORTO-----------------------------------------------------------------
                    if MARC.lower() == 'true':

                        #Crea una capa temporal
                        file.write (f"-#- REPORTE PARA INCONSISTENCIAS EN ORTOIMAGEN CON MARCOS DE CONTROL -#-\n")
                        file.write (f"\n")
                        arcpy.MakeFeatureLayer_management(os.path.join(Marcos_Control), "capa_temporal")
                        # Itera sobre cada elemento en la capa  
                        area_hectareas = 0
                        with arcpy.da.SearchCursor("capa_temporal", ["SHAPE@"]) as cursor:
                            for a in cursor:
                            #Reproyectar a origen unico nacional
                                a[0].projectAs('9377')
                                # Obtiene el área en metros cuadrados y la convierte a hectáreas (1 m² = 0.0001 ha)
                                area_hectareas = area_hectareas + round(a[0].area * 0.0001,2)                  
                        file.write (f"- ÁREA TOTAL DE LOS MARCOS DE CONTROL: --- {(area_hectareas)} hectáreas ---\n")
                        file.write (f"\n")
                                                                            
                        #CURSOR PARA CALCULAR EL ÁREA DE LOS ELEMENTOS EN INCONSISTENCIAS MDT 
                        arcpy.AddMessage ("Calculando área de inconsistencias por marcos de control")
                        inconsistencias = arcpy.analysis.Intersect([Marcos_Control,fc], "Inconsistencias_Limite")           
                        with arcpy.da.SearchCursor(inconsistencias, ['SHAPE@','Tipo_Error']) as sCur:
                            with arcpy.da.InsertCursor(os.path.join(str(gdb_temporal),str(fc_temporal)),['SHAPE@','Tipo_Error']) as iCur:
                                for row in sCur:
                                    row_list= list(row)
                                    row_list[0]= row[0].projectAs('9377')
                                    row_list[0]=row[0]
                                    row_list[1]=row[1]
                                    row=tuple(row_list)
                                    iCur.insertRow(row)

                        #PARA TIPO DE ERROR 1 = Error de modelo digital de terreno
                        conteo_area= 0
                        with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto1) as cursor:
                            for area in cursor:
                                conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                        file.write (f"- Área total de Error de modelo digital de terreno {(conteo_area)} hectareas\n")
                        ErrorORTO1 = round((conteo_area/area_hectareas)*100,2)
                        file.write (f"- Error porcentual de modelo digital de terreno {(ErrorORTO1)} %\n")
                        file.write (f"\n")
                                    
                        #PARA TIPO DE ERROR 2 = Error de línea de costura
                        conteo_area= 0
                        with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto2) as cursor:
                            for area in cursor:
                                conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                        file.write (f"- Área total de Error por línea de costura {(conteo_area)} hectareas\n")
                        ErrorORTO2 = round((conteo_area/area_hectareas)*100,2)
                        file.write (f"- Error porcentual por línea de costura {(ErrorORTO2)} %\n")
                        file.write (f"\n")

                        #PARA TIPO DE ERROR 3 = Error de fundido
                        conteo_area= 0
                        with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto3) as cursor:
                            for area in cursor:
                                conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                        file.write (f"- Área total de Error de fundido {(conteo_area)} hectareas\n")
                        ErrorORTO3 = round((conteo_area/area_hectareas)*100,2)
                        file.write (f"- Error porcentual por Error de fundido {(ErrorORTO3)} %\n")
                        file.write (f"\n")
                                
                        #PARA TIPO DE ERROR 4 = Error de radiometría
                        conteo_area= 0
                        with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto4) as cursor:
                            for area in cursor:
                                conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                        file.write (f"- Área total de Error por radiometría {(conteo_area)} hectareas\n")
                        ErrorORTO4 = round((conteo_area/area_hectareas)*100,2)
                        file.write (f"- Error porcentual por radiometría {(ErrorORTO4)} %\n")
                        file.write (f"\n")
                                    
                        #PARA TIPO DE ERROR 5 = Error de desplazamiento zonificado
                        conteo_area= 0
                        with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto5) as cursor:
                            for area in cursor:
                                conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                        file.write (f"- Área total de Error de desplazamiento zonificado {(conteo_area)} hectareas\n")
                        ErrorORTO5 = round((conteo_area/area_hectareas)*100,2)
                        file.write (f"- Error porcentual por desplazamiento zonificado {(ErrorORTO5)} %\n")
                        file.write (f"\n")
                                    
                        #PARA TIPO DE ERROR 6 = Error de omisión
                        conteo_area= 0
                        with arcpy.da.SearchCursor(fc_temporal, ['SHAPE@'], sql_orto6) as cursor:
                            for area in cursor:
                                conteo_area = conteo_area + round(area[0].area * 0.0001,2)       
                        file.write (f"- Área total de Error de omisión {(conteo_area)} hectareas\n")
                        ErrorORTO6 = round((conteo_area/area_hectareas)*100,2)
                        file.write (f"- Error porcentual por Error de omisión {(ErrorORTO6)} %\n")
                        file.write (f"\n")


                    else:
                        pass
                else:
                    pass
            else:
                pass            