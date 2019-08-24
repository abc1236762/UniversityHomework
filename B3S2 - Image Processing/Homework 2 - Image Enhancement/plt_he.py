from matplotlib import pyplot
import cv2
import numpy

Image = numpy.ndarray


def power_low_transformation(img: Image, gamma: float) -> Image:
    return numpy.array(255 * (img / 255) ** gamma, dtype="uint8")


def histogram_equalization(img: Image) -> Image:
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)


def save_histogram(img: Image, fig_name: str):
    fig, ax = pyplot.subplots(1, 3)
    fig.set_size_inches(20, 6)
    colors = ("r", "g", "b")
    for ch_i, color, each_ax in zip(range(2, -1, -1), colors, ax.flat):
        hist = cv2.calcHist([img], [ch_i], None, [256], [0, 256])
        each_ax.set_xlim(0, 256)
        each_ax.bar(range(1, 257), hist.flatten(), color=color)
    pyplot.savefig(fig_name, format="png")
    pyplot.clf()


def main(img_name: str):
    img = cv2.imread(img_name + ".jpg")
    save_histogram(img, "{}-hist.png".format(img_name))
    img_t1 = power_low_transformation(img, 4)
    img_t2 = power_low_transformation(img, 1 / 4)
    cv2.imwrite("{}-t4_00.png".format(img_name), img_t1)
    cv2.imwrite("{}-t0_25.png".format(img_name), img_t2)
    save_histogram(img_t1, "{}-t4_00-hist.png".format(img_name))
    save_histogram(img_t2, "{}-t0_25-hist.png".format(img_name))
    img_e = histogram_equalization(img)
    cv2.imwrite("{}-e.png".format(img_name), img_e)
    save_histogram(img_e, "{}-e-hist.png".format(img_name))

if __name__ == "__main__":
    main("bright")
    main("dark")
    main("gray")
    main("normal")
