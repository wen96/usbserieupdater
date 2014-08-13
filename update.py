#! python
import sys
import re


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
            if not cls.is_chapter(cls.chapter_str()):
                raise ArgumentException("The chapter format must be: SxC\n" +
                                        "\t Where S is seasson number and C " +
                                        "is chapter number")

            ChapterUpdater(
                path_from=cls.path_from(),
                path_to=cls.path_to(),
                seasson=cls.seasson(),
                chapter=cls.chapter()).run()
        else:
            raise ArgumentException("Bad syntax in parameters")

    @classmethod
    def is_chapter(cls, chapter):
        return re.match("^([0-9])+x([0-9])+$", chapter)

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

    @classmethod
    def seasson(cls):
        return int(cls.chapter_str().split("x")[0])

    @classmethod
    def chapter(cls):
        return int(cls.chapter_str().split("x")[1])


class ArgumentException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ChapterUpdater():
    path_from = ""
    path_to = ""
    seasson = 0
    chapter = 0

    def run(self):
        pass


try:
    ArgvProcessor.process()
except ArgumentException as e:
    print 'Arguments error:' + str(e)
