import os


def save_file(df, dir_path, filename):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        df.to_csv(dir_path + filename, index=False, encoding='utf8')
    else:
        df.to_csv(dir_path + filename, index=False, encoding='utf8')
