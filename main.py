from matplotlib import pyplot as plt
import numpy as np


class FFT:
    def __init__(self):
        self.__data = []
        self.__data_noisy = []
        self.__data_2d = []
        self.__dft_frequencies = []
        self.__modules = []
        self.__fft_frequencies = []

    def run(self):
        self.__scrape_data()
        self.__dft_frequencies = self.__dft(self.__data)
        self.__fft_frequencies = self.__fft(self.__data)
        self.__calc_modules(self.__data, self.__fft_frequencies)

    def __scrape_data(self):
        files = ["dane_02.in", "dane_02_a.in", "dane2_02.in"]
        lists = [self.__data, self.__data_noisy, self.__data_2d]

        for file, data_list in zip(files, lists):
            with open(file) as f:
                lines = f.read().splitlines()

            if file == "dane2_02.in":
                for line in lines[2:]:
                    row_data = list(map(float, line.split()))
                    data_list.append(row_data)
                continue

            for line in lines[2:]:
                try:
                    data_list.append(float(line))
                except ValueError:
                    print(f"Could not convert {line} to float")

    def __dft (self, x):
        N = len(x)
        X = np.zeros(N, dtype=complex)

        for k in range(N):
            for n in range(N):
                X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)

        return X

    def __fft(self, x):
        N = len(x)
        if N <= 1:
            return x

        # Even/odd element splitting
        even = self.__fft(x[0::2])
        odd = self.__fft(x[1::2])

        # Combine
        T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
        return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

    def __count_operations(self):
        pass

    def __calc_modules(self, data, frequencies):
        for x in range(len(data)):
            module = np.abs(frequencies[x])
            self.__modules.append(module)

    def plot_frequencies(self, modules):
        sample_num = range(len(modules))
        plt.plot(sample_num, self.__modules)
        plt.title("FFT frequencies")
        plt.xlabel("Sample number")
        plt.ylabel("Frequencies")
        plt.show()

    def get_dft_frequencies(self):
        return self.__dft_frequencies

    def get_fft_frequencies(self):
        return self.__fft_frequencies

    def get_modules(self):
        return self.__modules


def main():

    f = FFT()
    f.run()
    f.plot_frequencies(f.get_modules())

    return 0


if __name__ == "__main__":
    main()
