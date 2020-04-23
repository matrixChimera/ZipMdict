# _*_ coding:utf-8 _*_
# Developer: https://github.com/maomaowei5655
# Time: 2020/4/23
# File name: ZipMdict_0.1e.py
# IDE: PyCharm

import os
import re
import tkinter
import tkinter.filedialog
import tkinter.messagebox

from readmdict import *
import sys
import os.path
import argparse
import codecs




# Some global variables:
read_path = ''  # the path of the .mdx/.mdd file that will be unzipped
read_number_report = ''  # the message that will pop up after unzipping
def read_mdict():
    """
    Unzip/Read button's command: unzip/read a file that ends with "mdx"/"mdd" into files.
    (Adapted from "readmdict", cf. https://jingyan.baidu.com/article/95c9d20d47583bec4e756132.html)

    Returns:
        If successful, internal files of .mdx/.mdd will appear in a folder (named ""Unzipped_mdx)
            in the same folder as .mdx/.mdd, and an messagebox will pop up showing the number of entries in .mdx
            or the number of files in .mdd.
        If failed, an errorbox will pop up requesting you to specify a valid MDX/MDD file.

    """
    def passcode(s):
        try:
            regcode, userid = s.split(',')
        except:
            raise argparse.ArgumentTypeError("Passcode must be regcode,userid")
        try:
            regcode = codecs.decode(regcode, 'hex')
        except:
            raise argparse.ArgumentTypeError("regcode must be a 32 bytes hexadecimal string")
        return regcode, userid

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--extract', action="store_true",
                        help='extract mdx to source format and extract files from mdd')
    parser.add_argument('-s', '--substyle', action="store_true",
                        help='substitute style definition if present')
    # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
    parser.add_argument('-d', '--datafolder', default="Unzipped_mdd",
                        help='folder to extract data files from mdd')
    parser.add_argument('-e', '--encoding', default="",
                        help='folder to extract data files from mdd')
    parser.add_argument('-p', '--passcode', default=None, type=passcode,
                        help='register_code,email_or_deviceid')
    parser.add_argument("filename", nargs='?', help="mdx file name")
    args = parser.parse_args()

    if not args.filename:
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        args.filename = read_path
        args.extract = True

    # Extract the base and extension (.后缀名) of the file path:
    base, ext = os.path.splitext(args.filename)

    # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
    # If the file path is none or the extension of the file path is not either .mdx or .mdd, errors will pop up:
    if (not os.path.exists(args.filename)) or (read_path=='') or (ext.lower() not in ['.mdx', '.mdd']):
        print("Please specify a valid MDX/MDD file")
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        # region Messagebox for error:
        tkinter.messagebox.showerror('Error', "Please specify a valid MDX/MDD file")
        # endregion

    # read mdx file
    if ext.lower() == os.path.extsep + 'mdx':
        mdx = MDX(args.filename, args.encoding, args.substyle, args.passcode)
        if type(args.filename) is unicode:
            bfname = args.filename.encode('utf-8')
        else:
            bfname = args.filename
        print('======== %s ========' % bfname)
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        global read_number_report
        read_number_report = '  Number of Entries : %d' % len(mdx)
        print(read_number_report)
        for key, value in mdx.header.items():
            print('  %s : %s' % (key, value))
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        # region Messagebox for reporting outcome:
        tkinter.messagebox.showinfo('Output', '''Read/Unzip: \n\t{}\n
Output: \n\t{}'''.format(read_path.split(os.path.sep)[-1], read_number_report))
        # endregion
    else:
        mdx = None

    # read mdd file
    if ext.lower() == os.path.extsep + 'mdd':
        mdd_filename = ''.join([base, os.path.extsep, 'mdd'])
        mdd = MDD(mdd_filename, args.passcode)
        if type(mdd_filename) is unicode:
            bfname = mdd_filename.encode('utf-8')
        else:
            bfname = mdd_filename
        print('======== %s ========' % bfname)
        read_number_report = '  Number of files : %d' % len(mdd)
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        print(read_number_report)
        for key, value in mdd.header.items():
            print('  %s : %s' % (key, value))
        print(mdd.header)
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        # region Messagebox for reporting outcome:
        tkinter.messagebox.showinfo('Output', '''Read/Unzip: \n\t{}\n
Output: \n\t{}'''.format(read_path.split(os.path.sep)[-1], read_number_report))
        # endregion
    else:
        mdd = None

    if args.extract:
        # write out glos
        if mdx:
            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            folder_name = re.search(r'^.*{}'.format(os.path.sep), base).group() + 'Unzipped_mdx'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            output_fname = folder_name + os.path.sep + base.split(os.path.sep)[-1] + '.txt'
            tf = open(output_fname, 'wb')
            for key, value in mdx.items():
                tf.write(key)
                tf.write(b'\r\n')
                tf.write(value)
                if not value.endswith(b'\n'):
                    tf.write(b'\r\n')
                tf.write(b'</>\r\n')
            tf.close()
            # write out style
            if mdx.header.get('StyleSheet'):
                # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
                folder_name = re.search(r'^.*{}'.format(os.path.sep), base).group()
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
                style_fname = ''.join([folder_name, '_style', os.path.extsep, 'txt'])
                sf = open(style_fname, 'wb')
                sf.write(b'\r\n'.join(mdx.header['StyleSheet'].splitlines()))
                sf.close()
        # write out optional data files
        if mdd:
            datafolder = os.path.join(os.path.dirname(args.filename), args.datafolder)
            if not os.path.exists(datafolder):
                os.makedirs(datafolder)
            for key, value in mdd.items():
                fname = key.decode('utf-8').replace('\\', os.path.sep)
                dfname = datafolder + fname
                if not os.path.exists(os.path.dirname(dfname)):
                    os.makedirs(os.path.dirname(dfname))
                df = open(dfname, 'wb')
                df.write(value)
                df.close()


