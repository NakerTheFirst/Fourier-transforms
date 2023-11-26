from matplotlib import pyplot as plt
import numpy as np
import sys


class FFT:
    def __init__(self):
        self.__data = []
        self.__data_noisy = []
        self.__data_2d = []
        self.__dft_frequencies = []
        self.__amplitudes = []
        self.__fft_frequencies = []
        self.__dft_op_counter = 0
        self.__fft_op_counter = 0

    def run(self):
        # Remains here for the use of testing
        self.__scrape_data()

        # TODO: Uncomment before handing in the final programme
        # self.__scrape_data_final()

        # Perform the transformations
        self.__dft_frequencies = self.__threshold_list(self.__dft(self.__data))
        self.__fft_frequencies = self.__threshold_list(self.__fft(self.__data))
        self.__calc_amplitudes()

        print(self.__dft_frequencies)

        print(f"DFT operations: {self.__dft_op_counter}")
        print(f"FFT operations: {self.__fft_op_counter}")

        # Plotting
        self.plot_signal(self.__data)
        self.plot_amplitudes()

        # Inverse
        signal_dft_inverse = self.__idft(self.__dft_frequencies)
        signal_fft_inverse = self.__idft(self.__fft_frequencies)

        # Plot inverted signals to compare to the initial ones
        self.plot_signal(signal_dft_inverse, "Post IDFT signal")
        self.plot_signal(signal_fft_inverse, "Post IFFT signal")

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

    def __scrape_data_final(self):
        # Read the dimension
        dimensionality = int(input().strip())

        # Read the number of elements
        dimensions = list(map(int, input().strip().split()))

        # Initialize the data container
        if dimensionality == 1:
            N = dimensions[0]
            self.__data = [float(input().strip()) for _ in range(N)]
        elif dimensionality == 2:
            N, M = dimensions
            self.__data_2d = [[float(num) for num in input().strip().split()] for _ in range(N)]
        else:
            raise ValueError("Dimensionality must be 1 or 2")

    def __dft(self, x):
        N = len(x)
        X = np.zeros(N, dtype=complex)

        for k in range(N):
            for n in range(N):
                X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
                self.__dft_op_counter += 1

        return X

    def __fft(self, x):
        N = len(x)
        if N <= 1:
            return x

        # Even/odd element splitting
        even = self.__fft(x[0::2])
        odd = self.__fft(x[1::2])

        # Combine
        combined = [0] * N
        for k in range(N // 2):
            twiddle_factor = np.exp(-2j * np.pi * k / N) * odd[k]
            combined[k] = even[k] + twiddle_factor
            combined[k + N // 2] = even[k] - twiddle_factor

            # Count 2 operations (1 multiplication, 1 addition)
            self.__fft_op_counter += 2

        return combined

    def __idft(self, x):
        N = len(x)
        X = np.zeros(N, dtype=complex)

        for n in range(N):
            for k in range(N):
                X[n] += x[k] * np.exp(2j * np.pi * k * n / N)
            X[n] /= N

        return X

    def __ifft(self, x):
        N = len(x)
        if N <= 1:
            return x

        # Split the signal into even and odd indexed elements
        even = self.__ifft(x[0::2])
        odd = self.__ifft(x[1::2])

        # Combine
        combined = [0] * N
        for k in range(N // 2):
            twiddle_factor = np.exp(2j * np.pi * k / N) * odd[k]
            combined[k] = even[k] + twiddle_factor
            combined[k + N // 2] = even[k] - twiddle_factor

        # Normalize the results by the number of samples
        combined = [elem / N for elem in combined]

        return combined

    def __calc_amplitudes(self):
        for x in range(len(self.__data)):
            amplitude = np.abs(self.__fft_frequencies[x])
            self.__amplitudes.append(amplitude)

    def __threshold_list(self, input_list, epsilon=0.0005) -> list:
        """If list values are lower than epsilon, set them to 0"""
        def threshold_value(value):
            return 0 if abs(value) < epsilon else value

        # 1D list
        if all(isinstance(i, (int, float, complex)) for i in input_list):
            return [threshold_value(x) for x in input_list]

        # 2D list
        elif all(isinstance(row, list) for row in input_list):
            return [[threshold_value(x) for x in row] for row in input_list]

        else:
            raise ValueError("Input must be a 1D or 2D list of numbers")

    def plot_amplitudes(self):
        sample_num = range(len(self.__amplitudes))
        plt.scatter(sample_num, self.__amplitudes, s=15)
        plt.title("FFT Amplitudes")
        plt.xlabel("Sample number")
        plt.ylabel("Amplitudes")
        plt.grid(True)
        plt.show()

    # TODO: This doesn't work, unsure what to do - move on, get back later
    def plot_magnitude_spectrum(self):
        plt.scatter(self.__fft_frequencies, self.__amplitudes)
        plt.title("FFT Magnitude Spectrum")
        plt.xlabel("Frequencies")
        plt.ylabel("Amplitudes")
        plt.grid(True)
        plt.show()

    def plot_signal(self, signal, title="Discretised Signal in Time Domain"):
        plt.scatter(range(len(signal)), signal, s=15)
        plt.title(title)
        plt.xlabel("Sample number")
        plt.ylabel("Value")
        plt.grid(True)
        plt.show()


def main():

    f = FFT()
    f.run()

    return 0


if __name__ == "__main__":
    main()
