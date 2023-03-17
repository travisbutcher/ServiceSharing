import arcpy
import os, sys
import datetime

def update_template(update_dict, output_project):
    try:
        for project_map in aprx.listMaps():
            for l in project_map.listLayers():
                if l.isFeatureLayer:
                    print('updating {}'.format(l.name))
                    conProp = l.connectionProperties
                    print(conProp)
                    l.updateConnectionProperties(conProp, update_dict)
                    print('Finished {}'.format(l.name))

        print('Updating', prod_dict, 'with', staging_dict)
        #aprx.updateConnectionProperties(prod_dict, staging_dict)
        print('layers path update')
        aprx.saveACopy(output_project)
        print('files saved')
    except:
        print('update failed')

resource_template = r'Production_Resource.aprx'
base_template =  r'Production_BaseLayer.aprx'
api_template =  r'Production_API.aprx'
template_output = r'.\\ Services\\'

updates = [resource_template, base_template, api_template]
update_dev = True
update_staging = True
update_production = False

for resource in updates:
    if 'Resource' in resource:
        layer_suffix = 'Resource'
    elif 'BaseLayer' in resource:
        layer_suffix = 'BaseLayer'
    else:
        layer_suffix = 'API'

    # Get Pro project template
    aprx = arcpy.mp.ArcGISProject(resource)

    # Get map for the name above
    dev_dict = { 'connection_info': 
    {
                        'authentication_mode': 'DBMS', 
                        'database': '', 
                        'dbclient': 'sqlserver', 
                        'db_connection_properties': '', 
                        'password': "", 
                        'instance':'', 
                        'server': '', 
                        'user': '', 
                        'version': ''
                    }
                }

    staging_dict = { 'connection_info': 
    {
                        'authentication_mode': 'DBMS', 
                        'database': '', 
                        'dbclient': 'sqlserver', 
                        'db_connection_properties': '', 
                        'password': "", 
                        'instance':'', 
                        'server': '', 
                        'user': '', 
                        'version': ''
                    }
                }

    prod_dict = { 'connection_info': 
    {
                        'authentication_mode': 'DBMS', 
                        'database': '', 
                        'dbclient': 'sqlserver', 
                        'db_connection_properties': '', 
                        'password': "", 
                        'instance':'', 
                        'server': '', 
                        'user': '', 
                        'version': ''
                    }
                }
    if update_dev:
        update_template(dev_dict, r'{}\\Development_{}.aprx'.format(template_output, layer_suffix))

    if update_staging:
        update_template(staging_dict, r'{}\\Staging_{}.aprx'.format(template_output,layer_suffix))

    if update_production: 
        update_template(prod_dict, r'{}\\Production_{}.aprx'.format(template_output,layer_suffix))
