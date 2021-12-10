import pandas as pd
import shutil
import glob
import os
import numpy as np
import zipfile
from pathlib import Path

def show_orders(porder_request):
    out = []
    for s in [s.split('|') for s in porder_request if '|' in s]:
        out.append([ss.strip() for ss in s])
    df = pd.DataFrame(data=out[1:], columns=out[0])
    return df


def restructure_downloaded_files(download_dir):
    flist = glob.glob(os.path.join(download_dir, '*_3B*'))
    [os.remove(f) for f in glob.glob(os.path.join(download_dir, '*manifest.json'))]
    basenames = pd.unique([os.path.basename(f).split('_3B')[0] for f in flist])
    for b in basenames:
        sub_dir = os.path.join(download_dir, b)
        flist_sub = glob.glob(os.path.join(download_dir, b+'*'))
        if len(flist_sub) >= 5:
            os.makedirs(sub_dir, exist_ok=True)
            for fs in flist_sub:
                try:
                    shutil.move(fs, sub_dir)
                except:
                    continue


def convert_txt_to_imagelist(infile, outfile):
    df = pd.read_csv(infile, header=None).T
    dfout = df.apply(lambda x: x[0].split(':')[1].strip(), axis=1)
    dfout = dfout.drop_duplicates()
    dfout.to_csv(outfile, header=None, index=None)


def download_planet_order(df, index, download_dir):
    orderid = df.loc[index]['url']
    ordername = df.loc[index]['name']

    download_dir_sub = os.path.join(download_dir, ordername)

    print("Download Directory: ", download_dir_sub, "\nOrder Name: ", ordername)

    os.makedirs(download_dir_sub, exist_ok=True)
    s_dl = f'porder download --url {orderid} --local "{download_dir_sub}"'

    print(s_dl)
    os.system(s_dl)


def unzip_PSOrthoTileOrder(zip_file, 
                           target_dir=None, 
                           delete_zip=False, 
                           cleanup_intermediate=True):
    """
    
    """
    unzip_path = zip_file.parent / zip_file.name.rstrip('.zip')

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(unzip_path)

    base = [d for d in list(unzip_path.glob('**')) if d.stem == 'PSOrthoTile'][0]

    datasets = list(base.glob('*'))

    for ds in datasets:
        #print(ds)
        for f in ds.glob('analytic_sr_udm2/*'):
            shutil.move(str(f), str(ds))
        shutil.rmtree(str(ds / 'analytic_sr_udm2'))
        if not target_dir:
            shutil.move(str(ds), str(unzip_path))
        else:
            shutil.move(str(ds), str(Path(target_dir)))

    shutil.rmtree(unzip_path / 'files')
    
    if delete_zip:
        shutil.rmtree(zip_file)
        
    if cleanup_intermediate:
        if (len(list(unzip_path.glob('*'))) == 1) & (list(unzip_path.glob('*'))[0].stem =='manifest'):
            shutil.rmtree(unzip_path)
    
    return 1


def check_zipcontent_exists(zip_file, tiles_dir):
    flist = [f.stem for f in list(tiles_dir.glob('*/*'))]
    l = []
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for f in zip_ref.filelist:
            #print(f)
            try:
                p = Path(f.filename).parts[2]
                l.append(p in flist)
            except:
                continue
    return np.all(l)