# Some global variables:
write_path = ''  # the path of the .txt file that will be zipped
write_number_report = ''  # the message that will pop up after zipping
def write_mdict():
    """
        Zip/Write button's command: zip/write .txt files into a file that ends with "mdx"/"mdd".
        (Adapted from "readmdict", cf. https://jingyan.baidu.com/article/95c9d20d47583bec4e756132.html)

        Returns:
            If successful, internal files of .mdx/.mdd will appear in a folder (named ""Unzipped_mdx)
                in the same folder as .mdx/.mdd, and an messagebox will pop up showing the number of entries in .mdx
                or the number of files in .mdd.
            If failed, an errorbox will pop up requesting you to specify a valid MDX/MDD file.

    """
    import io
    import sys
    import importlib
    importlib.reload(sys)
    import collections
    from collections import defaultdict
    from writemdict import MDictWriter, encrypt_key
    from ripemd128 import ripemd128

    # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
    if write_path.split(os.path.sep)[-1].endswith('mdx'):
        # Zip files (dictionary_name.txt (and about.txt)) into .mdx
        # Delete .DS_Store in Mac:
        files_in_write_path = os.listdir(write_path)
        if '.DS_Store' in files_in_write_path:
           files_in_write_path.remove('.DS_Store')
        # The folder can only have at most 2 files:
        if len(files_in_write_path) > 2:
            tkinter.messagebox.showerror('Error', "The number of files in the folder must be <=2.")
        elif len(files_in_write_path) == 0:
            tkinter.messagebox.showerror('Error', "The number of files in the folder must be <=2.")
        elif len(files_in_write_path) == 1:
            # When the folder only has one .txt including entries
            global dictionary_txt
            dictionary_txt = files_in_write_path[0]

            head = 0
            new_mean = []
            f = io.open(os.path.join(write_path, dictionary_txt), 'r', encoding='utf-8')
            d = defaultdict(list)  # 建立一个空字典，也可使用{}建立。
            for line in f:  # 每次从f中读入一行
                line = line.rstrip('\n')  # 去除行尾的换行符
                if line == '</>':
                    if head == 2:
                        new_mean[0:] = ["".join(new_mean[0:])]
                        d[word].append(new_mean[0])
                    head = 1;
                    new_mean = []
                elif head == 1:
                    word = line
                    head = 2
                elif head == 2:
                    new_mean.append(line)
                    head = 2
            f.close()

            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            if not os.path.exists(os.path.join(write_path, 'Zipped_mdx')):
                os.makedirs(os.path.join(write_path, 'Zipped_mdx'))
            outfile_mdx = open(os.path.join(write_path, 'Zipped_mdx', dictionary_txt.split(os.path.extsep)[0] + '.mdx'),
                               "wb")
            writer = MDictWriter(d, dictionary_txt.split(os.path.extsep)[0], dictionary_txt.split(os.path.extsep)[0])
            writer.write(outfile_mdx)
            outfile_mdx.close()
            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            print('======== {} ========'.format(write_path))
            global write_number_report
            write_number_report = '{}.mdx'.format(dictionary_txt.split(os.path.extsep)[0])
            print('Output: {}'.format(write_number_report))
            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            # region Messagebox for reporting outcome:
            tkinter.messagebox.showinfo('Output',
                                        'Write/Zip: \n\t{}\n\nOutput: \n\t{}'.format(write_path, write_number_report))
            # endregion
        else:
            # When the folder have two .txt files including entries and about_information
            for file in files_in_write_path:
                if not file.startswith('about'):
                    dictionary_txt = file
                else:
                    global about_txt
                    about_txt = file

            head = 0
            new_mean = []
            f = io.open(os.path.join(write_path, dictionary_txt), 'r', encoding='utf-8')
            d = defaultdict(list)  # 建立一个空字典，也可使用{}建立。
            for line in f:  # 每次从f中读入一行
                line = line.rstrip('\n')  # 去除行尾的换行符
                if line == '</>':
                    if head == 2:
                        new_mean[0:] = ["".join(new_mean[0:])]
                        d[word].append(new_mean[0])
                    head = 1;
                    new_mean = []
                elif head == 1:
                    word = line
                    head = 2
                elif head == 2:
                    new_mean.append(line)
                    head = 2
            f.close()


            ff = io.open(os.path.join(write_path, about_txt), 'r', encoding='utf-8')  # 词典about信息，txt文件请保存为utf-8
            about = []
            for line in ff:  # 每次从f中读入一行
                about.append(line)
            about[0:] = ["".join(about[0:])]

            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            if not os.path.exists(os.path.join(write_path, 'Zipped_mdx')):
                os.makedirs(os.path.join(write_path, 'Zipped_mdx'))
            outfile_mdx = open(os.path.join(write_path, 'Zipped_mdx', dictionary_txt.split(os.path.extsep)[0]+'.mdx'), "wb")
            writer = MDictWriter(d, dictionary_txt.split(os.path.extsep)[0], about[0])
            writer.write(outfile_mdx)
            outfile_mdx.close()
            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            print('======== {} ========'.format(write_path))
            write_number_report = '{}.mdx'.format(dictionary_txt.split(os.path.extsep)[0])
            print('Output: {}'.format(write_number_report))
            # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
            # region Messagebox for reporting outcome:
            tkinter.messagebox.showinfo('Output', 'Write/Zip: \n\t{}\n\nOutput: \n\t{}'.format(write_path, write_number_report))
            # endregion
    # elif write_path.split(os.path.sep)[-1].endswith('mdd'):
        # # Zip files in mdd
        # folder_name = re.search(r'^.*{}'.format(os.path.sep), write_path).group() + 'Zipped_mdd'
        # if not os.path.exists(folder_name):
        #     os.makedirs(folder_name)
        # outfile_name = os.path.join(folder_name, write_path.split(os.path.sep)[-1])
        # for file in os.listdir(write_path):
        #     if file.lower().endswith('png'or'gif'or'jpg'or'jpeg'or'css'):
        #         file_object = open(os.path.join(write_path, file), 'rb')
        #         file_contents = file_object.read()
        #         outfile_mdd = open(outfile_name, 'wb')
        #         d = {"\\{}".format(file) : file_contents}
        #         writer = MDictWriter(d, file.split('.')[0], file, is_mdd=True)
        #         writer.write(outfile_mdd)
        #         file_object.close()
        #         outfile_mdd.close()
        #     else:
        #         file_object = open(os.path.join(write_path, file), 'r', encoding='utf-8', errors='ignore')
        #         file_contents = file_object.read()
        #         outfile_mdd = open(outfile_name, 'w')
        #         d = {"\\{}".format(file): file_contents}
        #         writer = MDictWriter(d, file.split('.')[0], file, is_mdd=True)
        #         writer.write(outfile_mdd)
        #         file_object.close()
        #         outfile_mdd.close()
        # write_number_report = outfile_name
        # print('Output: {}'.format(write_number_report))
        # # region Messagebox for reporting outcome:
        # tkinter.messagebox.showinfo('Output', 'Write/Zip: \n\t{}\n\nOutput: \n\t{}'.format(write_path, write_number_report))
        # # endregion
    else:
        # Modified by 掌上百科@maomaowei5655 in 2020-04-23:
        print('Please put files in a folder suffixed mdx/mdd.')
        # region Messagebox for error:
        tkinter.messagebox.showerror('Error', "Please specify a valid MDX file.")
        # endregion





