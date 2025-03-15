from spleeter.separator import Separator


if __name__ == '__main__':
    separator = Separator("spleeter:2stems")
    separator.separate_to_file("data/노래명.mp3", "splt")