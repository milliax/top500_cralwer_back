import time
import matplotlib.pyplot as plt
import uuid
import os
import numpy as np


def time_parser(Ltime):
    Ltime = int(Ltime) / 1000
    Ltime = time.localtime(Ltime)

    date = {"year": Ltime.tm_year, "month": Ltime.tm_mon}

    if date['month'] > 11:
        date['month'] = 11
    elif date['month'] > 6:
        date['month'] = 6
    else:
        date['month'] = 11
        date['year'] -= 1

    return date


def generate_plot(props):
    """ generate plot """
    if not ("method" in props):
        props["method"] = "pie"

    plt.figure(figsize=(10,5))
    if props["method"] == "pie":
        y = np.array(props["data"])
        percent = 100.*y/y.sum()
        patches, texts = plt.pie(y,startangle=90)
        labels = ["{label}: {percentage:1.2f}%".format(label=label, percentage=percentage) for (
            label, percentage) in zip(props["labels"], percent)]

        plt.legend(patches, labels, loc="best",
                   bbox_to_anchor=(-0.1, 1.), fontsize=12)

    root_folder = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    ))

    """ saving plot """
    filename = "{uuid}.png".format(uuid=generate_uuid(6))
    plt.savefig(filename, dpi=300)

    """ moving plot to correct folder """
    original = os.path.join(root_folder, filename)
    new = os.path.join(root_folder, "python/static", filename)
    os.replace(original, new)

    return filename


def generate_uuid(number):
    return uuid.uuid4().hex[:number].upper()