# region GUI
main_window = tkinter.Tk()
main_window.title('Unzip & Zip mdict')

# region Center the main window
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
# Define the width and height of the main window:
main_window_width = 800
main_window_height = 450
x = (screen_width - main_window_width) / 2
y = (screen_height - main_window_height) / 2
main_window.geometry("%dx%d+%d+%d" % (main_window_width, main_window_height, x, y))
# endregion

def file_path_select():
    global read_path
    read_path = tkinter.filedialog.askopenfilename()
    # Set the contents of path entry box:
    file_path.set(read_path)
# region Define the label, entry, and button of unzipping/reading
file_path = tkinter.StringVar()
label_file_path = tkinter.Label(main_window, text="File:").place(relx=4/72, rely=36/72, anchor='center')
entry_file_path = tkinter.Entry(main_window, textvariable=file_path, width=int(main_window_width * 0.085))
entry_file_path.place(relx=0.5, rely=9/18, anchor='center')
button_file_path = tkinter.Button(main_window, text="Choose", command=file_path_select)
button_file_path.place(relx=17/18, rely=18/36, anchor='center')
# endregion


def folder_path_select():
    global write_path
    write_path = tkinter.filedialog.askdirectory()
    # Set the contents of path entry box:
    folder_path.set(write_path)
# region Define the label, entry, and button of zipping/writing
folder_path = tkinter.StringVar()
label_folder_path = tkinter.Label(main_window, text="Folder:").place(relx=4/72, rely=108/144, anchor='center')
entry_folder_path = tkinter.Entry(main_window, textvariable=folder_path, width=int(main_window_width * 0.085))
entry_folder_path.place(relx=0.5, rely=27/36, anchor='center')
button_folder_path = tkinter.Button(main_window, text="Choose", command=folder_path_select)
button_folder_path.place(relx=17/18, rely=27/36, anchor='center')
# endregion

# region Create unzip/zip button
button_unzip = tkinter.Button(text='Unzip', width=6, fg='#2264d9', command=read_mdict)
button_zip = tkinter.Button(text='Zip', width=6, fg='#2264d9', command=write_mdict)
# Place the button via relative coordinates
button_unzip.place(relx=0.5, rely=21/36, anchor='center')
button_zip.place(relx=0.5, rely=30/36, anchor='center')
# endregion

img_logo = tkinter.PhotoImage(file='logo_128.png')
img_label = tkinter.Label(main_window, image=img_logo)
img_label.place(relx=0.5, rely=4/18, anchor='center')

label_right = tkinter.Label(main_window, fg='#d5d5d5', font=('Arial', 10),
                            text='''Developer: 掌上百科@maomaowei5655 (https://www.pdawiki.com/forum/space-uid-259358.html); GitHub@matrixChimera (https://github.com/matrixChimera)
Acknowledgements: 掌上百科@lgmcw; GitHub@zhansliu(https://github.com/zhansliu/writemdict)''')
label_right.place(relx=0.5, rely=140/144, anchor='center')


main_window.mainloop()
# endregion