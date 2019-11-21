#ifndef IMAGE_HPP
#define IMAGE_HPP
#include <string>
#include <boost/multi_array.hpp>

class image
{   
    std::string file_name;
    boost::multi_array<float, 2> kernel;
    boost::multi_array<unsigned char, 2> data;

public:
    image(std::string name);
    /*
        Constructor for image class, gets a file name as input
        and calls ReadGrayscaleJPEG() to read it and save it.
    */
    void Save(std::string save_name);
    /*
        Save method for image class. Calls WriteGrayscaleJPEG to save
        the current data to a JPEG file with the name given as input.
    */
    void BoxBlur(unsigned int kernel_size);
    unsigned int Sharpness(void);

private:
    void Convolution(boost::multi_array<unsigned char, 2> &input,
                     boost::multi_array<unsigned char, 2> &output,
                     boost::multi_array<float, 2> &kernel);
    /*
        Convolution method takes an input image data, and for each
        value of a pixel in the input image, by 
        summing the product of each kernel value and the
        corresponding pixel value, the output image is created.
        For output pixels close to the boundary, the values are extended
        from the image.
    */
};
#endif /* IMAGE.HPP */