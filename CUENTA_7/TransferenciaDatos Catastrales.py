#Desarrollo Transferencia de Datos Catastrales
#Desarrollado por : Michael Andres Rojas Rivera y Yaritza Dorely Quevedo Tovar
#24/07/2024
#Descripción: Script para la migración y transferencia de datos de una capa LADM a una base de datos con vacios de información catastral.

import arcpy
import os

# Parámetros de entrada
Base_Catastral = arcpy.GetParameterAsText(0)
Base_Vectorizada = arcpy.GetParameterAsText(1)
Ruta_Salida = os.path.dirname(Base_Catastral)

arcpy.env.overwriteOutput = True

# Convertir Base_Catastral a puntos conservando la información
featuretopoint = arcpy.management.FeatureToPoint(Base_Catastral, os.path.join(Ruta_Salida, 'Base_Catastral_Point'), "INSIDE")

# Asegurar la existencia de campos en Base_Vectorizada
fields_to_add = [("CODIGO", "TEXT"), ("CODIGO_ANT", "TEXT")]
existing_fields = [f.name for f in arcpy.ListFields(Base_Vectorizada)]
for field_name, field_type in fields_to_add:
    if field_name not in existing_fields:
        arcpy.management.AddField(Base_Vectorizada, field_name, field_type)
        arcpy.AddMessage(f"Campo '{field_name}' añadido a la capa de destino.")

# Crear una capa temporal para Base_Vectorizada
Base_Vectorizada_Layer = "Base_Vectorizada_Layer"
arcpy.MakeFeatureLayer_management(Base_Vectorizada, Base_Vectorizada_Layer)
arcpy.AddMessage("Capa temporal 'Base_Vectorizada_Layer' creada.")

arcpy.AddMessage("Procesando puntos y transfiriendo datos")

# Crear un diccionario para contar puntos por polígono
polygon_point_counts = {}

# Iterar sobre los puntos en featuretopoint
with arcpy.da.SearchCursor(featuretopoint, ["SHAPE@", "CODIGO", "CODIGO_ANT"]) as point_cursor:
    for point in point_cursor:
        # Realizar la selección por localización para encontrar el polígono correspondiente
        arcpy.management.SelectLayerByLocation(Base_Vectorizada_Layer, "CONTAINS", point[0])
        with arcpy.da.SearchCursor(Base_Vectorizada_Layer, ["OID@", "SHAPE@", "CODIGO", "CODIGO_ANT"]) as polygon_cursor:
            for polygon in polygon_cursor:
                polygon_id = polygon[0]
                # Inicializar o incrementar el contador de puntos para el polígono
                if polygon_id in polygon_point_counts:
                    polygon_point_counts[polygon_id]['count'] += 1
                else:
                    polygon_point_counts[polygon_id] = {'count': 1, 'CODIGO': point[1], 'CODIGO_ANT': point[2]}

# Actualizar los atributos en Base_Vectorizada donde hay exactamente un punto
with arcpy.da.UpdateCursor(Base_Vectorizada, ["OID@", "CODIGO", "CODIGO_ANT"]) as update_cursor:
    for row in update_cursor:
        polygon_id = row[0]
        if polygon_id in polygon_point_counts and polygon_point_counts[polygon_id]['count'] == 1:
            row[1] = polygon_point_counts[polygon_id]['CODIGO']
            row[2] = polygon_point_counts[polygon_id]['CODIGO_ANT']
            update_cursor.updateRow(row)
            arcpy.AddMessage(f"Polígono OID {polygon_id} actualizado con CODIGO {row[1]} y CODIGO_ANT {row[2]}.")

#arcpy.management.Delete(featuretopoint)

arcpy.AddMessage("Proceso finalizado con éxito.")



