# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:18:01 2016
@author: ellisrj2

This script is used to find mouse or human orthologs from an inputted list of mouse or human genes. You must download the full MGI orthologs file found at: http://www.informatics.jax.org/homology.shtml. The script is written with the assumption that multiple gene lists are in one directory and the path to this directory is the function input. The script can easily be modified to work on one list.
"""

def get_MGI_hum_orthologs(wdir):
    import pandas
    import csv
    import os, os.path

    path = os.listdir(wdir)
    
    for f,i in zip(path,range(len(path))):
        if f[-3:] == 'txt':
            homologene_ids = []
            mouse_genes = []
            human_genes = []
            
            genes = [gene.rstrip('\n') for gene in open(f)]
            genes = [gene.lower() for gene in genes]
            
            #load MGI_all_orthologs.xlsx, make all genes lowercase for ease of searching
            df_ortho_file = pandas.read_excel('MGI_all_orthologs.xlsx', skipinitialspace=True)
            
            #separate dataframe into human data and mouse data
            df_human = df_ortho_file[df_ortho_file['Common Organism Name']=='human']
            df_human_genes = df_human['Symbol']
            df_human_genes = [str(gene) for gene in df_human_genes]
            df_human_genes = [gene.lower() for gene in df_human_genes]
            df_human_homologene_ids = df_human['HomoloGene ID']
            df_human_homologene_ids = [int(homoid) for homoid in df_human_homologene_ids]
        
            df_mouse = df_ortho_file[df_ortho_file['Common Organism Name']=='mouse, laboratory']
            df_mouse_genes = df_mouse['Symbol']
            df_mouse_genes = [str(gene) for gene in df_mouse_genes]
            df_mouse_genes = [gene.lower() for gene in df_mouse_genes]
            df_mouse_homologene_ids = df_mouse['HomoloGene ID']
            df_mouse_homologene_ids = [int(homoid) for homoid in df_mouse_homologene_ids]
            
            for gene in genes:
                if gene in df_mouse_genes:
                    mouse_genes.append(gene)
                    mouse_gene_index = df_mouse_genes.index(gene)
                    mouse_homologene_id = df_mouse_homologene_ids[mouse_gene_index]
                    homologene_ids.append(mouse_homologene_id)
                    if mouse_homologene_id in df_human_homologene_ids:
                        human_gene_index = df_human_homologene_ids.index(mouse_homologene_id)
                        human_genes.append(df_human_genes[human_gene_index])
                    else:
                        human_genes.append('no corresponding ortholog')
                else:
                    mouse_genes.append('gene not in list')
                    human_genes.append('gene not in list')
                    homologene_ids.append('gene not in list')
                    
            with open(f + '_MGI_human_orthologs.csv', 'w') as thefile:
                writer = csv.writer(thefile)
                writer.writerow(['Gene', 'Homologene ID', 'Human Ortholog'])
                writer.writerows(zip(genes, homologene_ids, human_genes))
                    