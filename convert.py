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

        print(f"Conversion completed. Total files converted: {count}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    qvm_version = 7
    convert_qvm(qvm_version)
