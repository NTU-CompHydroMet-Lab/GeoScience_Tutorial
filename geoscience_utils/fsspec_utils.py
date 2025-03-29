# geoscience/package/fsspec_utils.py
import fsspec
from virtualizarr import open_virtual_dataset

def get_s3_files(bucket_path, pattern='*.nc', anonymous=True)->list:
    """Get files from S3 bucket matching the pattern.
    
    Args:
        bucket_path (str): S3 bucket path
        pattern (str): File pattern to match
        anonymous (bool): Whether to use anonymous access
    
    Returns:
        list: List of matched file paths
    """
    try:
        fs = fsspec.filesystem('s3', anon=anonymous, connect_timeout=30)
        files = fs.glob(f'{bucket_path}/{pattern}')
        sorted_files = sorted(['s3://' + f for f in files])
        print(f'Dataset info:\n  Total number: {len(sorted_files)}\n  First file: {sorted_files[0]}\n  Last file: {sorted_files[-1]}')
        return sorted_files
    except:
        raise ValueError(f'Failed to access S3 bucket: {bucket_path}')
    

def create_virtual_datasets(file_urls:str, storage_options=None)->list:
    """Create virtual datasets from a list of URLs.

    Args:
        file_urls (list): List of URLs to create virtual datasets from.
        storage_options (dict, optional): Storage options for data access.
            Defaults to {'anon': True} for anonymous access.

    Returns:
        list: List of virtual dataset objects.
    """
    if storage_options is None:
        storage_options = {'anon': True} # anonymous acces (no login), access public dataset

    virtual_datasets = [
        open_virtual_dataset(
            url,
            indexes={},
            reader_options={'storage_options': storage_options}
        )
        for url in file_urls
    ]

    return virtual_datasets


if __name__ == '__main__':

    files = get_s3_files(
        'noaa-cdr-sea-surface-temp-optimum-interpolation-pds/data/v2.1/avhrr',
        '202408/*.nc'
    )

    oisst_datasets = create_virtual_datasets(files)

    print(oisst_datasets)
