#include <string>
#include "image.hpp"
#include "hw6.hpp"
#include <iostream>
#define BOOST_DISABLE_ASSERTS
#include <boost/multi_array.hpp>

image::image(std::string name)
{
    ReadGrayscaleJPEG(name, data);
    file_name = name;
}
void image::Save(std::string save_name)
{
    if (save_name.empty())
    {
        // If save name is not provided, original file name is used
        save_name = file_name;
    }

    //Input name is stored and current data is written
    WriteGrayscaleJPEG(save_name, data);
}
void image::Convolution(boost::multi_array<unsigned char, 2> &input,
                        boost::multi_array<unsigned char, 2> &output,
                        boost::multi_array<float, 2> &kernel)
{
    if ((input.shape()[0] == output.shape()[0]) &&
        (input.shape()[1] == output.shape()[1]) &&
        (kernel.shape()[0] % 2 == 1) &&
        (kernel.shape()[0] == kernel.shape()[1]) &&
        (kernel.shape()[0] >= 3))
    // Checking if input and output are of the same size and odd,
    // with square kernels of at least size 3.
    {
        //Initializing the variables for size of data
        unsigned int ext = ((unsigned int)kernel.shape()[0] - 1) / 2;
        //ext is the pixel number required to extend image for boundary pixels
        unsigned int m1 = (unsigned int)input.shape()[0];
        unsigned int m2 = (unsigned int)input.shape()[1];
        unsigned int n = (unsigned int)kernel.shape()[0];
        boost::multi_array<unsigned char, 2> data_extended(boost::extents[m1 + 2 * ext][m2 + 2 * ext]);
        // data_extended is the 2D multi array with 2*ext extra rows and columns
        boost::multi_array<unsigned char, 2> mat(boost::extents[n][n]);
        // mat is a 2D multi array which consists of surrounding pixel data
        typedef boost ::multi_array<double, 2>::index_range index_range;
        auto data_view = data_extended[boost::indices[index_range(ext, m1 + ext)][index_range(ext, m2 + ext)]];
        // View range for data_extended
        for (unsigned int i = 0; i < m1; i++)
        {
            for (unsigned int j = 0; j < m2; j++)
            {
                data_view[i][j] = input[i][j];
                // data_extended's center is filled with image data
            }
        }
        for (unsigned int i = 0; i < ext; i++)
        {
            for (unsigned int j = 0; j < ext; j++)
            {
                data_extended[i][j] = input[0][0];
                data_extended[i + m1 - 1 + ext][j] = input[m1 - 1][0];
                data_extended[i][j + m2 - 1 + ext] = input[0][m2 - 1];
                data_extended[i + m1 - 1 + ext][j + m2 - 1 + ext] = input[m1 - 1][m2 - 1];
                // Corners are filled
            }
        }
        // Filling left extension
        for (unsigned int i = ext; i < m1 + ext; i++)
        {
            for (unsigned int j = 0; j < ext; j++)
            {
                data_extended[i][j] = data[i - ext][0];
            }
        }
        // Filling right extension
        for (unsigned int i = ext; i < m1 + ext; i++)
        {
            for (unsigned int j = m2 + ext - 1; j < m2 + 2 * ext; j++)
            {
                data_extended[i][j] = data[i - ext][m2 - 1];
            }
        }
        // Filling top extension
        for (unsigned int i = 0; i < ext; i++)
        {
            for (unsigned int j = ext; j < m2 + ext; j++)
            {
                data_extended[i][j] = data[0][j - ext];
            }
        }
        // Filling bottom extension
        for (unsigned int i = m1 + ext - 1; i < m1 + 2 * ext; i++)
        {
            for (unsigned int j = ext; j < m2 + ext; j++)
            {
                data_extended[i][j] = data[m1 - 1][j - ext];
            }
        }
        // After getting data_extended, looping over pixels
        for (unsigned int i = 0; i < m1; i++)
        {
            for (unsigned int j = 0; j < m2; j++)
            {
                mat = data_extended[boost::indices[index_range(i, i + n)][index_range(j, j + n)]];
                // mat is the surrounding pixels 2D array
                float sum = 0.;
                for (unsigned int k = 0; k < n; k++)
                {
                    for (unsigned int l = 0; l < n; l++)
                    {
                        sum = sum + ((float)(mat[k][l])) * ((float)(kernel[k][l]));
                        // Elementwise multiplication and summation
                    }
                }
                if (round(sum) > 255.)
                {
                    // Upper limit for final value for pixel
                    sum = 255.;
                }
                if (round(sum) < 0.)
                {
                    sum = 0.;
                    // Lower limit for final value for pixel
                }
                output[i][j] = (unsigned char)(sum);
            }
        }
    }
    else
    {
        std::cout << "Input/Output conflict." << std::endl;
        exit(EXIT_FAILURE);
    }
}
void image::BoxBlur(unsigned int kernel_size)
{
    // Declaring the kernel
    boost::multi_array<float, 2> kernel(boost::extents[kernel_size][kernel_size]);
    for (unsigned int i = 0; i < kernel_size; i++)
    {
        for (unsigned int j = 0; j < kernel_size; j++)
        {
            // kernels values are 1/(n^2) for size n kernel
            float n = float(kernel_size);
            kernel[i][j] = (float)1. / (n * n);
        }
    }
    boost::multi_array<unsigned char, 2> output(boost::extents[data.shape()[0]][data.shape()[1]]);
    Convolution(data,
                output,
                kernel);
//--design_0
//--Correct use of this (optional in this context).
//--START
    this->data = output;
//--END
}

unsigned int image::Sharpness(void)
{
    // Declaring variables
    boost::multi_array<float, 2> kernel(boost::extents[3][3]);
    boost::multi_array<unsigned char, 2> output(boost::extents[data.shape()[0]][data.shape()[1]]);
    unsigned int m1 = (unsigned int) data.shape()[0];
    unsigned int m2 = (unsigned int) data.shape()[1];
    unsigned int max_pix = 0;
    unsigned int current_pix;
    // Laplacian operator initialized
    kernel[0][0] = 0.;
    kernel[0][1] = 1.;
    kernel[0][2] = 0.;
    kernel[1][0] = 1.;
    kernel[1][1] = -4.;
    kernel[1][2] = 1.;
    kernel[2][0] = 0.;
    kernel[2][1] = 1.;
    kernel[2][2] = 0.;
    Convolution(data,
                output,
                kernel);
    for (unsigned int i = 0; i < m1; i++)
    {
        for (unsigned int j = 0; j < m2; j++)
        {
            current_pix = (unsigned int)output[i][j];
            if (current_pix > max_pix)
            {
                // Looping over each pixel, comparing it with the current max
                max_pix = current_pix;
            }
        }
    }
    return max_pix;
}

//--design_0
//--Good commenting. The frequency of comments is appropriate and feels like
//--I'm being guided through the code. Well done!
//--For the image extension part, the logic certainly seems correct.
//--One way you could have succinctly execute the boundary computations was
//--to cap the indices outside [0, num_pixels_in_image_length - 1] to the
//--nearest boundary value by taking the index i and computing
//--  y = max(0, i)
//--  z = min(y, num_pixels_in_image_length-1)
//--where z is your new index; do the same for j.
//--Then these new indices used on your original image will give you the
//--extended image values at the original i, j.
//--
//--In general, succinct code is less error-prone and easier to read!
//--END
