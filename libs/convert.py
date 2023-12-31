import os
from utils import fs
from format.qvm import QVM


def convert_qvm(qvm_version=7):
    src_folder = "input"
    dst_folder = "output"
    count = 0

    try:
        for srcpath in fs.walkdir(src_folder, '*.qvm'):
            qvmfile = QVM()
            qvmfile.load(srcpath)

            dstpath = srcpath.replace(src_folder, dst_folder, 1)

            print(f"Converting: {srcpath} to {dstpath}")

            os.makedirs(os.path.dirname(dstpath), exist_ok=True)

            with open(dstpath, 'wb') as fp:
                qvmfile.save(fp, version=qvm_version)

            count += 1

        return dstpath

    except Exception as exception:
        print(f"Error occurred: {str(exception)}")
        return None
