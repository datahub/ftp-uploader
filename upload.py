import glob, os, ftplib
from multiprocessing import Pool


######################### CONFIG #############################
ABS_PATH_TO_DIRECTORY = ''
FILE_TYPES = '*.png'
CONCURRENT_UPLOADS = 4

DOMAIN = ''
USER = ''
PASS = ''
DESTINATION_DIRECTORY = ''
##############################################################


def upload(infile):
    try:
        ftp = ftplib.FTP(DOMAIN, USER, PASS)
        f = open(infile, 'rb')
        ftp.cwd(DESTINATION_DIRECTORY)
        ftp.storbinary('STOR %s' % (os.path.basename(infile)), f)
        f.close()
        ftp.quit()
        os.remove(infile)
        print 'UPLOADED: %s' % (infile)
    except:
        print 'FAILED: %s' % (infile)

def go():
    to_upload = []
    for image_file in glob.glob(os.path.join(ABS_PATH_TO_DIRECTORY, FILE_TYPES)):
        to_upload.append(image_file)

    pool = Pool(CONCURRENT_UPLOADS)
    pool.map(upload, to_upload)
    pool.close()
    pool.join()

if __name__ == "__main__":
    go()
