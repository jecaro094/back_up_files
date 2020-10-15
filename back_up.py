# NOTE Import libraries
import os, shutil
from datetime import datetime


separador = "*"*20

# NOTE Functions

def last_modification_date_from_file(path):
    """
    Returns last modification date from file detailed in path (input)
    """
    modification_date_str = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
    modification_date_str2 = (modification_date_str).split("T")[0] + " " + (modification_date_str).split("T")[1]
    try:
        return datetime.strptime(modification_date_str2, '%Y-%m-%d %H:%M:%S.%f')
    except:
        return datetime.strptime(modification_date_str2, '%Y-%m-%d %H:%M:%S')
        

def last_date_from_file(folder):
    """
    Prints all files inside the directory and its modification date
    Returns last date from folder (file latest modified inside)
    """
    date_vector= []
    for path, subdirs, files in os.walk(folder):
        for name in files:
            date_vector.append(last_modification_date_from_file(path))
            file_considered = (os.path.join(path, name)).split(f"{folder}")[-1]
            #print(file_considered, last_modification_date_from_file(path))
            
    return max(date_vector)


def get_folders_inside_path(root_folder):
    """
    Returns list of folders in the order in which are in the folder structure
    """
    
    dirs_path_inside = [x[0] for x in os.walk(root_folder) if x[0]!=root_folder]
    path_without_root = ["".join(x.split(f"{root_folder}")) for x in dirs_path_inside]
    #print(path_without_root)
    folder_to_consider = [x.split(f"{os.path.sep}") for x in path_without_root]
    
    for f in folder_to_consider:
        f.pop(0)
        
    #print(folder_to_consider)
    
    return sorted(folder_to_consider, key=len)


def create_missing_folders(source_folder, target_folder, folder_to_copy):
    """
    Creates missing folders in target directory before copying all the files...
    """
    print("\n", separador + " COMENZAMOS A CREAR CARPETAS " + separador)

    for f in get_folders_inside_path(source_folder):
        #print(f)
        final_folder = os.path.join(target_folder, *f)
        f_name = final_folder.split(target_folder)[-1]
        if not os.path.exists(final_folder):
            try:
                print(f"Creando carpeta en '{folder_to_copy}: '{f_name}'...")
                os.mkdir(final_folder)
            except:
                print(f"Error al crear carpeta en '{folder_to_copy}': '{f_name}'")
                pass
        else:
            print(f"La carpeta '{f_name}' ya existe en '{folder_to_copy}'!!")
            pass

    print(separador + " FINALIZAMOS LA CREACIÓN DE CARPETAS " + separador, "\n")
            


def copy_files(source, target, folder_to_copy):
    """
    """

    print("\n", separador + " COMENZAMOS A COPIAR ARCHIVOS " + separador)

    if os.listdir(source) and os.listdir(target):
        for path, subdirs, files in os.walk(source):
            for name in files:
                file_considered = (os.path.join(path, name)).split(f"{source}")[-1]
                s = source + file_considered
                t = target + file_considered
                #print("file_considered", file_considered)
                
                # Condición para mover archivos...
                if not os.path.exists(t):
                    try:
                        print(f"Creando archivo en '{folder_to_copy}': ", t.split(target)[-1])
                        os.chmod(s, 0o777)
                        shutil.copy2(s, t)
                    except:
                        print(f"Error al crear archivo en '{folder_to_copy}': ", t.split(target)[-1])
                        pass
                else: # If exists
                    last_modification_t = last_modification_date_from_file(t)
                    last_modification_s = last_modification_date_from_file(s)
                    
                    # If I updated a file, I replace it when I make the copy in the Hard Disk
                    if last_modification_t<last_modification_s:
                        print(f"Actualizando archivo en '{folder_to_copy}': ", t.split(target)[-1])
                        os.chmod(t, 0o777)
                        os.remove(t)
                        shutil.copy2(s, t)

    elif not os.listdir(source) and os.listdir(target):
        print(f"Cannot copy; {source} does not exist...")

    elif not os.listdir(target) and os.listdir(source):
        print(f"Cannot copy; {target} does not exist...")

    elif not os.listdir(source) and not os.listdir(target):
        print("Cannot copy; none of the dirs does not exist...")
                
    
    print(separador + " FINALIZAMOS LA COPIA DE ARCHIVOS " + separador, "\n")

# ----------------------------------------------------------------------------------------- #
# ------------------------------------ MAIN CODE ------------------------------------------ #
# ----------------------------------------------------------------------------------------- #

#source_dir = os.path.join(os.getcwd(), "source")
#target_dir = os.path.join(os.getcwd(), "target")

source_dir = 'D:\\DatosUsuario\\jecar\\Escritorio\\MASTER_BIG_DATA'
target_dir = "F:\\BACK UPS\\USADOS\\BACKUP_MASTER"

# NOTE No pueden existir las dos a la vez (o, al menos, una debe ser una lista vacía)...
#folders_not_to_copy = ['API-MÁSTER-SCHEDULING', '.tmp.drivedownload', '.Rhistory', '.RData']
only_copy_these_folders = ['6-INFRAESTRUCTURA BIG DATA']

# NOTE Es mejor hacer esto solo una vez...
#create_missing_folders(source_dir, target_dir)

try: 
    folders_not_to_copy
    for folder_to_copy in os.listdir(source_dir):

        if folder_to_copy not in folders_not_to_copy:
            s = os.path.join(source_dir, folder_to_copy)
            t = os.path.join(target_dir, folder_to_copy)
            create_missing_folders(s, t, folder_to_copy)
            copy_files(s, t, folder_to_copy)

except: 
    only_copy_these_folders
    for folder_to_copy in os.listdir(source_dir):

        if folder_to_copy in only_copy_these_folders:
            s = os.path.join(source_dir, folder_to_copy)
            t = os.path.join(target_dir, folder_to_copy)
            create_missing_folders(s, t, folder_to_copy)
            copy_files(s, t, folder_to_copy)
