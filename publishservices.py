import arcpy
import os

# Set output file names
update_template = r'Staging_Resource.aprx'
outdir = r".\\Services\\SD Files\\"
federated_server=""


# Reference map to publish
aprx = arcpy.mp.ArcGISProject(update_template)
for project_map in aprx.listMaps():
    service = project_map.name
    try:
        service = service.replace('(','_').replace(')','_').replace('-','_')
        print(service)
        sddraft_filename = r".\\Services\\Staging\\" + service + ".sddraft"
        print(sddraft_filename)
        sddraft_output_filename = os.path.join(outdir, sddraft_filename)
        print(sddraft_output_filename)

        # Create MapImageSharingDraft and set service properties
        sharing_draft = project_map.getWebLayerSharingDraft("FEDERATED_SERVER", "MAP_IMAGE", service)
        sharing_draft.federatedServerUrl = federated_server
        sharing_draft.summary = "Service {}".format(project_map.name)
        sharing_draft.tags = "Publish"

        # Create Service Definition Draft file
        print('Exporting Service Definition'.format(service))
        sharing_draft.exportToSDDraft(sddraft_filename)

        # Stage Service
        sd_filename = service + ".sd"
        sd_output_filename = os.path.join(outdir, sd_filename)
        arcpy.StageService_server(sddraft_output_filename, sd_output_filename)

        # Share to portal
        print('Uploading Service Definition'.format(service))
        arcpy.UploadServiceDefinition_server(sd_output_filename, federated_server)

        print('Successfully Uploaded {}'.format(service))
    except:
        print('error publishing {}'.format(service))