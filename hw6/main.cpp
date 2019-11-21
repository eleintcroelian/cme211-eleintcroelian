#include <string>
#include <iostream>
#include "image.hpp"

int main()
{
    image original("stanford.jpg");
    unsigned int original_sharpness = original.Sharpness();
    std::cout << "Original image: " << original_sharpness;
    for (int i = 3; i < 28; i = i + 4)
    {
        image blured("stanford.jpg");
        std::string save_name;
        if (i < 10)
            save_name = "BoxBlur0" + std::to_string(i) + ".jpeg";
        if (i > 10)
            save_name = "BoxBlur" + std::to_string(i) + ".jpeg";
        blured.BoxBlur(i);
        blured.Save(save_name);
        std::cout << " BoxBlur(" << i << "): " << blured.Sharpness();
    }
    std::cout << std::endl;
}
