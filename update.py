#! python
import sys
import os
import re
import ctypes
import platform
import shutil


class ArgvProcessor:
    MIN_N_ARGV = 2
    MAX_n_ARGV = 4

    ARGUMENTS_MODE = 2

    @classmethod
    def process(cls):
        cls.n_arguments = len(sys.argv)

        if cls.n_arguments < cls.MIN_N_ARGV or\
                cls.n_arguments > cls.MAX_n_ARGV or\
                sys.argv[1] in ("-h", "--help"):
            print "usage: ./update.py <path_from_folder>" +\
                "<path_folder_to_update> SxC\n"
        elif cls.n_arguments is 2:
            print "TO-DO"
        elif cls.n_arguments is 4:
            cls.ARGUMENTS_MODE = 1

            chapter = Chapter(cls.chapter_str())
            updater = ChapterUpdater()
            updater.path_from = cls.path_from()
            updater.path_to = cls.path_to()
            updater.chapter = chapter
            updater.run()
        else:
            raise ArgumentException("Bad syntax in parameters")

    @classmethod
    def path_from(cls):
        return sys.argv[1]

    @classmethod
    def path_to(cls):
        return sys.argv[2]

    @classmethod
    def chapter_str(cls):
        if cls.ARGUMENTS_MODE is 1:
            return sys.argv[3]
        else:
            return sys.argv[1]


class ArgumentException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ChapterUpdater:
    path_from = ""
    path_to = ""
    chapter = None

    def run(self):
        self.remove_before()
        self.copy_news()

    def copy_news(self):
        for filename in os.listdir(self.path_from):
            chapter_str = self.extract_chapter_str(filename)
            if Chapter(chapter_str) >= self.chapter:
                if not self.is_in_destination(filename):
                    if self.destination_have_engouth_space(filename):
                        print "Copying " + filename
                        shutil.copyfile(self.path_from + filename,
                                        self.path_to + filename)

    def destination_have_engouth_space(self, new_chapter):
        new_file_complete_path = self.path_from + new_chapter
        return FilesystemHelper.get_size_bytes(new_file_complete_path) <\
            self.device_size()

    def is_in_destination(self, filename):
        chapter_str = self.extract_chapter_str(filename)
        new_chapter = Chapter(chapter_str)
        for filename in os.listdir(self.path_to):
            chapter_str = self.extract_chapter_str(filename)
            if chapter_str:
                if Chapter(chapter_str) == new_chapter:
                    return True

    def device_size(self):
        return FilesystemHelper.get_free_space_bytes(self.path_to)

    def remove_before(self):
        for filename in os.listdir(self.path_to):
            chapter_str = self.extract_chapter_str(filename)
            if chapter_str:
                if Chapter(chapter_str) < self.chapter:
                    print "Removing " + filename
                    os.remove(self.path_to + filename)

    def extract_chapter_str(self, string_file):
        chapter_str = re.search(Chapter.regex_chapter, string_file)
        if chapter_str:
            return chapter_str.group(0)
        else:
            return None


class Chapter:
    seasson = 0
    chapter = 0
    regex_chapter = "([0-9])+x([0-9])+"

    def __init__(self, chapter_string):
        if not self.is_chapter(chapter_string):
            raise ArgumentException("The chapter format must be: SxC\n" +
                                    "\t Where S is seasson number and C " +
                                    "is chapter number. Get it " +
                                    chapter_string)
        self.seasson = self.seasson(chapter_string)
        self.chapter = self.chapter(chapter_string)

    def is_chapter(self, chapter):
        complete_regex = "^" + self.regex_chapter + "$"
        return re.match(complete_regex, chapter)

    def seasson(self, chapter_string):
        return int(chapter_string.split("x")[0])

    def chapter(self, chapter_string):
        return int(chapter_string.split("x")[1])

    def __lt__(self, other):
        if (self.seasson == other.seasson):
            return self.chapter < other.chapter
        else:
            return self.seasson < other.seasson

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        return self.chapter == other.chapter and self.seasson == other.seasson


class FilesystemHelper:
    @classmethod
    def get_free_space_bytes(cls, folder):
        """ Return folder/drive free space (in bytes)
        """
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(folder), None, None, ctypes.pointer(
                    free_bytes))
            return free_bytes.value
        else:
            st = os.statvfs(folder)
            return st.f_bavail * st.f_frsize

    @classmethod
    def get_size_bytes(cls, file):
        return os.stat(file).st_size

try:
    ArgvProcessor.process()
except ArgumentException as e:
    print 'Arguments error:' + str(e)
